import os
from datetime import date, datetime
import time
from typing import Iterable
import webbrowser


module_path = os.path.dirname(os.path.abspath(__file__))

today = date.today().strftime("%Y%m%d")
starttime = time.time()
starttime_str = datetime.fromtimestamp(starttime).strftime('%Y%m%d %H:%M:%S')


def clean_list(input_list):
    ## removes empty strings and strips the items inside
    output_list = [item.strip() for item in input_list if item != '' and item is not None]
    return output_list


def clean_list_dict(input_list, original_URL):
    ## processes nested list-dict, removing duplicates and empty category_title
    output_list = [x for x in input_list
                   if x['category_title'] != ''
                   and 'read' not in x['category_title'].lower()
                   and x['url'] != original_URL
                   ]
    return [dict(t) for t in {tuple(d.items()) for d in output_list}]


def flatten_list_dict(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (dict, bytes)):
            for sub_x in flatten_list_dict(x):
                yield sub_x
        else:
            yield x


def open_html(html):
    if not isinstance(html, str):
        html = str(html)
    with open(f'{os.getcwd()}/test.html', 'w') as f:
        f.write(html)
        f.flush()

    webbrowser.open(f"file:///{f.name}")


def flatten_list(items):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten_list(x):
                yield sub_x
        else:
            yield x.strip()
