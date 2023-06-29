# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import csv
import datetime
from scrapy.exporters import CsvItemExporter
import pytz
from datetime import datetime, date
utc_now = datetime.now(pytz.utc)
utc8 = pytz.timezone('Asia/Taipei')

# 轉換為 UTC+8 時間
utc8_now = utc_now.astimezone(utc8)

# 提取日期部分
utc8_date = utc8_now.date()
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
        self.file = open(f'meet_job_{str(utc8_date)}.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


import sqlite3


class SqliteNoDuplicatesPipeline:

    def __init__(self):

        ## Create/Connect to database
        self.con = sqlite3.connect(f'meet_job_spider_{utc8_date}.db')

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()

        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes(
            job_title TEXT,
            job_tag TEXT,
            company_name TEXT,
            salary_max INTEGER,
            salary_min INTEGER,
            salary_currency TEXT,
            salary_length TEXT,
            skill_cata_tag TEXT,
            job_description TEXT,
            link TEXT,
            create_date_utc8 TEXT
        )
        """)

    def process_item(self, item, spider):

        ## Check to see if text is already in database
        self.cur.execute("select * from quotes where job_title = ?", (item['job_title'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['job_title'])

        ## If text isn't in the DB, insert data
        else:

            ## Define insert statement
            self.cur.execute("""
                INSERT INTO quotes (job_title, job_tag, company_name, salary_max, salary_min, salary_currency, salary_length, skill_cata_tag, job_description, link, create_date_utc8) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?) 
            """,
                             (
                                 item['job_title'],
                                 item['job_tag'],
                                 item['company_name'],
                                 item['salary_max'],
                                 item['salary_min'],
                                 item['salary_currency'],
                                 item['salary_length'],
                                 item['skill_cata_tag'],
                                 item['jd'],
                                 item['url'],
                                 utc8_date

                             )
            )

            ## Execute insert of data into database
            self.con.commit()

        return item