"""
This program scrapes our source URLs, extracts the first 10 pages of customer
review data of coffee maker products from Amazon, cleans the extracted data,
and writes the scraped data into datasets for later data analysis.
"""

import requests
from bs4 import BeautifulSoup


def write_csv(file_name, first, second):
    """
    Takes a string 'file_name' for the csv name, a string 'first' representing
    the first part of the URL, a string 'second' representing the second
    part of the URL.
    Extracts the first 10 pages of customer review (sorted by top reviews)
    information (review_date, rating, helpful_vote, review_title, review_body),
    cleans the text data, and writes the scraped data into a csv file
    named 'file_name.csv`.
    """

    f = open(file_name, "w")

    headers = "review_date,rating,helpful_vote,review_title,review_body\n"
    f.write(headers)

    for p in range(1, 11):
        url = first + str(p) + second + str(p)
        header = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X'
                                 '10_14_6) AppleWebKit/537.36 (KHTML,'
                                 'like Gecko) Chrome/98.0.4758.80 Safari/'
                                 '537.36'), 'referer': url}

        # response.status_code is 200 if Amazon didn't block it
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')

        reviews = soup.find_all('div', {'data-hook': 'review'})

        for item in reviews:
            review_date = item.find('span', {'data-hook': 'review-date'})\
                          .text.replace('Reviewed in the United States on ',
                                        '').strip()
            rating = item.find('i',
                               {'data-hook':
                                'review-star-rating'}).text.replace(
                                    'out of 5 stars', '').strip()
            review_title = item.find('a', {'data-hook':
                                     'review-title'}).text.strip().lower()

            if item.find('span', {'data-hook':
                         'review-body'}).find('span').text\
                   .strip().lower() == "":
                review_body = item.find('span', {'data-hook':
                                        'review-body'}).text.strip().lower()
            else:
                review_body = item.find('span', {'data-hook':
                                        'review-body'}).find('span')\
                                  .text.strip().lower()

            if item.find('span', {'data-hook':
                                  'helpful-vote-statement'}) is None:
                helpful_vote = 0
            else:
                helpful_vote = item.find('span', {'data-hook':
                                         'helpful-vote-statement'})\
                                   .text.replace(' people found this helpful',
                                                 '').strip()

            if helpful_vote == "One person found this helpful":
                helpful_vote = 1

            f.write(review_date.replace(",", "") + "," + str(rating) + ","
                    + str(helpful_vote).replace(",", "") + ","
                    + review_title.replace(",", " ") + ","
                    + review_body.replace(",", " ")
                                 .replace('the media could not be loaded.',
                                          '').strip() + "\n")

    f.close()


def main():
    nespresso_first = ('https://www.amazon.com/'
                       'Nespresso-VertuoPlus-Espresso-DeLonghi-Aeroccino/'
                       'product-reviews/B01MTZ419O/'
                       'ref=cm_cr_getr_d_paging_btm_next_')
    nespresso_second = '?ie=UTF8&reviewerType=all_reviews&pageNumber='

    keurig_first = ('https://www.amazon.com/'
                    'Keurig-Single-Serve-K-Cup-Special/'
                    'product-reviews/B07J5FV7WS/'
                    'ref=cm_cr_arp_d_paging_btm_next_')
    keurig_second = '?ie=UTF8&reviewerType=all_reviews&pageNumber='

    mr_coffee_first = ('https://www.amazon.com/'
                       'Mr-Coffee-Espresso-Cappuccino-Barista/'
                       'product-reviews/B007K9OIMU/'
                       'ref=cm_cr_arp_d_paging_btm_next_')
    mr_coffee_second = '?ie=UTF8&reviewerType=all_reviews&pageNumber='

    write_csv("nespresso_reviews.csv", nespresso_first, nespresso_second)
    write_csv("keurig_reviews.csv", keurig_first, keurig_second)
    write_csv("mr_coffee_reviews.csv", mr_coffee_first, mr_coffee_second)


if __name__ == '__main__':
    main()