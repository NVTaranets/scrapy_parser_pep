import csv
from collections import defaultdict
from datetime import datetime

from pep_parse.constants import BASE_DIR, DATA_TIME_FORMAT, OUTPUT_SUB_DIR

RESULT_DIR = BASE_DIR / OUTPUT_SUB_DIR


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
        RESULT_DIR.mkdir(exist_ok=True)
        # file_name = RESULT_DIR / f'status_summary_{time}.csv'
        file_name = f'results/status_summary_{time}.csv'
        with open(
            file_name,
            mode='w',
            encoding='utf-8',
            newline=''
        ) as f:
            writer = csv.writer(f)
            writer.writerow(('Статус', 'Количество'))
            writer.writerows(self.counts.items())
            writer.writerow(('Total', self.total))
