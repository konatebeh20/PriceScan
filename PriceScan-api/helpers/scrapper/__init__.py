# -*- coding: utf-8 -*-
"""
Package de scraping pour PriceScan
"""

from .carrefour import scrape_carrefour
from .kedjenou import scrape_kedjenou
from .afrikmall import scrape_afrikmall
from .bazart import scrape_bazart
from .jumia import scrape_jumia
from .utils import fetch_page, clean_price

__all__ = [
    'scrape_carrefour',
    'scrape_kedjenou',
    'scrape_afrikmall',
    'scrape_bazart',
    'scrape_jumia',
    'fetch_page',
    'clean_price'
]
