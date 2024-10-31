options(warn = -1)
library(RSQLite)
library(dplyr, warn.conflicts=FALSE)
library(ggplot2)
library(lubridate, warn.conflicts=FALSE)
library(tidyr)

dir.create("data")
url <- "http://infinity.unstable.life/Flashpoint/Data/flashpoint.sqlite"
destfile <- "data/flashpoint.sqlite"

# by default, there is a 60 seconds timeout limit when downloading a file
# this can be a problem when downloading large files, so we increase that limit
options(timeout = 300)

download.file(url, destfile)
  
con <- dbConnect(SQLite(), "data/flashpoint.sqlite")
games <- dbReadTable(con, "game")
dbDisconnect(con)

str(games)

games <- games %>% select(id, title, developer, publisher, platform,
                          releaseDate, language, library, tagsStr)

str(games)

head(games)

top_developers <- games %>% count(developer) %>% arrange(desc(n)) %>% head(10)
top_developers

top_developers <- games %>% filter(developer != "") %>% count(developer) %>%
  arrange(desc(n)) %>% head(10)
top_developers

top_publishers <- games %>% filter(publisher != "") %>% count(publisher) %>%
  arrange(desc(n)) %>% head(10)
top_publishers

top_developers %>% as.data.frame() %>%
  ggplot(aes(x = reorder(developer, n), y = n, fill = developer)) +
  geom_bar(stat = "identity") + coord_flip() +
  scale_y_continuous(breaks = seq(0, 2500, by = 500)) +
  ggtitle("Top ten developers distribution") +
  theme(legend.position = "none", axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.y = element_text(face = "bold"))

sizes <- round(top_developers$n / sum(top_developers$n) * 100, 1)
labels <- vector()

for(i in 1:(length(sizes))){
  labels[i] <- paste(top_developers$developer[i], "-", toString(sizes[i]), "%")
}
  
top_developers %>% as.data.frame() %>%
  ggplot(aes(x = "", y = sizes, fill = reorder(developer, -n))) +
  geom_bar(stat = "identity", width = 1, color = "black") +
  coord_polar(theta = "y", start = 0) +
  theme(axis.text = element_blank(), axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        legend.title = element_blank()) +
  scale_fill_discrete(labels = labels) +
  ggtitle("Top ten developers distribution")

top_publishers %>% as.data.frame() %>%
  ggplot(aes(x = reorder(publisher, n), y = n, fill = publisher)) +
  geom_bar(stat = "identity") + coord_flip() +
  scale_y_continuous(breaks = seq(0, 8000, by = 1000)) +
  ggtitle("Top ten publishers distribution") +
  theme(legend.position = "none", axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.y = element_text(face = "bold"))

sizes <- round(top_publishers$n / sum(top_publishers$n) * 100, 1)
labels <- vector()

for(i in 1:(length(sizes))){
  labels[i] <- paste(top_publishers$publisher[i], "-", toString(sizes[i]), "%")
}

top_publishers %>% as.data.frame() %>%
  ggplot(aes(x = "", y = sizes, fill = reorder(publisher, -n))) +
  geom_bar(stat = "identity", width = 1, color = "black") +
  coord_polar(theta = "y", start = 0) +
  theme(axis.text = element_blank(), axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        legend.title = element_blank()) +
  scale_fill_discrete(labels = labels) +
  ggtitle("Top ten publishers distribution")

dates <- games %>% filter(releaseDate != "") %>%
  select(title, releaseDate, platform, library) %>%
  arrange(releaseDate)
head(dates)
tail(dates)

dates$releaseDate <- dates$releaseDate %>% ymd(truncated = 2)
dates <- dates %>% na.omit() %>% arrange(releaseDate)
head(dates)
tail(dates)

dates <- dates %>% slice(1:(nrow(dates)-2))
head(dates, 20)

dates <- dates %>% slice(2:nrow(dates))
tail(dates, 20)

dates %>% filter(platform == "Flash") %>% head(20)

top_platforms <- dates %>% count(platform) %>% arrange(desc(n)) %>% head(5)
top_platforms

colors <- c("red", "orange", "blue", "green", "black")

top_platforms %>% as.data.frame() %>% arrange(platform) %>%
  ggplot(aes(x = reorder(platform, n), y = n, fill = platform)) +
  geom_bar(stat = "identity") + coord_flip() +
  scale_y_continuous(breaks = seq(0, 60000, by = 10000)) +
  ggtitle("Top five platforms distribution") +
  theme(legend.position = "none", axis.title.x = element_blank(),
        axis.title.y = element_blank(), axis.text.y = element_text(face = "bold")) +
  scale_fill_manual(values = colors)

sizes <- round(top_platforms$n / sum(top_platforms$n) * 100, 1)
labels <- vector()

for(i in 1:(length(sizes))){
  labels[i] <- paste(top_platforms$platform[i], "-", toString(sizes[i]), "%")
}

colors <- c("red", "orange", "green", "black", "blue")

top_platforms %>% as.data.frame() %>%
  ggplot(aes(x = "", y = sizes, fill = reorder(platform, -n))) +
  geom_bar(stat = "identity", width = 1, color = "black") +
  coord_polar(theta = "y", start = 0) +
  theme(axis.text = element_blank(), axis.title.x = element_blank(),
        axis.title.y = element_blank(), legend.title = element_blank()) +
  scale_fill_manual(labels = labels, values = colors) +
  ggtitle("Top five platforms distribution")

year_platform <- dates %>% filter(platform %in% top_platforms$platform)
years <- year_platform$releaseDate %>% sapply(substr, start = 1, stop = 4)
year_platform$releaseDate <- years

colors <- c("red", "orange", "blue", "green", "black")

year_platform %>% count(releaseDate, platform) %>%
  ggplot(aes(x = releaseDate, y = n, fill = platform, width = 0.5)) +
  geom_bar(position = position_stack(reverse = TRUE), stat = "identity") +
  scale_y_continuous(breaks = seq(0, 6000, by = 1000)) +
  theme(axis.title.x = element_blank(),
        axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1),
        axis.title.y = element_blank()) +
  scale_fill_manual(values = colors)

top_languages <- games %>% filter(language != "") %>% { . ->> tmp } %>%
  select(language) %>%
  vapply(gsub, pattern = ",", replacement = ";", character(nrow(tmp))) %>%
  as.data.frame() %>%
  separate_rows(language, sep = "; ") %>% count(language) %>%
  arrange(desc(n)) %>%
  filter(language != "en") %>% head(10)
top_languages

top_languages %>% as.data.frame() %>% arrange(language) %>%
  ggplot(aes(x = reorder(language, n), y = n, fill = language)) +
  geom_bar(stat = "identity") + coord_flip() +
  scale_y_continuous(breaks = seq(0, 8000, by = 1000)) +
  ggtitle("Top ten languages distribution") +
  theme(legend.position = "none", axis.title.x = element_blank(),
        axis.title.y = element_blank(), axis.text.y = element_text(face = "bold"))

sizes <- round(top_languages$n / sum(top_languages$n) * 100, 1)
labels <- vector()

for(i in 1:(length(sizes))){
  labels[i] <- paste(top_languages$language[i], "-", toString(sizes[i]), "%")
}

top_languages %>% as.data.frame() %>%
  ggplot(aes(x = "", y = sizes, fill = reorder(language, -n))) +
  geom_bar(stat = "identity", width = 1, color = "black") +
  coord_polar(theta = "y", start = 0) +
  theme(axis.text = element_blank(), axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        legend.title = element_blank()) +
  scale_fill_discrete(labels = labels) +
  ggtitle("Top ten languages distribution")

top_genres <- games %>% filter(tagsStr != "") %>% { . ->> tmp } %>%
  select(tagsStr) %>%
  vapply(gsub, pattern = ",", replacement = ";", character(nrow(tmp))) %>%
  as.data.frame() %>%
  separate_rows(tagsStr, sep = "; ") %>% count(tagsStr) %>%
  arrange(desc(n)) %>% head(10)
top_genres

top_genres %>% as.data.frame() %>%
  ggplot(aes(x = reorder(tagsStr, n), y = n, fill = tagsStr)) +
  geom_bar(stat = "identity") + coord_flip() +
  scale_y_continuous(breaks = seq(0, 30000, by = 5000)) +
  ggtitle("Top ten genres distribution") +
  theme(legend.position = "none", axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.y = element_text(face = "bold"))

sizes <- round(top_genres$n / sum(top_genres$n) * 100, 1)
labels <- vector()

for(i in 1:(length(sizes))){
  labels[i] <- paste(top_genres$tagsStr[i], "-", toString(sizes[i]), "%")
}

top_genres %>% as.data.frame() %>%
  ggplot(aes(x = "", y = sizes, fill = reorder(tagsStr, -n))) +
  geom_bar(stat = "identity", width = 1, color = "black") +
  coord_polar(theta = "y", start = 0) +
  theme(axis.text = element_blank(), axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        legend.title = element_blank()) +
  scale_fill_discrete(labels = labels) +
  ggtitle("Top ten genres distribution")

most_played <- read.csv("data/most_played.csv") %>% rename(id = category)
most_played

rank <- inner_join(games, most_played, by = join_by(id)) %>% arrange(desc(Play.Count))
rank

rank %>% ggplot(aes(x = reorder(title, Play.Count), y = Play.Count, fill = title)) +
  geom_bar(stat = "identity") + coord_flip() +
  scale_y_continuous(breaks = seq(0, 50000, by = 10000)) +
  ggtitle("Top forty Flashpoint games by play count") +
  theme(legend.position = "none", axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1),
        axis.text.y = element_text(face = "bold"))
