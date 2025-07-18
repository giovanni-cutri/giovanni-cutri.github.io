# %% [markdown]
# # Steam Reviews Analysis
#
# [Steam](https://store.steampowered.com/) is a video game platform which allows players to buy, play and rate their favourite games, as well as leaving reviews on them.
#
# This notebook contains a text mining analysis involving the reviews left on the website for some popular video games, with the intention to gain insights on the key features of a game which leave a more long lasting impact on players and shape their opinion on it.

# %% [markdown]
# ## Import modules

# %%
import requests
import bs4
import json
import nltk

# %% [markdown]
# These are the modules we are going to use:
# - *requests* is necessary to make HTTP request to websites and get the response;
# - *bs4* is a very handy tool to extract data from a HTML source code;
# - *json* is used to exchange data in a standardized format;
# - *nltk* (Natural Language ToolKit) is essential to perform Natural Language Processing (NLP).

# %% [markdown]
# ## Retrieve data

# %% [markdown]
# Fortunately for us, Steam provides a free API with few restrictions, which makes it easy to retrieve data of any kind from the website, including the games reviews.
#
# By reading the [official documentation](https://partner.steamgames.com/doc/store/getreviews), we can find the API endpoint we are interested in and the parameters we can pass to it to modify the response.
#
# We still have to choose which games we are going to pick for our analysis. A good idea could be to use the 25 most played games on Steam, a list which can be found on this [webpage](https://steamcharts.com/top).

# %%
# make a request to the website for that page
res = requests.get("https://steamcharts.com/top")

# initialize the source code parser
soup = bs4.BeautifulSoup(res.text, "html")

# find the HTML elements which contain the ids of the games
games_elements = soup.select("a[href*='app']")

game_ids = []

# save the ids into a list
for game_element in games_elements:
    game_id = game_element.attrs["href"].split("app/")[-1]
    game_ids.append(game_id)

print(game_ids)

# %% [markdown]
# Now that we have got the identifiers for the games, we can use the API to get their reviews.

# %%
reviews_texts = []

for game_id in game_ids:

    # limit the number of reviews to 10 (default is 20)
    api_endpoint = f"https://store.steampowered.com/appreviews/{game_id}?json=1&purchase_type=all&num_per_page=10"

    res = requests.get(api_endpoint).json()

    # get the reviews for the game
    reviews = res["reviews"]

    # for each review, get the text and save it to a list
    for review in reviews:
        review_text = review["review"]
        reviews_texts.append(review_text)


# dump the list into a separate file to easily access it later
with open("reviews.json", "w", encoding="utf-8") as f:
    json.dump(reviews_texts, f)

# print a sample review
print(reviews_texts[0])

# %% [markdown]
# ## Text Mining Analysis

# %% [markdown]
# We are all set: let's import the reviews from the file and start our text mining analysis.

# %%
with open("reviews.json", "r", encoding="utf-8") as f:
    reviews = json.load(f)

for review in reviews[:5]:
    tokens = nltk.tokenize.word_tokenize(review)
    print(tokens[:5])

# %% [markdown]
# Each portion of text in our data is a *token*: they could be smaller sentences, words, characters, etc. Here we choose to consider individual words as tokens, and look at the result for each review.
#
# As we can see, unfortunately punctuation and symbols are considered as tokens on their own by the software, so we need to filter them out first. In addition to that, we also have to consider stopwords, that is, words that do not bring any particular meaning to the whole sentence, such as articles or prepositions.

# %%
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))

for review in reviews[:10]:
    tokens = word_tokenize(review)
    clean_tokens = [
        word
        for word in tokens
        if word.casefold() not in stop_words and word.casefold().isalpha()
    ]
    print(clean_tokens[:5])

# %% [markdown]
# Now the tokens are less cluttered and we start to see some interesting words which fit well into a video game review, such as "game", "playing", "download", and so on.
#

# %% [markdown]
# We can take a step further and stem the words: that means to reduce each word to its root form, just as it happens in a dictionary. This is needed because we are often not focused on the specific inflection of the word in the context, but rather the generic idea which is associated with it.

# %%
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

for review in reviews[:5]:
    tokens = word_tokenize(review)
    clean_tokens = [
        word
        for word in tokens
        if word.casefold() not in stop_words and word.casefold().isalpha()
    ]
    stemmed_words = [stemmer.stem(word) for word in clean_tokens]
    print(stemmed_words[:5])
