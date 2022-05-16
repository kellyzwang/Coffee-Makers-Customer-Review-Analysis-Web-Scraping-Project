"""
This program works with three coffee maker product customer review datasets,
processes data, and implements functions that create data visualizations
needed to answer the third research question: "Which coffee maker does
customers like the most and stands out as the most efficient or
user-friendly? (For the customer reviews of each coffee maker,
what are their most appeared positive and negative keywords?)"
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import string
import plotly.express as px
from heapq import nlargest
from nltk.corpus import stopwords


def plot_rating_histogram(df, brand):
    """
    Takes a coffee maker product review dataframe 'df' and a string
    'brand' as parameters.
    Plots a customer rating histogram for the 'brand' coffee maker
    Creates and a new directory 'images' if it doesn't exist and save
    the plot in the 'images' folder.
    """
    fig = px.histogram(df, x="rating", title="{} Customer Rating"
                       .format(brand))
    # create a new directory 'images'
    if not os.path.exists("images"):
        os.mkdir("images")
    path_name = "images/{}_rating_hist.png".format(brand)
    fig.write_image(path_name)


def get_word_count(df, n):
    """
    Takes a coffee maker product review dataframe 'df' as parameter.
    Returns the first n most appeared words and its count as a dict.
    Does not count any English stop words in the NLTK library.
    """
    word_count = {}
    sw_nltk = stopwords.words('english')
    for review in df['review_title']:
        # remove punctuation in review_body
        review = review.translate(str.maketrans('', '', string.punctuation))
        words = review.split()
        for word in words:
            if word.lower() not in sw_nltk:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
    most_appeared = dict(nlargest(n, word_count.items(), key=lambda i: i[1]))
    return most_appeared


def plot_most_freq_words_bar(df, brand):
    """
    Takes a coffee maker product review dataframe 'df' and a string
    'brand' as parameters.
    Plots a bar chart that displays the first 30 most frequently appeared
    words in the product review titles for the 'brand' coffee maker.
    """
    # clear matplotlib canvas
    plt.clf()
    plt.cla()
    most_appeared = get_word_count(df, 30)
    y_pos = np.arange(len(most_appeared.keys()))
    plt.barh(y_pos, most_appeared.values(), color='mediumpurple')
    plt.yticks(y_pos, most_appeared.keys())
    plt.xticks(np.arange(0, max(most_appeared.values())+1, 1.0))
    plt.title('Most Common Words in review_title for {}'
              .format(brand))
    plt.tight_layout()
    # create a new directory 'images' if it doesn't exist
    if not os.path.exists("images"):
        os.mkdir("images")
    path_name = "images/{}_most_fre_words_bar.png".format(brand)
    plt.savefig(path_name)
    plt.close()


def add_sentiment(df):
    """
    Takes a coffee maker product review dataframe 'df'.
    Classifies reviews into "positive" and "negative", a review will
    be considered "positive" if it has a rating > 3, "negative" if
    it has a rating < 3, "neutral" if it has a rating of 3.
    Returns a new dataframe with an added "sentiment" column.
    """
    new_df = df.copy()
    sentiment_list = []
    for rating in new_df['rating']:
        if rating > 3:
            sentiment_list.append("positive")
        elif rating < 3:
            sentiment_list.append("negative")
        else:
            sentiment_list.append("neutral")

    new_df['sentiment'] = sentiment_list
    return new_df


def plot_most_freq_words_sentiment_bar(df, brand, sentiment):
    """
    Takes a coffee maker product review dataframe 'df', a string
    'brand', and a string 'sentiment' as parameters.
    Plots a bar chart that displays the first 30 most common words in
    the product review titles for the 'brand' coffee maker and the given
    'sentiment'.
    """
    # filter df to keep only reviews with the given sentiment
    new_df = add_sentiment(df)
    sentiment_mask = new_df['sentiment'] == sentiment
    filtered_df = new_df[sentiment_mask]

    # clear matplotlib canvas
    plt.clf()
    plt.cla()

    # change color base on sentiment
    if sentiment == "positive":
        plot_color = "mediumseagreen"
    elif sentiment == "negative":
        plot_color = "crimson"

    # plot a bar chart
    most_appeared = get_word_count(filtered_df, 30)
    y_pos = np.arange(len(most_appeared.keys()))
    plt.barh(y_pos, most_appeared.values(), color=plot_color)
    plt.yticks(y_pos, most_appeared.keys())
    plt.xticks(np.arange(0, max(most_appeared.values())+1, 1.0))
    plt.title('Most Common Words in {sen} review_titles for {brand}'
              .format(brand=brand, sen=sentiment))
    plt.tight_layout()
    # create a new directory 'images' if it doesn't exist
    if not os.path.exists("images"):
        os.mkdir("images")
    path_name = "images/{sen}_{brand}_most_fre_words_bar.png"\
                .format(brand=brand, sen=sentiment)
    plt.savefig(path_name)
    plt.close()


def main():
    nespresso_df = pd.read_csv('nespresso_reviews.csv')
    keurig_df = pd.read_csv('keurig_reviews.csv')
    mr_coffee_df = pd.read_csv('mr_coffee_reviews.csv')

    plot_rating_histogram(nespresso_df, "Nespresso")
    plot_rating_histogram(keurig_df, "Keurig")
    plot_rating_histogram(mr_coffee_df, "Mr Coffee")

    plot_most_freq_words_bar(nespresso_df, "Nespresso")
    plot_most_freq_words_bar(keurig_df, "Keurig")
    plot_most_freq_words_bar(mr_coffee_df, "Mr Coffee")

    # not working
    plot_most_freq_words_sentiment_bar(nespresso_df, "Nespresso", "positive")
    plot_most_freq_words_sentiment_bar(nespresso_df, "Nespresso", "negative")
    plot_most_freq_words_sentiment_bar(keurig_df, "Keurig", "positive")
    plot_most_freq_words_sentiment_bar(keurig_df, "Keurig", "negative")
    plot_most_freq_words_sentiment_bar(mr_coffee_df, "Mr Coffee", "positive")
    plot_most_freq_words_sentiment_bar(mr_coffee_df, "Mr Coffee", "negative")


if __name__ == '__main__':
    main()