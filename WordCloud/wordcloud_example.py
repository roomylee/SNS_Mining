from collections import Counter
from konlpy.tag import *
import pytagcloud
from NLP import *




query = "Select * from twitter_reply where Inclination = 1"
words = extract_frequent_words(query, is_repost=True)

print(words)
print(type(words))


taglist = pytagcloud.make_tags(words[:60], maxsize=150)
pytagcloud.create_tag_image(taglist, 'wordcloud.jpg', size=(600, 400), fontname='BMHANNA_11yrs_ttf', rectangular=False)
