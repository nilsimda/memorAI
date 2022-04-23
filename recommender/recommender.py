import os
import openai
import config
openai.api_key = config.OPENAI_API_KEY
# response = openai.
response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Give me a list of 5 interesting events that happened in Munich between 1970-2000",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(response)
print(type(response))

