"""
This program works with three coffee maker product customer review
datasets, processes data, and implements functions that create data
visualizations needed to answer the second research question: When
do customers submit the most reviews? Do people submit more reviews
during the holiday season? How does customers’ sentiment (positive
review rate) change over time for each product?
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

import question_3


def customer_review_per_month(df, brand, product_name):
    """
    Takes a coffee maker product review dataframe 'df', a string
    'brand', and a string 'product_name' as parameters.
    Plots a bar chart that graphs the number of customer reviews
    submitted for each month of the year for the 'brand' coffee maker.
    Creates and a new directory 'images' if it doesn't exist and save
    the plot in the 'images' folder.
    """
    # data manipulation
    new_df = extract_month(df)
    group_month_df = new_df.groupby('review_month')['rating'].count()\
        .to_frame()
    group_month_df.reset_index(inplace=True)

    # plotting
    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November",
                   "December"]
    sns.barplot(data=group_month_df, x="review_month", y="rating",
                order=month_order)
    plt.title('{} Review Count by Month of Year'.format(product_name))
    plt.xlabel('Month of Review')
    plt.ylabel('Number of Reviews')
    plt.xticks(rotation=-45)

    # create a new directory 'images' if it doesn't already exist
    if not os.path.exists("images"):
        os.mkdir("images")
    path_name = "images/{}_review_count_by_month.png".format(brand)
    plt.savefig(path_name)


def positive_review_per_month(df, brand, product_name):
    """
    Takes a coffee maker product review dataframe 'df', a string
    'brand', and a string 'product_name' as parameters.
    Plots a point plot that graphs the change in positive review
    rate across each month of the year for the 'brand' coffee maker.
    Creates and a new directory 'images' if it doesn't exist and save
    the plot in the 'images' folder.
    """
    new_sen_df = question_3.add_sentiment(df)
    new_mon_df = extract_month(new_sen_df)
    # count total reviews by month
    total_sen_reviews_df = new_mon_df.groupby('review_month', as_index=False)\
        .count()
    total_sen_reviews_df = total_sen_reviews_df.loc[:, ['review_month',
                                                        'sentiment']]
    # count total reviews with sentiment 'positive' by month
    pos_count = {}
    for i in range(len(new_mon_df)):
        month = new_mon_df.loc[i, 'review_month']
        if month not in pos_count:
            pos_count[month] = 0
        if new_mon_df.loc[i, 'sentiment'] == 'positive':
            pos_count[month] += 1
    # calculate positive review rate
    pos_rate_list = []
    for i in range(len(total_sen_reviews_df)):
        curr_month = total_sen_reviews_df.loc[i, 'review_month']
        pos_rate_list.append(pos_count[curr_month] /
                             total_sen_reviews_df.loc[i, 'sentiment'] * 100)
    total_sen_reviews_df['positive_rate'] = pos_rate_list

    # plotting
    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November",
                   "December"]
    sns.catplot(data=total_sen_reviews_df, x="review_month", y="positive_rate",
                kind='point', order=month_order)
    plt.title('{} Positive Review Rate Over Time'.format(product_name))
    plt.xlabel('Month of Review')
    plt.ylabel('Positive Sentiment Rate')
    plt.xticks(rotation=-45)

    # create a new directory 'images' if it doesn't already exist
    if not os.path.exists("images"):
        os.mkdir("images")
    path_name = "images/{}_pos_senti_over_time.png".format(brand)
    plt.savefig(path_name)


def extract_month(df):
    """
    Takes a coffee maker product review dataframe 'df'.
    Extracts the month of each review's 'review_date'.
    Returns a new dataframe with an added "review_month" column.
    """
    new_df = df.copy()
    month_list = []

    for i in range(len(new_df['review_date'])):
        get_month = df['review_date'][i].split()[0]
        month_list.append(get_month)

    new_df['review_month'] = month_list
    return new_df


def main():
    nespresso_df = pd.read_csv('nespresso_reviews.csv')
    keurig_df = pd.read_csv('keurig_reviews.csv')
    mr_coffee_df = pd.read_csv('mr_coffee_reviews.csv')

    customer_review_per_month(nespresso_df, "Nespresso",
                              "Nesspress Vertuo Plus")
    customer_review_per_month(keurig_df, "Keurig", "Keurig K-Cafe")
    customer_review_per_month(mr_coffee_df, "Mr Coffee",
                              "Mr Coffee Cafe Barista")

    positive_review_per_month(nespresso_df, "Nespresso",
                              "Nesspress Vertuo Plus")
    positive_review_per_month(keurig_df, "Nespresso", "Nesspress Vertuo Plus")
    positive_review_per_month(mr_coffee_df, "Nespresso",
                              "Nesspress Vertuo Plus")


if __name__ == '__main__':
    main()