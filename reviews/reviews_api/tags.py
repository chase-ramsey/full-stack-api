from reviews_api.models import Tag, ReviewTag
import json

def create_review_tags(review, update=False):
  watson = json.loads(review.watson_report)
  if update:
    ReviewTag.objects.filter(review=review).delete()
  for concept in watson['concepts']
    try:
      tag = Tag.objects.get(word=concept['text'])
    except:
      tag = Tag.objects.create(word=concept['text'])
    review_tag = ReviewTag.objects.create(tag=tag, review=review)
