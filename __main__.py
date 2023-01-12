import get_categories
import get_products
from setlogging import logger
from utils import module_path
import os


if __name__ == '__main__':
    """Uncomment below two lines to use 'all_links.txt' file instead of get live categories from the site."""
    # with open(os.path.join(module_path, 'all_links.txt'), 'r') as myfile:
    #     all_links = myfile.read().splitlines()
    all_links = get_categories.main()

    logger.info('=' * 65)
    logger.info(f"Retrieving all product details from Green Image Tech")
    for url in all_links:
        get_products.main(url)
