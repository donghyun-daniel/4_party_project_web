from sentiment_predict import sentimentAnalysis
from clustering_test import keywordCluster as clusterTest
from clustering_train import keywordCluster as clusterTrain
from datapreprocessingpipeline_keyword import preprocessing
import itertools
from nlp_proj.models import UploadFile
from nlp_proj.models import CategoryData_17
from nlp_proj.models import CategoryData_8
from nlp_proj.models import ResultData_17
from nlp_proj.models import ResultData_8
from nlp_proj.models import RawData
import django
from django.core.wsgi import get_wsgi_application
import csv
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'nlp.settings'
django.setup()


application = get_wsgi_application()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ModelTrainHandler():
    def __init__(self, url):
        super().__init__()
        self.data = pd.read_csv(url)

    def preprocess(self):
        pre_data = preprocessing(self.data)
        return pre_data

    def cluster(self, data):
        categories = clusterTrain(data)
        for idx, category in enumerate(categories):
            for i in range(len(category)):
                if idx == 0:
                    CategoryData_8(title=category[i][0], first=category[i][1],
                                   second=category[i][2], third=category[i][3]).save()
                else:
                    CategoryData_17(
                        title=category[i][0], first=category[i][1], second=category[i][2], third=category[i][3]).save()
        # categories[0] = cluster8 형식 : [[cluster1 category name, c1 top1, c1 top2, c1 top3],
        #                                   [c2 category name, c2 top1, c2 top2, c2 top3] ..... [c8 category....]]
        # categories[1] = cluster17 형식은 동일

    def handle(self):
        pre_data = self.preprocess()
        self.cluster(pre_data)


class ModelTestHandler():
    def __init__(self):
        super().__init__()
        # 기홍님 확인하실 것 !
        # url 에서 Data 받아오는 부분은 web main page에서 넘겨받기
        files = UploadFile.objects.all().values()
        url = "/home/ubuntu/4_party_project/nlp/media/"
        self.data = pd.read_csv(os.path.join(url, files[0]['file']))
        # url = "model/raw/big_test.csv"
        # self.data = pd.read_csv(url)
        cols = list(self.data.columns)
        for i in range(len(self.data)):
            RawData(id=i, HotelName=self.data[cols[0]][i], HotelAddress=self.data[cols[1]][i], HotelRating=self.data[cols[2]][i], ReviewDate=self.data[cols[3]]
                    [i], ReviewRating=self.data[cols[4]][i], ReviewTitle=self.data[cols[5]][i], ReviewText=self.data[cols[6]][i]).save()

    def preprocess(self):
        pre_data = preprocessing(self.data)
        # pre_data.to_csv("preprocess.csv", sep=',')
        return pre_data

    def cluster(self, data):
        cluster_data = clusterTest(data)
        return cluster_data

    def sentimentprocess(self, data, category):
        results = sentimentAnalysis(data, category)
        return results

    def handle(self):
        category_8 = CategoryData_8.objects.values('title')
        category_17 = CategoryData_17.objects.values('title')
        category_8 = pd.DataFrame(category_8)
        category_8 = category_8['title'].values.tolist()
        category_17 = pd.DataFrame(category_17)
        category_17 = category_17['title'].tolist()
        categories = [category_8, category_17]
        print(categories[0])
        # 데이터 전처리
        pre_data = self.preprocess()

        # 기홍님 확인하실 것 !
        # train 에서 저장한 category8, 17 불러오기
        # categories = [[], []] <= 이렇게 만들어놓으시면 내부 연결은 추후 작업
        # 위에서처럼 8, 17 클러스터에 대해서 각각 담아줄 것
        cluster_data = self.cluster(pre_data)

        results = self.sentimentprocess(cluster_data, categories)
        # text,category,sentiment,rawid
        for idx, result in enumerate(results):
            for item in result:
                RawID = int(item[3])
                _raw = RawData.objects.get(id=RawID)
                if idx == 0:
                    ResultData_8(text=item[0], category=item[1], sentiment=item[2],
                                 date=_raw.ReviewDate, raw_text=_raw.ReviewText).save()
                else:
                    ResultData_17(text=item[0], category=item[1], sentiment=item[2],
                                  date=_raw.ReviewDate, raw_text=_raw.ReviewText).save()
        # results[0] = cluster 8
        # results[1] = cluster 17
