#!/usr/bin/python
import praw
import pdb
import re
import os
import sys

# Create the Reddit instance
user_agent = "Windows:ReadReactBot:0.1 (by /u/rgautier)"
r = praw.Reddit(user_agent=user_agent)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = filter(None, posts_replied_to)

# Get the top 5 values from our subreddit
subreddit = r.get_subreddit('pcmasterrace')

f = open("posts_replied_to.txt","a")
for submission in subreddit.get_hot(limit=50):
    print "reviewing: " + submission.title.encode('utf-8')

    # If we haven't replied to this post before
    if submission.id not in posts_replied_to:

        # Do a case insensitive search
        if re.search("giveaway", submission.title, re.IGNORECASE):
            # Reply to the post
            try:
                print submission.selftext.encode('utf-8')
            except:
		print "Error: ", sys.exc_info()[0]
                print "Probably rate limited cuz you're a bot."
                f.close()
                quit()
            else:
                print "Bot replying to : ", submission.title
                # write these out as we go so if we get rate limited, we have the data 
                f.write(submission.id + "\n")
      
                # Store the current id into our list
                posts_replied_to.append(submission.id)

# Close out the submissions replied to
f.close()
