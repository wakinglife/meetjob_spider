# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import csv
import datetime
from scrapy.exporters import CsvItemExporter

class JobSpiderPipeline:
    def open_spider(self, spider):
        self.f = open("./meet_job_scrapy.csv", mode='a', encoding='utf-8')
        csv.writer(self.f, delimiter='*')
        # salary_min是提供的薪資
        self.f.write(
            "'job_tag','title', 'company_name', 'salary_min', 'salary_max', 'salary_currency', 'salary_length', 'skills', 'job_description', 'link'")

    def close_spider(self, spider):
        if self.f:
            self.f.close()

    def process_item(self, item, spider):
        self.f.write(f"{item['job_tag']}*{item['job_title']}*{item['company_name']}*{item['salary_min']}*{item['salary_max']}*{item['salary_currency']}*{item['salary_length']}*{item['skill_cata_tag']}*{item['jd']}*{item['url']}")
        return item


class CsvPipeline:
    def __init__(self):
        self.file = open(f'meet_job_{str(datetime.date.today())}.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
