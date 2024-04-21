import demo.MediaCrawler.config as config
import demo.MediaCrawler.db as db
from demo.MediaCrawler.base.base_crawler import AbstractCrawler
from demo.MediaCrawler.media_platform.bilibili import BilibiliCrawler
from demo.MediaCrawler.media_platform.douyin import DouYinCrawler
from demo.MediaCrawler.media_platform.kuaishou import KuaishouCrawler
from demo.MediaCrawler.media_platform.weibo import WeiboCrawler
from demo.MediaCrawler.media_platform.xhs import XiaoHongShuCrawler
from typing import List

class CrawlerFactory:
    CRAWLERS = {
        "xhs": XiaoHongShuCrawler,
        "dy": DouYinCrawler,
        "ks": KuaishouCrawler,
        "bili": BilibiliCrawler,
        "wb": WeiboCrawler
    }

    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            raise ValueError("Invalid Media Platform Currently only supported xhs or dy or ks or bili ...")
        return crawler_class()

async def crawl_search(count: int, keywords: str, enable_comments: bool):

    # init db
    if config.SAVE_DATA_OPTION == "db":
        await db.init_db()

    crawler = CrawlerFactory.create_crawler(platform="wb")
    crawler.init_config(
        platform="wb",
        login_type="cookie",
        crawler_type='search',
        set_enable_comments=enable_comments,
    )
    crawler.set_crawler_max_notes_count(count)
    crawler.set_keywords(keywords)
    await crawler.start()

    if config.SAVE_DATA_OPTION == "db":
        await db.close()

async def crawl_specified(note_list:List[str],enable_comments: bool):
    print("*****")
    print(type(note_list))
    print("*****")
    # specified_list = list()
    # specified_list.append(note_list)
    specified_list = note_list.split(",")

    # init db
    if config.SAVE_DATA_OPTION == "db":
        await db.init_db()

    crawler = CrawlerFactory.create_crawler(platform="wb")
    crawler.init_config(
        platform="wb",
        login_type="cookie",
        crawler_type='detail',
        set_enable_comments=enable_comments,
    )
    crawler.set_specified_id_list(specified_list)
    await crawler.start()

    if config.SAVE_DATA_OPTION == "db":
        await db.close()