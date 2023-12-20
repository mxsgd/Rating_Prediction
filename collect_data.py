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
            'https://www.goodreads.com/book/show/44767458/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.dzn2KcfMTbv4_Y7J--YkzQ","after":"NjAwMDEsMTYzNjg3NDUwNjMxNw"}',
            'https://www.goodreads.com/book/show/55399/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.bVFjnLUaYZbgd7ppmo2S5g","after":"MjUwNTUsMTMzNTM5MDEwMjAwMA"}',
            'https://www.goodreads.com/book/show/459064/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.XL4DGHje60hBMPhwzS3OZA","after":"NTIwMCwxNTE4NjE5MzE3MjI0"}',
            'https://www.goodreads.com/book/show/478951/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.lhpPtHaXDWoLQTXBi3tyZg","after":"NjI5MSwxNjc5MzE3MzgzODU2"}',
            'https://www.goodreads.com/book/show/4703427/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.P7Fw0KWZn_TorWeK5Cy6_Q","after":"NDkyOSwxNTI5Nzg2MTAyODcx"}',
            'https://www.goodreads.com/book/show/5038/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.xT2pU_2LCIg9CzBZUKIDSw","after":"OTEyLDEyNTc5MjM2MjIwMDA"}',
            'https://www.goodreads.com/book/show/22328546/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.jQtH0YcfXnYWUle7dEhYeA","after":"NjAwMDEsMTU1MTk4NDUzOTI4NA"}',
            'https://www.goodreads.com/book/show/35072205/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.SXYwnQBcOPvCdhIw-p8_PA","after":"MTk1ODUsMTQ5OTM2OTE2NTk1OA"}',
            'https://www.goodreads.com/book/show/27188596/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.Lw7D3OzGTC0oCrznMOb6sQ","after":"MjUyNDgsMTUxMDkyMTgzMTAwMA"}',
            'https://www.goodreads.com/book/show/958263/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.5YZmsJfwTsEtfngLIBxKJQ","after":"MTMzMDMsMTU5MDg1ODExMDIxOQ"}',
            'https://www.goodreads.com/book/show/6324600/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.GcSdxtHaCFImDWj7DJSxxw","after":"NDkwNiwxMzMyMzMwNzU3MDAw"}',
            'https://www.goodreads.com/book/show/2574850/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.BwjjpRX0K_X1mnm_8gNKCA","after":"NTkxNiwxMzMxODE1NTAxMDAw"}',
            'https://www.goodreads.com/book/show/12393909/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.es1aXWQIwNlxW-WDW4KUUA","after":"ODQzMywxMzQzNTgyMzQzMDAw"}',
            'https://www.goodreads.com/book/show/30814745/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.phxBhCRthn14XRv19xaQTw","after":"NDEwMiwxNDkzODMzMTkyNTMx"}',
            'https://www.goodreads.com/book/show/24379183/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.jR7rsqBmkrhXJn3H2rc-uQ","after":"MTUwMDUsMTQyMTcwNzc2NDAwMA"}',
            'https://www.goodreads.com/book/show/1344586/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.oOUT0u0z-0tDxyr29r9CwA","after":"MjYwMSwxNjEzMjczNDI2MzYx"}',
            'https://www.goodreads.com/book/show/6330164/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.4GOu4zY-IIt23LIY4biYGA","after":"NDAxLDE1Nzk5MTA2MTU0NTQ"}',
            'https://www.goodreads.com/book/show/17152891/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.j9M69oare1fE0HmYOwtVWg","after":"MzYyMCwxNDIzNTQ1MDY1MDAw"}',
            'https://www.goodreads.com/book/show/54594933/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v3.8BjVsul4cWU6-zZx","after":"MTY3MDEsMTYwMTI5NzI1NzcxMg"}',
            'https://www.goodreads.com/book/show/32616656/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.LYZB0vmEZhNowOhWLMzh0Q","after":"MTYyMCwxNjk3NzYxMjU0MzMz"}'
            ]

for url in url_list:
    collect_data(url)