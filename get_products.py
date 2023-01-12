import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import traceback
from setlogging import logger
from utils import module_path, clean_list


def get_product_info(soup):
    product_info = soup.find('div', 'product-info')
    product_title = product_info.find('h2', 'product_title').text.strip()
    product_category = product_info.find('span', 'product-category').text.strip()
    product_details_list = product_info.find(
        'div', 'woocommerce-product-details__short-description short-description').ul.text.split(
        "\n")
    product_details_list = clean_list(product_details_list)
    df_product_info = pd.DataFrame(
        {
            'product_title': product_title,
            'product_category': product_category,
            'product_details_list': [product_details_list]
            })
    return df_product_info


def get_specs(soup):
    df_specs = pd.read_html(str(soup.find('div', 'woocommerce-tabs wc-tabs-wrapper').table))[0]
    df_specs = df_specs.transpose()
    df_specs.columns = df_specs.iloc[0]
    df_specs = df_specs[1:]
    return df_specs


def get_data(URL):
    res = requests.get(URL)
    soup = BeautifulSoup(res.content, 'html.parser')

    df_product_info = get_product_info(soup)
    df_specs = get_specs(soup)

    data_json = json.dumps(
        {'URL': URL,
         'product_info': df_product_info.to_dict('records'),
         'specifications': df_specs.to_dict('records')
         }, ensure_ascii=False)
    return data_json


def save_to_json(data_json):
    URL = json.loads(data_json)['URL']
    product_title = json.loads(data_json)['product_info'][0]['product_title']
    product_category = json.loads(data_json)['product_info'][0]['product_category']

    url_subdir_list = clean_list(URL.split('/shop/')[1].split('/'))
    if url_subdir_list[-1].lower().replace(' ', '-').replace('_', '-').strip() \
            == product_title.lower().replace(' ', '-').replace('_', '-').replace('/', '-').strip():
        url_subdir_list.pop()

    data_subdir = os.path.join(module_path, 'data_json', '/'.join(url_subdir_list))
    if not os.path.exists(data_subdir):
        os.makedirs(data_subdir)

    with open(os.path.join(data_subdir, f"{product_title}.json"), 'w') as output_file:
        output_file.write(data_json)
        output_file.flush()

    return data_subdir


def main(URL):
    logger.info('-' * 65)
    try:
        data_json = get_data(URL)
        logger.info(f"Sucessfully retrieved data from {URL}")
    except:
        logger.error(f"Failed to get data from {URL}, exception printed below for reference")
        traceback.print_exc()
        exit(1)

    """Uncomment below codes if you would like a physical JSON file on your directory"""
    try:
        data_location = save_to_json(data_json)
        logger.info(f'Successfully saved data at: {data_location}')
    except:
        logger.error(f'Failed to save data, exception printed below for reference')
        traceback.print_exc()
        exit()


if __name__ == "__main__":
    url_list = ["https://www.greenimagetech.com/shop/strip-lights/led-neon/gs-neox/",
                "https://www.greenimagetech.com/shop/strip-lights/led-neon/gs-neos-0612/"]

    for url in url_list:
        main(url)
