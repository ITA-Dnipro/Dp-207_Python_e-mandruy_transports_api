import scrapy
from scrapy.http import FormRequest, Request
from datetime import datetime
import pytz
import json
from ..middlewares import RandomUserAgentMiddleware


class PoezdatoBlablacarsSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            (
                'scrapy.contrib.downloadermiddleware.'
                'useragent.UserAgentMiddleware'
                ): None,
            (
                RandomUserAgentMiddleware
            ): 400
        }
    }

    name = 'poezdato_blablacars'
    POEZDATO_API_PART_URL = 'https://poezdato.net/search/get-trips2?'
    start_urls = ["https://poezdato.net/"]

    def __init__(self, *args, **kwargs):
        self.departure_name = kwargs['departure_name'].lower().capitalize()
        self.departure_date = kwargs['departure_date']
        self.arrival_name = kwargs['arrival_name'].lower().capitalize()

    def parse(self, response):
        form_action_url = response.xpath(
            '//*/form[@id="dir"]/@action'
        ).get()
        #
        post_url = f'{response.url[:-1]}{form_action_url}'
        #
        form_data = {
            "dir_from": self.departure_name,
            "st_from_id": "",
            "dir_where": self.arrival_name,
            "st_where_id": "",
            "dir_date": self.departure_date,
            "dir_time_from": "",
            "dir_time_to": "",
            # "dir_long_distance": "0",
            "dir_long_distance": "1",
            # "dir_suburban": "0",
            "dir_suburban": "1",
            "dir_submit": "Найти"
        }
        yield FormRequest(
            post_url,
            callback=self.search_result_page,
            formdata=form_data
        )

    def search_result_page(self, response):
        cars_src = response.xpath(
            '//*/input[@id="cars_src"]/@value'
        ).get()
        cars_dst = response.xpath(
            '//*/input[@id="cars_dst"]/@value'
        ).get()
        cars_country = response.xpath(
            '//*/input[@id="cars_country"]/@value'
        ).get()
        cars_country_dst = response.xpath(
            '//*/input[@id="cars_country_dst"]/@value'
        ).get()
        cars_date = response.xpath(
            '//*/input[@id="cars_date"]/@value'
        ).get()
        # mobile = response.xpath(
        #     '//*/input[@id="mobile"]/@value'
        # ).get()
        notrains = '1'
        details = '1'
        #
        api_url = (
            f'{PoezdatoBlablacarsSpider.POEZDATO_API_PART_URL}'
            f'src={cars_src}&'
            f'dst={cars_dst}&'
            f'date={cars_date}&'
            f'country={cars_country}&'
            f'notrains={notrains}&'
            f'details={details}&'
            f'country_dst={cars_country_dst}'
        )
        yield Request(url=api_url, callback=self.api_responce_handler)

    def api_responce_handler(self, response):
        jsonresponse = json.loads(response.text)
        #
        kyiv_tz = pytz.timezone('Europe/Kiev')
        parsed_time = datetime.now(tz=kyiv_tz).strftime("%d-%m-%Y %H:%M:%S")
        #
        result_dict = {}
        if jsonresponse['result'] is False:
            result_dict['result'] = False
            result_dict['error_code'] = jsonresponse['error_code']
        else:
            result_dict['result'] = True
            result_dict['departure_name'] = self.departure_name
            result_dict['departure_date'] = self.departure_date
            result_dict['arrival_name'] = self.arrival_name
            result_dict['parsed_time'] = parsed_time
            result_dict['source_name'] = 'poezdato/blablacar'
            result_dict['source_url'] = jsonresponse['url']
            # result_dict['blablacar_trips_url'] = jsonresponse['url']
            result_dict['trips'] = []
            for t in jsonresponse['trips']:
                try:
                    car_model = t['car_model']
                except KeyError:
                    car_model = None
                result_dict['trips'].append(
                    {
                        'departure_name': t['src'],
                        'departure_date': t['departure'],
                        'arrival_name': t['dst'],
                        'price': t['price'],
                        'car_model': car_model,
                        'blablacar_url': t['link'],
                        'parsed_time': parsed_time,
                        'source_name': 'poezdato/blablacar',
                        'source_url': response.url,

                    }
                )
        yield result_dict
