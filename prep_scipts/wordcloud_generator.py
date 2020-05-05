from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk
import re
import string
import pathlib

import mainController as mainCtrl

# run calculations for 5 debates to get word clouds
debate_names = ["Green Belt - Moral Maze", "Hypocrisy - Moral Maze", "Syria - Moral Maze",
                "Problem Families - Moral Maze", "Welfare State - Moral Maze"]

for debateName in debate_names:
    # get transcript text
    debate_text = mainCtrl.get_full_transcript(debateName)

    # clean up text: basics
    debate_text = debate_text.lower()
    # remove html tags
    html_tags_re = re.compile('<.*?>')
    debate_text = re.sub(html_tags_re, '', debate_text)

    # get words in text
    words = nltk.word_tokenize(debate_text)

    # set stopwords: unnecessary words
    # set participant names as stopwords
    participant_list = mainCtrl.get_participants_list(debateName)
    first_names = [speaker["first_name"].lower() for speaker in participant_list]
    last_names = [speaker["last_name"].lower() for speaker in participant_list]

    # various words manually selected from images that are not considered to be superfluous in the cloud
    manual_stopwords = [" ve", "re", "ca", "yes", "michael", "groeger wilson", "co", "didn", "edwina",
                        "aaron", "ll", "doesn", "don", "cl", "km", "mh", "cf", "mb", "mp", "ks", "going",
                        "mr", "pq", "really", "absolutely", "go", "isn", "theo", "ve", "ve got", "wouldn",
                        "indeed", "much", "take", "balick", "giles", "actually", "might", "said", "make",
                        "looking", "garret", "ve", " re", "re ", " ll", " ll"]

    # remove stopwords from text
    stopwords = list(STOPWORDS) + list(string.punctuation) + ["n't"] + manual_stopwords + first_names + last_names
    filtered = [word for word in words if not word in stopwords]

    # generate word cloud and graphic
    plt.figure(figsize=(20, 15))
    # text = 'all your base are belong to us all of your base base base'
    wordcloud = WordCloud(width=1800, height=1400, background_color="white", max_words=100).generate(" ".join(filtered))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    # save image
    parent_dir = pathlib.Path(__file__).parent.parent
    path = parent_dir.joinpath("views\\assets\\" + debateName + "_wordcloud.jpg").resolve()
    plt.savefig(path)
    print("Saved Wordcloud for " + debateName)
    # plt.show()

