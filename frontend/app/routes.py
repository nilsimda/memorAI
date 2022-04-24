from flask import render_template, flash, redirect, url_for, request, abort, make_response
from flask_login.utils import login_required
from app import app, db
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user
from app.models import Feedback, User
from werkzeug.urls import url_parse
from recommender.assistant import Assistant
from recommender.content import ContentGetter
from transformers import pipeline
import os

from flask_cors import CORS, cross_origin
# app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
assistant = Assistant()

@app.route('/')
@app.route('/index')
@login_required
def index():
    assistant.initialize(current_user)
    return render_template('index.html', title='Home')
                             
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='Sign In',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    return render_template('feedback.html', title='Feedback')


@app.route('/voice-journal', methods=['POST'])
@cross_origin()
def audio():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = "recording.mp3"
    full_file_name = os.path.join(app.instance_path, app.config.get('UPLOAD_FOLDER', 'uploads'), file_name)
    print(full_file_name)
    file.save(full_file_name)

    # Process Text
    text_entry = speech2text(full_file_name)
    # text_entry = "Hello I am Juan"
    print(text_entry)
    # Add Text to My Story
    assistant.add_info_user_story(text_entry)
    return text_entry

@login_required
@app.route('/assistant_page', methods=['GET', 'POST'])
def assistant_page():
    return render_template('assistant_page.html', title='AssistantPage')


@app.route('/voice-assistant', methods=['POST'])
@cross_origin()
def voice_assistant():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = "recording.mp3"
    full_file_name = os.path.join(app.instance_path, app.config.get('UPLOAD_FOLDER', 'uploads'), file_name)
    print(full_file_name)
    file.save(full_file_name)

    # Process Text
    text_entry = speech2text(full_file_name)
    print(text_entry)
    # text_entry = "Hello I am Juan"
    answer = assistant.ask(text_entry + "?")
    print(answer)
    # Add Text to My Story
    return answer

@login_required
@app.route('/recommendations')
def recommendations():
    content_getter = ContentGetter()
    event_recommendation, event_description = assistant.recommend_event()
    song_recommendation = assistant.recommend_song()
    artist_recommendation, artist_description = assistant.recommend_band()
    movie_recommendation, movie_description = assistant.recommend_film()

    # event_recommendation = "1996 Summer Olympics"
    # song_recommendation = "Feel Good Inc"
    # artist_recommendation = "Radiohead"

    print("recommended event: {}".format(event_recommendation))
    print("recommended desription: {}".format(event_description))

    # print("birth yea: ".format(event_recommendation))

    # Get Content
    images = content_getter.get_images(event_recommendation, 2)
    # images = ["0", "1", "2"]
    _, song_url = content_getter.get_yt_link(song_recommendation + "acoustic cover")
    _, artist_url = content_getter.get_yt_link(artist_recommendation + "acoustic cover")
    _, movie_url = content_getter.get_yt_link(movie_recommendation + "trailer")

    print(song_url)
    print(artist_url)


    return render_template('recommendations.html', title='Recommendations', 
                            event_img1 = images[0], event_img2 = images[1],
                            event_text = event_recommendation, event_description=event_description,
                            artist_name=artist_recommendation, artist_description=artist_description,
                            movie_name=movie_recommendation,movie_description=movie_description,
                            song_name=song_recommendation,
                            song_url1=song_url , song_url2=artist_url, movie_url=movie_url)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                birth_year=form.birth_year.data,
                birth_place=form.birth_place.data,
                current_place=form.current_place.data,
                favorite_band=form.favorite_band.data,
                favorite_film=form.favorite_film.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

def speech2text(audio_file):
        asr = pipeline(
            task="automatic-speech-recognition",
            model= "facebook/wav2vec2-base-960h",
            tokenizer= "facebook/wav2vec2-base-960h",
        )
        return asr(audio_file)["text"]

