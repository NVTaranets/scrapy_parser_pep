# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from collections import defaultdict
from datetime import datetime

from pep_parse.constants import BASE_DIR, DATA_TIME_FORMAT, OUTPUT_DIR

# from itemadapter import ItemAdapter


class PepParsePipeline:

    def open_spider(self, spider):
        self.counts = defaultdict(int)
        self.total = 0

    def process_item(self, item, spider):
        self.counts[item['status']] += 1
        self.total += 1
        return item

    def close_spider(self, spider):
        time = datetime.now().strftime(DATA_TIME_FORMAT)
        print(BASE_DIR)
        with open(
            f'{OUTPUT_DIR}/status_summary_{time}.csv',
            mode='w',
            encoding='utf-8'
        ) as f:
            f.write('Статус,Количество\n')
            for status, count in self.counts.items():
                f.write(f'{status},{count}\n')
            f.write(f'Total,{self.total}\n')
