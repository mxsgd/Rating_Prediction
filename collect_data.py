import requests
from bs4 import BeautifulSoup
import json
import re
import csv
from langdetect import detect

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

def collect_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    script_tag = soup.find('script', id='__NEXT_DATA__')
    reviews = []
    if script_tag:
        script_text = script_tag.text

        try:
            json_data = json.loads(script_text)
            reviews_data = json_data['props']['pageProps']['apolloState']
            for edge in reviews_data:
                match = re.match('^Review.*', edge)
                if match:
                    append_dict = {"text": str(reviews_data[edge]['text']),
                                   "rating": str(reviews_data[edge]['rating'])}
                    reviews.append(append_dict)
            english_reviews = [review for review in reviews if is_english(review['text'])]
            print(english_reviews)
            with open("data.csv", 'a', encoding="utf-8", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['text', 'rating'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for data in english_reviews:
                    writer.writerow(data)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print("Script tag with id '__NEXT_DATA__' not found.")



url_list = ['https://www.goodreads.com/book/show/41564599/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.vXTxKZhU-Xgu4w5oXz87zg","after":"MzA1MCwxNjkxNjMwNDEyODQ2"}',
            'https://www.goodreads.com/book/show/166997/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.UObYRrnlaBsTEG8a1Jju7w","after":"MzIxMzEsMTU3OTI3MjY1NjAxOA"}',
            'https://www.goodreads.com/book/show/40701780/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.1eNeCqjggj-dNnOHTIYOcA","after":"ODMwMSwxNjMzMTc0MjEwMzU5"}',
            'https://www.goodreads.com/book/show/676920/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.Lz1jO5oyGRM-u0MxCZv6iw","after":"NzE2LDE2MjkwNDczODUxODM"}',
            'https://www.goodreads.com/book/show/45974/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.mnUvzqUrsXiAvOjnYqO55Q","after":"MTc2MDAsMTQ2ODMzODk1NzAwMA"}',
            'https://www.goodreads.com/book/show/40121378/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.b-26D0ndpgC7ICmWDgP53Q","after":"MjE4NzksMTU5NTA4MTEzODI3MQ"}',
            'https://www.goodreads.com/book/show/55401/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v3.e0YfHlF9ZuI2jP2d","after":"ODg1OSwxNDg1NDcyMDQyMzIy"}',
            'https://www.goodreads.com/book/show/49552/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.Utz0fvS02P1YxyJHfysyFw","after":"NDQyMzUsMTU1ODgxMDY5OTA4MA"}',
            'https://www.goodreads.com/book/show/117833/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.Q4P9D2JWyAZxcOq0Bodrqg","after":"MzY1NDQsMTQzNzc0MzU4OTAwMA"}',
            'https://www.goodreads.com/book/show/944076/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.vwhpu8TX6P8c5v6VNhoqcA","after":"OTczMywxMzkzNDQ1OTQwMDAw"}',
            'https://www.goodreads.com/book/show/61535/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.HPrzMnLVNf2V-doX9Zf1CQ","after":"OTA2NywxNDU2MzQyMzY5MDAw"}',
            'https://www.goodreads.com/book/show/538871/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.RPVfi4E5JQYMUx9W7dbCgw","after":"NDEwMSwxNjM2MzkyNjIzNzMx"}',
            'https://www.goodreads.com/book/show/5129/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.Sm_a8GGh77Rw99ImSVfoTA","after":"MzU2MzksMTMyMTI0Mjk1NzAwMA"}',
            'https://www.goodreads.com/book/show/44767458/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.dzn2KcfMTbv4_Y7J--YkzQ","after":"NjAwMDEsMTYzNjg3NDUwNjMxNw"}'
            ]

for url in url_list:
    collect_data(url)