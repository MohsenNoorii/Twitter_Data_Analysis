#!/usr/bin/env python
"""
With mask Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""
from persian_wordcloud.wordcloud import PersianWordCloud, add_stop_words
from wordcloud import STOPWORDS as EN_STOPWORDS
from os import path
from PIL import Image
import numpy as np

d = path.dirname(__file__)
twitter_mask = np.array(Image.open(path.join(d, "twitter-logo.jpg")))

text='ا طه_محـری فاطمه_سادات alborz.1986 Amir_Sharifi '

stopwords = add_stop_words(['کاسپین'])
stopwords |= EN_STOPWORDS

# Generate a word cloud image

wordcloud = PersianWordCloud(
    only_persian=False,
    max_words=200,
    stopwords=stopwords,
    margin=0,
    width=800,
    height=800,
    min_font_size=1,
    max_font_size=500,
    random_state=True,
    background_color="white",
    mask=twitter_mask
).generate(text)

image = wordcloud.to_image()
image.show()
image.save('en-fa-result.png')