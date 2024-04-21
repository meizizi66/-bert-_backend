import argparse
import asyncio
import sys

import MediaCrawler.config as config
import MediaCrawler.db as db
from MediaCrawler.base.base_crawler import AbstractCrawler
from MediaCrawler.media_platform.bilibili import BilibiliCrawler
from MediaCrawler.media_platform.douyin import DouYinCrawler
from MediaCrawler.media_platform.kuaishou import KuaishouCrawler
from MediaCrawler.media_platform.weibo import WeiboCrawler
from MediaCrawler.media_platform.xhs import XiaoHongShuCrawler
from demo.crawl_def import crawl_search, crawl_specified



asyncio.get_event_loop().run_until_complete(crawl_search(5,"华晨宇",False))
