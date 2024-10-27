import os  # Make sure this is imported at the top
import requests
from bs4 import BeautifulSoup

def save_investment_content(link, save_function):
    res = requests.get(link)
    soup = BeautifulSoup(res.content, 'html.parser')
    soup = soup.select("div.content > div.row > div:nth-child(1)")
    text = [el.get_text() for el in soup]
    text = f'--------\n{link}\n---------\n'.join(text).replace("NEXT", "")

    # Ensure 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    file_name = f'data/{link.split("/")[-1]}.txt'
    save_function(file_name, text)

    return text

def save_file(file_name, text):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(text)
