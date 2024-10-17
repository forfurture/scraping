import os
import time

import requests
from bs4 import BeautifulSoup

BASE_DIR = "everyspec.com"
BASE_URL = 'http://everyspec.com'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36'
}


def download_pdf(pdf_links):
    download_links = []
    for link in pdf_links:
        print(f'processing pdf {link}')
        data = requests.get(link, headers=HEADER, timeout=60)
        html = BeautifulSoup(data.content, 'html.parser')
        for button in html.find_all('button'):
            if button.text.startswith('Download'):
                download_links.append(button.attrs['onclick'][len('document.location.href=\''):-2])
    return download_links


def parse_links(html):
    links = []
    for link in html.find_all('a'):
        if link['href'].startswith('http://everyspec.com/MIL-') and 'class' not in link.attrs:
            links.append(link['href'])
    return links


def parse_mil_link_pages(link):
    page = 1
    total_links = []
    while True:
        print(f"{link}?page={page}  -- processing ")
        data = requests.get(f"{link}?page={page}", headers=HEADER, timeout=60)
        html = BeautifulSoup(data.content, 'html.parser')
        links = parse_links(html)
        if len(links) == 0:
            break
        page = page + 1
        time.sleep(1)
        total_links.extend(links)
    return total_links


def parse_mil_links(tag):
    data = requests.get(f"{BASE_URL}/{tag}", headers=HEADER, timeout=60)
    html = BeautifulSoup(data.content, 'html.parser')
    links = parse_links(html)
    pdf_links = []
    for link in links:
        tag_links = parse_mil_link_pages(link)
        pdf_links.extend(download_pdf(tag_links))
    return pdf_links


if __name__ == '__main__':
    # tag = 'MIL-HDBK'
    # tag_dir = os.path.join(BASE_DIR, tag)
    # os.makedirs(tag_dir, exist_ok=True)
    # links = parse_mil_links(tag)
    # with open(os.path.join(tag_dir, 'list.json'), 'w', encoding='utf-8') as f:
    #     data_to_write = '\n'.join(links)
    #     f.write(data_to_write)
    tag = 'MIL-PRF'
    tag_dir = os.path.join(BASE_DIR, tag)
    os.makedirs(tag_dir, exist_ok=True)
    links = parse_mil_links(tag)
    with open(os.path.join(tag_dir, 'list.json'), 'w', encoding='utf-8') as f:
        data_to_write = '\n'.join(links)
        f.write(data_to_write)
    tag = 'MIL-SPECS'
    tag_dir = os.path.join(BASE_DIR, tag)
    os.makedirs(tag_dir, exist_ok=True)
    links = parse_mil_links(tag)
    with open(os.path.join(tag_dir, 'list.json'), 'w', encoding='utf-8') as f:
        data_to_write = '\n'.join(links)
        f.write(data_to_write)
    tag = 'MIL-STD'
    tag_dir = os.path.join(BASE_DIR, tag)
    os.makedirs(tag_dir, exist_ok=True)
    links = parse_mil_links(tag)
    with open(os.path.join(tag_dir, 'list.json'), 'w', encoding='utf-8') as f:
        data_to_write = '\n'.join(links)
        f.write(data_to_write)
