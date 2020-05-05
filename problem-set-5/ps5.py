# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import os.path

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:

        description = ''
        if hasattr(entry, 'description'):
            description = translate_html(entry.description)

        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title
        
    def get_description(self):
        return self.description
        
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.invariant_check(phrase)
        self.phrase = phrase

    def invariant_check(self, phrase):
        phrase_words = phrase.split(' ')
        assert('' not in phrase_words)
        for word in phrase_words:
            assert(word.isalpha())

    def get_phrase(self):
        return self.phrase

    def is_phrase_in(self, text):

        phrase = self.get_phrase().lower()

        text_words = text \
            .translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))) \
            .translate(str.maketrans(string.digits, ' ' * len(string.digits))) \
            .lower() \
            .split()

        def is_subset(subset, superset):
            for word in subset:
                if word not in superset:
                    return False
            return True

        return is_subset(phrase.split(), text_words) and phrase in ' '.join(text_words)

# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, title):
        PhraseTrigger.__init__(self, title)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, description):
        PhraseTrigger.__init__(self, description)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time_string):
        self.time = datetime.strptime(time_string, "%d %b %Y %H:%M:%S") \
                            .replace(tzinfo=pytz.timezone("EST"))

    def get_time(self):
        return self.time

# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, time_string):
        TimeTrigger.__init__(self, time_string)

    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) < self.get_time()

class AfterTrigger(TimeTrigger):
    def __init__(self, time_string):
        TimeTrigger.__init__(self, time_string)

    def evaluate(self, story):
        return self.get_time() < story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, other):
        self.other_trigger = other
    
    def evaluate(self, story):
        return not self.other_trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, lhs, rhs):
        self.lhs_trigger = lhs
        self.rhs_trigger = rhs

    def evaluate(self, story):
        return self.lhs_trigger.evaluate(story) and \
               self.rhs_trigger.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, lhs, rhs):
        self.lhs_trigger = lhs
        self.rhs_trigger = rhs

    def evaluate(self, story):
        return self.lhs_trigger.evaluate(story) or \
               self.rhs_trigger.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
                break
    return filtered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!

    TRIGGER_DEF = ['TITLE','DESCRIPTION','AFTER','BEFORE','NOT','AND',"OR"]
    ADD = 'ADD'

    TRIGGER_DICT = {}

    def get_trigger(t):
        if t[1] == 'TITLE':
            return TitleTrigger(t[2])
        elif t[1] == 'DESCRIPTION':
            return DescriptionTrigger(t[2])
        elif t[1] == 'AFTER':
            return AfterTrigger(t[2])
        elif t[1] == 'BEFORE':
            return BeforeTrigger(t[2])
        elif t[1] == 'NOT':
            return NotTrigger(TRIGGER_DICT[t[2]], TRIGGER_DICT[t[3]])
        elif t[1] == 'AND':
            return AndTrigger(TRIGGER_DICT[t[2]], TRIGGER_DICT[t[3]])
        elif t[1] == 'OR':
            return OrTrigger(TRIGGER_DICT[t[2]], TRIGGER_DICT[t[3]])
        else:
            raise Exception('Something went wrong...')

    trigger_file = open(filename, 'r')
    lines = []
    triggerlist = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            t = line.split(',')
            if t[0] != 'ADD':
                TRIGGER_DICT[t[0]] = get_trigger(t)
            else:
                for i in t[1:]:
                    triggerlist.append(TRIGGER_DICT[i])
    return triggerlist


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:

        # Problem 11
        my_path = os.path.abspath(os.path.dirname(__file__))
        triggerlist = read_trigger_config(os.path.join(my_path, 'triggers.txt'))

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':

    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

