# Telloscrap
Crawler for [Tellonym.me](https://tellonym.me)


### Description:
The script crawls the user info, questions and answers of a Tellonym User and saves it to a JSON file.

### Usage:
```telloscrap.py USERNAME [--full]```

Use the parameter --full to also save metadata of each question (Off by default).


### Additional Info:
Due to some changes on the serverside of Tellonym, it's not possible anymore to crawl 100% of the Questions.
However, the script will detect how much can be crawled and collect as many as possible.


### Disclaimer:
_Use this script on your own risk. The author cannot guarantee it's working reliable and won't take any resposibility for misuse._
