import json
from key import API_KEY
from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key=API_KEY)

def make_call(text='', extract='entities,keywords,concepts,doc-sentiment,doc-emotion', max_items=10, indent=2):
  return json.dumps(
    alchemy_language.combined(
      text=text,
      extract=extract,
      max_items=max_items),
    indent=indent
  )
