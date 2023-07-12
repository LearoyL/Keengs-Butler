import praw
import NSFWlist
import random
import pandas as pd
def boooba():
    # Define user agent
    user_agent = "praw_scraper_1.0"

    # Create an instance of reddit class
    reddit = praw.Reddit(username="learoy_",
                         password="2598Dodo$",
                         client_id="DjNQpJBDJNllDQt6ARoC4g",
                         client_secret="QfozboqTBRzV7T095aZ8gX116dOFvg",
                         user_agent= user_agent
                         )

    # Create sub-reddit instance
    cat = NSFWlist.doggy
    randomnum = random.randrange(0, len(cat))
    print (randomnum)
    subreddit_name = cat[randomnum]
    print (subreddit_name)
    subreddit = reddit.subreddit(subreddit_name)

    df = pd.DataFrame()  # creating dataframe for displaying scraped data

    # creating lists for storing scraped data
    titles = []
    scores = []
    ids = []
    urls = []

    # looping over posts and scraping it
    for submission in subreddit.top(limit=1):
        titles.append(submission.title)
        urls.append(submission.url)
        scores.append(submission.score)  # upvotes
        ids.append(submission.id)

    df['Title'] = titles
    df['Id'] = ids
    df['URL'] = urls
    df['Upvotes'] = scores  # upvotes

    ##print(df)
    print(urls)
    print(df.shape)
    df.head(10)
    finalurl= urls[0]
    return finalurl