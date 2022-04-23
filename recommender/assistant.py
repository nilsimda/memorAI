import openai
import config
import templates
import random
import csv
from easydict import EasyDict as edict

openai.api_key = config.OPENAI_API_KEY

class Assistant(object):
    def __init__(self, user_filename, engine="text-davinci-002"):
        self.engine = engine
        user = {}
        with open(user_filename, mode='r', encoding='utf-16') as inp:
            reader = csv.reader(inp)
            user = {cols[0]:cols[1] for cols in reader}
        self.user = edict(user)
        self.user.my_story = templates.my_story.format(self.user.name, self.user.birth_year, 
                                                        self.user.birth_place, self.user.current_place, 
                                                        self.user.favorite_band, self.user.favorite_film)
    
    def initialize(self):
        _ = self.send_query(templates.init_query.format(self.user.name))

    def add_info_user_story(self,info):
        self.user.my_story += (info+".")

    def recommend_film(self):
        return self.send_query(templates.film_query.format(self.user.favorite_film))

    def recommend_band(self):
        return self.send_query(templates.band_query.format(self.user.favorite_band))

    def recommend_song(self):
        return self.send_query(templates.song_query.format(self.user.favorite_band))

    def recommend_event(self):
        year = int(self.user.birth_year)+random.randint(15,50)
        year = int((year/10)*10)
        print("year: {}".format(year))
        return self.send_query(templates.historical_query.format(self.user.birth_place, year))
    
    def ask(self, question):
        return self.send_query(self.user.my_story + "\n\nHuman: " + question)
    
    def send_query(self,msg,max_tokens=32):
        response = openai.Completion.create(
        engine=self.engine,
        prompt=msg,
        temperature=0.6,
        max_tokens=max_tokens,
        top_p=0.8,
        frequency_penalty=0,
        presence_penalty=0
        )
        return response["choices"][0]["text"]
