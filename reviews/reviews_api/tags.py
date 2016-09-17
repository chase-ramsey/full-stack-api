from reviews_api.models import Tag, ReviewTag, Review
import json


def clean_up_tags():
  tag_list = Tag.objects.all()
  for tag in tag_list:
    rt_list = ReviewTag.objects.filter(tag=tag)
    if len(rt_list) == 0:
      tag.delete()


def create_review_tags(review=None, data=None, id=None, update=False):
  if review:
    watson = json.loads(review.watson_report)
  else:
    watson = json.loads(data['watson_report'])
    ReviewTag.objects.filter(review__pk=id).delete()
    review = Review.objects.get(pk=id)
  for keyword in watson['keywords']:
    try:
      tag = Tag.objects.get(word=keyword['text'])
    except:
      tag = Tag.objects.create(word=keyword['text'])
    review_tag = ReviewTag.objects.create(tag=tag, review=review)
  if update:
    clean_up_tags()
