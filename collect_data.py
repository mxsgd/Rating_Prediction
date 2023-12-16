import requests
from bs4 import BeautifulSoup
import json
import re
url = 'https://www.goodreads.com/book/show/41564599/reviews?reviewFilters={"workId":"kca://work/amzn1.gr.work.v1.vXTxKZhU-Xgu4w5oXz87zg","after":"MzA1MCwxNjkxNjMwNDEyODQ2"}'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

script_tag = soup.find('script', id='__NEXT_DATA__')

print(type(script_tag))
if script_tag:
    script_text = script_tag.text

    try:
        json_data = json.loads(script_text)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
else:
    print("Script tag with id '__NEXT_DATA__' not found.")
reviews_data = json_data['props']['pageProps']['apolloState']



reviews = []
sum = 0
for edge in reviews_data:
    match = re.match('^Review.*', edge)
    if match:
        append_dict = {"text": str(reviews_data[edge]['text']), "ratings": str(reviews_data[edge]['rating'])}
        reviews.append(append_dict)
print(reviews[1])