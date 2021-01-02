# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import pymysql
from openpyxl import load_workbook
import openpyxl


class GsespiderPipeline:
    # def __init__(self):


    def process_item(self, item, spider):
        db = pymysql.connect("localhost", "root", "goodxyl2021", "webdesign")
        cursor = db.cursor()
        GSE = item["GSE_num"]
        Status = item["Status"]
        Title = item["Title"]
        Organisms = item["Organism"]
        ExpType = item["ExperimentType"]
        Summary = item["Summary"]
        OverallDesign = item["OverallDesign"]
        Platform = item["Platform"]
        Sample = item["Samples"]
        # with open(r"C:\Users\QiTianM425\Desktop\scrapy.csv", 'a+', encoding='utf-8', newline="") as cf:
        #     w = csv.writer(cf)
        #     w.writerow([GSE, Status, Title, Organisms, ExpType, Summary, OverallDesign, Platform, Sample])
        cursor.execute("insert into gse ("
                       "GSE_num, Status, Title, Organism, Experiment_type, Summary, Overall_design, Platforms, Samples)"
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (GSE, Status, Title, Organisms, ExpType, Summary, OverallDesign, Platform, Sample))
        db.commit()
        db.close()
        return item
