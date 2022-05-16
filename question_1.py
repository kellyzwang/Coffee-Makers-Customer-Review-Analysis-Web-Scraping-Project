"""
This program works with three coffee maker product customer review datasets,
processes data, and implements functions that create data visualizations
needed to answer the first research question: Is there a correlation between
the number of helpful votes and rating? Do people find negative reviews or
positive reviews more helpful?
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

import question_3


def helpful_votes_vs_rating(df, brand, product_name):
    """
    Takes a coffee maker product review dataframe 'df', a string
    'brand', and a string 'product_name' as parameters.
    Plots a scatterplot that compares the rating against the
    number of helpful votes for the 'brand' coffee maker.
    Creates and a new directory 'images' if it doesn't exist and save
    the plot in the 'images' folder.
    """
    # plotting
    sns.relplot(data=df, x="helpful_vote", y="rating")
    plt.title('{} Helpful Votes vs Ratings'.format(product_name))
    plt.xlabel('Helpful Votes')
    plt.ylabel('Ratings')

    # create a new directory 'images' if it doesn't already exist
    if not os.path.exists("images"):
        os.mkdir("images")
    path_name = "images/{}_helpful_votes_rating_scatplt.png".format(brand)
    plt.savefig(path_name)


def compare_helpfulness(df, brand, product_name):
    """
    Takes a coffee maker product review dataframe 'df', a string
    'brand', and a string 'product_name' as parameters.
    Plots a bar chart that displays the total number of helpful votes
    that each sentiment category has for the 'brand' coffee maker.
    Creates and a new directory 'images' if it doesn't exist and save
    the plot in the 'images' folder.
    """
    # data manipulation
    new_df = question_3.add_sentiment(df)
    total_sen_votes_df = new_df.groupby('sentiment')['helpful_vote']\
        .sum().to_frame()
    total_sen_votes_df.reset_index(inplace=True)

    # plotting
    sns.barplot(data=total_sen_votes_df, x="sentiment", y="helpful_vote")
    plt.title('{} Helpful Votes Across Sentiment'.format(product_name))
    plt.xlabel('Sentiment')
    plt.ylabel('Helpful Votes')

    # create a new directory 'images' if it doesn't already exist
    if not os.path.exists("images"):
        os.mkdir("images")
    path_name = "images/{}_helpful_votes_senti_barplt.png".format(brand)
    plt.savefig(path_name)


def main():
    nespresso_df = pd.read_csv('nespresso_reviews.csv')
    keurig_df = pd.read_csv('keurig_reviews.csv')
    mr_coffee_df = pd.read_csv('mr_coffee_reviews.csv')

    helpful_votes_vs_rating(nespresso_df, "Nespresso", "Nespresso Vertuo Plus")
    helpful_votes_vs_rating(keurig_df, "Keurig", "Keurig K-Cafe")
    helpful_votes_vs_rating(mr_coffee_df, "Mr Coffee",
                            "Mr Coffee Cafe Barista")

    compare_helpfulness(nespresso_df, "Nespresso", "Nespresso Vertuo Plus")
    compare_helpfulness(keurig_df, "Keurig", "Keurig K-Cafe")
    compare_helpfulness(mr_coffee_df, "Mr Coffee", "Mr Coffee Cafe Barista")


if __name__ == '__main__':
    main()