import json
import re
from reviews_api.key import API_KEY
from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key=API_KEY)

def make_call(text='', extract='entities,keywords,concepts,doc-sentiment,doc-emotion', max_items=10, indent=2):
  text = re.sub('__(.*)__', '', text)
  text = re.sub('/(.*)/', '', text)
  text = re.sub('`(.*)`', '', text)
  return json.dumps(
    alchemy_language.combined(
      text=text,
      extract=extract,
      max_items=max_items),
    indent=indent
  )
