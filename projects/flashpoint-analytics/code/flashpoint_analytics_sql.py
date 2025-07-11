# %% [markdown]
# # Flashpoint Analytics
#
# [Flashpoint Archive](https://flashpointarchive.org/?lang=en-US) is a web-game preservation project, made in 2018 in an effort to save as many games as possible from the then upcoming [Flash End-of-Life](https://www.adobe.com/products/flashplayer/end-of-life-alternative.html), while also making them playable for everyone. Today, it hosts more than 170 000 games and thousands of active users all around the world.
#
# This notebook contains a descriptive statistical analysis about the games available in Flashpoint, with an emphasis on categorical data, such as the technology that was used to make them or the publisher who used to host them in the past.
#
# The Flashpoint database, which keeps all the data that will be used in the analysis, can be found [here](https://web.archive.org/web/20230621043837/https://infinity.unstable.life/Flashpoint/Data/flashpoint.sqlite).

# %% [markdown]
# ## Import modules

# %%
import os
import urllib.request
import sqlite3

# %% [markdown]
# These are the modules that we are going to use for our analysis. We are working with Python, but instead of relying on the *pandas* module like in the other notebook, we are going to write and run SQL queries directly to get the information we want.

# %% [markdown]
# ## Retrieve data

# %%
try:
    os.mkdir("data")
except FileExistsError:
    pass

# download data from the source (it can take a while)

url = "https://web.archive.org/web/20230621043837id_/https://infinity.unstable.life/Flashpoint/Data/flashpoint.sqlite"
filename = "data/flashpoint.sqlite"
urllib.request.urlretrieve(url, filename)

# connect to the database and create a cursor

con = sqlite3.connect("data/flashpoint.sqlite")
cur = con.cursor()

# %% [markdown]
# We have created a connection with the database and a cursor which we will use to execute our queries and retrieve the results.

# %% [markdown]
# ## Explore data

# %% [markdown]
# Let's have a first look at our data.

# %%
res = cur.execute("PRAGMA table_info(game);").fetchall()
res

# %% [markdown]
# We have used the PRAGMA command, which is exclusive to SQLite (it is one of the things that differentiate it from other SQL flavors such as MySQL, SQL Server, and so on).
#
# There are 27 columns in the table: we can see the name of each field, its data type (mostly *varchar*, therefore characters and text), the possibility of the field being NULL (0) or not (1), its default value (which is None for almost all of them) and finally whether it is part of the primary key (1) or not (0). As we could expect, the *id* of the game, which is needed to uniquely identify it, serves as a primary key in the table structure.
#
# We are going to need only some of these variables for our goal, so let's keep the relevant ones and look at the first rows of our dataset.

# %%
vars_to_keep = [
    "id",
    "title",
    "developer",
    "publisher",
    "platform",
    "releaseDate",
    "language",
    "library",
    "tagsStr",
]
vars_to_keep = ", ".join(vars_to_keep)
vars_to_keep
res = cur.execute("SELECT %s FROM game LIMIT 3;" % (vars_to_keep)).fetchall()

for row in res:
    print(" | ".join(str(x) for x in row))

# %% [markdown]
# We can already notice that there is some missing data, especially in the *Release Date* and *Language* fields.

# %% [markdown]
# ## Analyze data

# %% [markdown]
# ### Developers and Publishers

# %% [markdown]
# We may be interested to know who are the most prolific developers and publishers. Let's find out by creating a frequency table for each variable and looking at the first ten entries.

# %%
top_developers = cur.execute(
    "SELECT developer, count(*) FROM game GROUP BY developer ORDER BY count(*) DESC LIMIT 10"
).fetchall()
top_developers

# %% [markdown]
# The first row is blank because of the issue we noticed earlier: some games do not have a developer value associated to them in the database. Let's filter out those entries.

# %%
top_developers = cur.execute(
    "SELECT developer, count(*) FROM game WHERE developer != '' GROUP BY developer ORDER BY count(*) DESC LIMIT 10"
).fetchall()
top_developers

# %% [markdown]
# These are the most represented developers in the database. As a Flash games fan may notice at first glance, most of them are specialised in escape games; therefore, we can suppose that it should be a very popular genre: we will dig into this later.
#
# Before moving on, Neopets deserves a special mention for how it managed to build a passionate community still active after over 25 years since its release in 1999.

# %%
top_publishers = cur.execute(
    "SELECT publisher, count(*) FROM game WHERE publisher != '' GROUP BY publisher ORDER BY count(*) DESC LIMIT 10"
).fetchall()
top_publishers

# %% [markdown]
# Among the publishers, we can see some very renowned names, at least in the gaming community, like *Newgrounds*, *Armor Games* and *Kongregate*. There is also a considerable amount of licensed games published by TV broadcasters, such as *Disney*, *Nickelodeon* and *Cartoon Network*, supposedly to promote their shows.
#
# The main publishing platform is DeviantArt, which, despite being known mostly as a place for artists to store their drawings, also offers the possibility to share Flash content.

# %% [markdown]
# ### Release Dates and Platforms

# %% [markdown]
# Flash games started to appear towards the end of the twentieth century and became popular in the next decade, before slowly fading out in favour of mobile games.
#
# Let's observe the release dates we have got here, keeping in mind that they are not specified for all games.

# %%
older_dates = cur.execute(
    "SELECT title, releaseDate, platform, library FROM game WHERE releaseDate != '' ORDER BY releaseDate LIMIT 10"
).fetchall()
older_dates

# %%
newer_dates = cur.execute(
    "SELECT title, releaseDate, platform, library FROM game WHERE releaseDate != '' ORDER BY releaseDate DESC LIMIT 10"
).fetchall()
newer_dates

# %% [markdown]
# There seems to be a problem with the data: entries should follow the "YYYY-MM-DD" date format as per Flashpoint guidelines, but some games come with a different one; in addition, if the exact day or month of release is unknown, specifying the year only is also allowed.

# %% [markdown]
# Ignoring the problematic data, we see that the oldest game in the list is *Blastar*, which was released in 1984. Actually, the game present in Flashpoint is a HTML5 version, which was developed and released much more recently.
#
# Moving on, starting from 1993 we recognize some old technologies, such as *Shochwave*, *VRML* and *Hyper-G*.
#
# We can actually distinguish between proper games and animations by looking at the *library* column: the former are labeled with *arcade*, the latter with *theatre* values. Thus, the oldest animation featured is *Idle Johnny* from 1993, while the first "true" game (not counting *Blastar*) could be either *QP-Shot 1000* (which came out some time in 1994), or *Virtual Banana Original* and *Virtual University of Auckland*, both from February 1994.

# %% [markdown]
# On the other side, looking at more recent games, we find out that nowadays *HTML5* is the standard technology to make browser games.

# %% [markdown]
# For the sake of completeness, let's restrict our search to *Flash*-only games.

# %%
older_flash = cur.execute(
    "SELECT title, releaseDate, platform, library FROM game WHERE releaseDate != '' and platform = 'Flash' ORDER BY releaseDate LIMIT 10"
).fetchall()
older_flash

# %% [markdown]
# The first *Flash* game is *Claus.com* from 1995. We notice from the titles that most of these are actually websites built in *Flash* and not individual games or animations.

# %% [markdown]
# To take an overall view, let's compare the various platforms by games count, considering the top five.

# %%
top_platforms = cur.execute(
    "SELECT platform, count(*) FROM game GROUP BY platform ORDER BY count(*) DESC LIMIT 5;"
).fetchall()
top_platforms

# %% [markdown]
# *Flash* is clearly the winner, followed by a rising *HTML5* and its old companion *Shockwave*, with *Unity* and *Java* as outsiders.

# %% [markdown]
# ## Most common languages

# %% [markdown]
# Let's move on to another topic: *Flashpoint* allows non-English content as well, and it can be interesting to know which countries have contributed the most to the world of web games aside from the anglophone ones.

# %%
top_languages = cur.execute(
    "SELECT language, count(*) FROM game WHERE language != '' and language NOT LIKE '%en%' GROUP by language ORDER BY count(*) DESC LIMIT 10"
).fetchall()
top_languages

# %% [markdown]
# We can see a strong presence of Asian content, with Japanese, Korean and Chinese among the top ten languages. The rest of the list is completed by several European countries.

# %% [markdown]
# ## Most popular genres

# %% [markdown]
# Let's now focus on game genres, featured on the *tagsStr* column, to discover the most common ones.

# %%
top_genres = cur.execute(
    "SELECT tagsStr, count(*) FROM game WHERE tagsStr != '' GROUP by tagsStr ORDER BY count(*) DESC LIMIT 10"
).fetchall()
top_genres

# %% [markdown]
# The big three genres are *Arcade*, *Puzzle* and *Adventure* and honestly it's kind of odd to see *Action* at such a low position. Conversely, as we expected from our previous analysis on developers, *Escape the Room* is fairly popular, along with *Dress Up* and *Simulation* games.

# %%
con.close()

# %% [markdown]
# ## Most played games

# %% [markdown]
# As a final insight, let's find out which are the most played games among the *Flashpoint* users: to do this, we are going to use some official statistics from the platform itself. Visit [this webpage](https://web.archive.org/web/20230622070602/https://flashpoint-analytics.unstable.life/), scroll down to the corresponding section and download the data in *.csv* format.

# %%
import pandas

con = sqlite3.connect("data/most_played.sqlite")

df = pandas.read_csv("data/most_played.csv")
df.to_sql("most_played", con, if_exists="append", index=False)

cur = con.cursor()

most_played = cur.execute("SELECT * FROM most_played").fetchall()

for row in most_played[:10]:
    print(row)
con.close()


# %% [markdown]
# The file contains the *id* for the most 40 played games, along with a play count. Let's use the identifiers to find the titles of these games and other info by combining the main dataframe and the new data.

# %%
ids = []

for row in most_played:
    id = row[0]
    ids.append(id)

con = sqlite3.connect("data/flashpoint.sqlite")
cur = con.cursor()

placeholders = ",".join(["?"] * len(ids))
query = f"SELECT title FROM game WHERE id IN ({placeholders})"
titles = cur.execute(query, ids).fetchall()
titles


# %% [markdown]
# ## Conclusion

# %% [markdown]
# This was a thorough analysis of the *Flashpoint* catalogue, which hopefully gives some insights about the world of web-based games and their significant relevance in the history of the Internet.
#
# The effort to preserve this kind of content has generated amazing results, saving an astounding quantity of material which would have disappeared otherwise. Despite the concrete risk of a digital dark age, we should insist on preserving the stuff that we care about and keep it alive, not only for historical reasons, but also for the nostalgic value we associate with it.
