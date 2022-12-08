import re
import ssl
from statistics import mean

import aiohttp
import certifi
from lxml import html
from pandas import read_excel

from .database import insert_data

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
)


async def scrape_data(values: list) -> list:
    prices = []
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=conn) as session:
        for value in values:
            async with session.get(
                value[1],
                headers={"User-Agent": USER_AGENT}
            ) as response:
                xpath = value[2]
                source_code = html.fromstring(await response.text())
                if not re.search(r'text\(\)$', xpath):
                    xpath += '/text()'
                list_of_elems = source_code.xpath(xpath)
                digits = re.findall(r'\d', list_of_elems[0])
                try:
                    result = int(''.join(digits))
                except ValueError:
                    prices.append(None)
                prices.append(result)
    return prices


async def read_excel_file(path: str) -> tuple[str, int]:
    df = read_excel(path)
    values = [df.columns.values.tolist()] + df.values.tolist()
    insert_data(values)
    prices = await scrape_data(values)
    mean_price = round(mean(prices), 2)
    return values, mean_price
