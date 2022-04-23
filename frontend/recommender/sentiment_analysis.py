import openai
from recommender import config
from recommender import templates
from easydict import EasyDict as edict

openai.api_key = config.OPENAI_API_KEY

def analyze_sentiment(text,engine="text-davinci-002"):
    response = openai.Completion.create(
    engine=engine,
    prompt=templates.feedback.format(text),
    temperature=0.5,
    max_tokens=16,
    top_p=1.0,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response["choices"][0]["text"]