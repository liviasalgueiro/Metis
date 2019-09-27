import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import urllib
import urllib.request


def list_of_links(url_master, url, class_name):
    """ This function returns a list with all the individual product links we will scrape later"""

    my_session = requests.session()
    cookies = ''
    while cookies == '':
        try:
            cookies = my_session.get(url_master).cookies
            break
        except:
            time.sleep(5)
            print("Trying a Connection...")
            continue

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    response = my_session.get(url, headers=headers, cookies=cookies)

    if response.status_code != 200:
        return "ERROR IN THE STATUS CODE, {}".format(response.status_code)
    else:
        page = response.text
        soup = BeautifulSoup(page, "lxml")
        list_url_links = [e['href'] for e in soup.find_all(class_=class_name)]
        list_no_duplicates = []
        [list_no_duplicates.append(x) for x in list_url_links if x not in list_no_duplicates]
        return list_no_duplicates


url_master = "http://www.bloomingdales.com"
class_name = "productDescLink"

product = "Dresses"  # for each category of clothing, we have to change that.

total_pages = range(1, 31)  # number of pages we want to scrape. Each page has 96 product labels.
final_list_of_url = []
for page in total_pages:
    # first, we check bloomingdale's website to see the url pattern for the product we're scraping:
    url = 'https://www.bloomingdales.com/shop/womens-apparel/designer-dresses/Pageindex/{}?id=21683'.format(page)
    time.sleep(1)

    for row in list_of_links(url_master, url, class_name):
        final_list_of_url.append(row)


def get_images_info(url_master, url):
    """ This function is responsible for accessing each url from the list we created using list_of_links function
    and scraping all the important information about the product in a dict format, as well as saving its image. """

    my_session = requests.session()
    cookies = ''
    while cookies == '':
        try:
            cookies = my_session.get(url_master).cookies
            break
        except:
            time.sleep(5)
            print("Try a Connection...")
            continue

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    response = my_session.get(url, headers=headers, cookies=cookies)

    if response.status_code != 200:
        return "ERROR IN THE STATUS CODE, {}".format(response.status_code)
    else:
        page = response.text
        soup = BeautifulSoup(page, "lxml")

        # Product Information:
        try:
            unavailable = soup.find(class_='unavailable-image-message').text
        except:
            unavailable = 0

        if unavailable == 0:
            web_id = url.split('ID=')
            web_id = web_id[1].split('&')[0]
            store = "Bloomingdale's"
            brand = soup.find(class_='brand-name-link product-title-no-transform h2 b-breakword').text.replace("\n",
                                                                                                               "").split()
            brand = " ".join(brand)

            price = soup.find('div', class_='price').text.replace("\n", "").split()
            price = " ".join(price)

            color = soup.find('span', class_='color-display-name').text.replace("\n", "").replace("Color: ", "").split()
            color = " ".join(color)

            name = soup.find('h1', class_='text c-no-bold product-title-no-transform b-breakword').text.replace("\n",
                                                                                                                "").split()
            name = " ".join(name)
            description = name

            product_type = soup.find(class_='breadcrumbs-panel no-bullet').text.replace("\n", "").split()[-1]

            headers = ['product_id', 'product_url', 'store', 'type', 'name', 'price', 'description', 'color', 'brand']
            product_dict = dict(zip(headers, [[web_id],
                                              [url],
                                              [store],
                                              [product_type],
                                              [name],
                                              [price],
                                              [description],
                                              [color],
                                              [brand]]))

            # Saving the image:
            img_url = soup.find("meta", property="og:image")["content"]
            urllib.request.urlretrieve(img_url, os.path.basename(web_id + ".jpg"))

            return product_dict


frames = []

for link in final_list_of_url:
    product_url = "https://www.bloomingdales.com{}".format(link)
    product_dict = get_images_info(url_master, product_url)
    df = pd.DataFrame.from_dict(product_dict)
    frames.append(df)

result = pd.concat(frames).reset_index(drop=True)
result.to_csv("bloomingdales_{}_pages{}-{}.csv".format(product, total_pages[0], total_pages[-1]))
