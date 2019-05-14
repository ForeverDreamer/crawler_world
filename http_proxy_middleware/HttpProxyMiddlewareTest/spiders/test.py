# -*- coding: utf-8 -*-
import scrapy
import logging

logger = logging.getLogger("test spider")


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["103.243.24.223"]
    website_possible_httpstatus_list = [403]
    handle_httpstatus_list = [403]
    
    start_urls = (
        'http://127.0.0.1:8000/ct/ps',
    )

    def parse(self, response):
        if response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            logger.info("got page: %s" % response.body.decode('utf-8'))
            yield response.request
