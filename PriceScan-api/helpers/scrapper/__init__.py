# -*- coding: utf-8 -*-
"""
Package de scraping pour PriceScan
"""

from .carrefour import scrape_carrefour
from .abidjanmall import scrape_abidjanmall
from .prosuma import scrape_prosuma
from .playce import scrape_playce
from .utils import fetch_page, clean_price

__all__ = [
    'scrape_carrefour',
    'scrape_abidjanmall', 
    'scrape_prosuma',
    'scrape_playce',
    'fetch_page',
    'clean_price'
]
