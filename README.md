# Telloscrap
Crawler for [Tellonym.me](https://tellonym.me)


### Description:
The script crawls the user info, questions and answers of a User and saves it to a JSON file.
It can be used as an OSINT Tool or to preserve Q/A of an account to analyze later.

### Usage:
```telloscrap.py USERNAME [--full]```

Use the parameter --full to also save metadata of each question (Off by default).


### Additional Info:
Due to some changes on the serverside of Tellonym, it's not possible anymore to crawl 100% of the Questions.
However, the script will detect how much can be crawled and collect as much as possible.
