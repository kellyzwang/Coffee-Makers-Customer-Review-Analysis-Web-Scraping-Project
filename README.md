# Coffee Makers Customer Review Analysis

## Getting Started
To set up for this project locally, you will need libraries pandas, matplotlib, seaborn, numpy, plotly, requests, BeautifulSoup, nltk, Kaleido.

More detailed example instructions for installations are documented as following:


###### Installing pandas, matplotlib, seaborn, numpy, plotly for data processing and visualizations
```
pip3 install pandas
pip3 install matplotlib
pip3 install seaborn
pip3 install numpy
pip3 install plotly
```

###### Installing requests and BeautifulSoup for web scraping
```
pip3 install requests
pip3 install beautifulsoup4
```

###### Installing nltk for stop words
```
pip3 install nltk
```

###### Installing Kaleido for exporting static images for plotly figures
```
pip3 install -U kaleido
```

## To Download our Datasets
To obtain datasets, run `write_csv.py`. This program works with web scraping, extracts the first 10 pages of customer
review data of the three coffee maker products from Amazon, cleans the extracted data,
and writes the scraped data into three datasets in CSV format:
1. nespresso_review.csv
2. keurig_review.csv
3. mr_coffee_review.csv


## To Reproduce our Results
Running `question_1.py`, `question_2.py`, and `question_3.py` should generate all the data visualizations in the `images` folder.

### Notes
If you get the error `NLTK stop words not found`, try to download the stop words after installing nltk.
```
nltk.download('stopwords')
```
