import scrapy
from job_spider.items import JobSpiderItem

class MeetJobSpider(scrapy.Spider):

    name = "meet_job"
    job_list = ['軟體工程師', '網站工程師', '後端工程師', '前端工程師',
                'Mobile%20App%20工程師', '軟體測試工程師', 'DevOps%20%2F%20SRE%20工程師', '雲端%20%2F%20系統架構',
                '資料科學%20%2F%20人工智慧', '資訊安全工程師', '韌體%20%2F%20嵌入式工程師', '硬體工程師',
                '機構%20%2F%20熱流工程師', '產品%20%2F%20專案管理', 'UI%20%2F%20UX%20設計師', '工業設計師',
                '平面設計師', '視覺設計師', '商務營運', '業務%20%2F%20商務開發',
                '客戶管理', '客戶服務', '合作夥伴管理', '商業分析%20%2F%20商業研究',
                '顧問', '行銷相關', '數位行銷', '社群行銷',
                '內容行銷', '品牌%20%2F%20策略行銷', '實體廣告%20%2F%20活動', '公關行銷',
                '人力資源相關', '財務相關', '法務相關', '行政總務']
    job_name_list = ['軟體工程師', '網站工程師', '後端工程師', '前端工程師',
                    'Mobile App 工程師', '軟體測試工程師', 'DevOps / SRE 工程師', '雲端 / 系統架構',
                    '資料科學 / 人工智慧', '資訊安全工程師', '韌體 / 嵌入式工程師', '硬體工程師',
                    '機構 / 熱流工程師', '產品 / 專案管理', 'UI / UX 設計師', '工業設計師',
                    '平面設計師', '視覺設計師', '商務營運', '業務 / 商務開發',
                    '客戶管理', '客戶服務', '合作夥伴管理', '商業分析 / 商業研究',
                    '顧問', '行銷相關', '數位行銷', '社群行銷',
                    '內容行銷', '品牌 / 策略行銷', '實體廣告 / 活動', '公關行銷',
                    '人力資源相關', '財務相關', '法務相關', '行政總務']

    # allowed_domains = ["meet.jobs/zh-TW"]
    front_url = 'https://meet.jobs/zh-TW/jobs?page='
    page_num = 1
    skill_num = 0
    tail_url = '&order=update'
    extra_selection = '&job_functions=' + job_list[skill_num]
    start_urls = [front_url + str(page_num) + tail_url + extra_selection]
    end_page = 0

    def parse(self, response):
        #print(response.request.url)
        urls = response.xpath("//div[@class='job-card card']/a/@href").getall()
        share_path = "https://meet.jobs"
        if len(urls) == 0:
            self.end_page = 1
        if self.skill_num == 0:
            current_job = dict()
            current_job['job_name'] = self.job_name_list[0]
        else:
            current_job = dict()
            current_job['job_name'] = response.meta['job_name']
        for url in urls:
            if url.split('/')[2] == 'jobs':
                job_item = JobSpiderItem()
                job_item['url'] = share_path + url
                yield scrapy.Request(
                    url=share_path + url,
                    method='get',
                    callback=self.parse_get_detail_job,
                    meta={'job_name': current_job['job_name']}
                )

        self.page_num += 1
        if self.end_page == 0:
            yield scrapy.Request(
                url=self.front_url + str(self.page_num) + self.tail_url + self.extra_selection,
                method='get',
                callback=self.parse,
                meta={'job_name': current_job['job_name']}
            )
        else:
            self.end_page = 0
            if self.skill_num < len(self.job_list) - 1:
                self.page_num = 1
                self.skill_num += 1
                self.extra_selection = '&job_functions=' + self.job_list[self.skill_num]
                yield scrapy.Request(
                    url=self.front_url + str(self.page_num) + self.tail_url + self.extra_selection,
                    method='get',
                    callback=self.parse,
                    meta={'job_name': self.job_name_list[self.skill_num]}
                )
            else:
                print("finish crawling")

    def parse_get_detail_job(self, response):
        # 公司、職缺
        job_package = JobSpiderItem()
        job_package['job_tag'] = response.meta['job_name']

        jobtitle = response.xpath("//h1/text()").getall()[0].split('｜')[0]
        print(jobtitle)
        try:
            job_title = jobtitle.split('-')[0].strip()
            company_name = jobtitle.split('-')[1].strip()
        except:
            company_name = jobtitle.strip()
        try:
            salary = response.xpath("//div[@class='job-intro block']/div[@class='prices']/h2/text()").getall()[0]
        except:
            salary = 'unknown'
        skill_cata_tag = response.xpath("//div[@class='job-intro block']//div[@class='tag-box smallest-text']/text()").getall()
        skill_cata_tag = self.data_cleaning(skill_cata_tag)
        jd = response.xpath("//div[@class='from-editor']//p/text()").getall()
        jd = self.data_cleaning(jd)
        job_package['job_title'] = job_title
        job_package['company_name'] = company_name
        job_package['salary'] = salary
        job_package['skill_cata_tag'] = skill_cata_tag
        job_package['jd'] = jd
        job_package['url'] = response.url
        yield job_package

    def data_cleaning(self, list_of_item):
        output = ''
        for item in list_of_item:
            if output == '':
                output = item
            elif item.strip() != '':
                output = output + '|||' + item.strip()
        return output.replace(u'\xa0', u'')

