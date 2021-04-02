#from test import model
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse, redirect
import numpy as np
import pandas as pd
import os
from nlp.settings import BASE_DIR
import json
import math
import sys

from .forms import barChart
from .forms import UploadFileForm
from .models import ResultData_17
from .models import ResultData_8
from .models import CategoryData_17
from .models import CategoryData_8
from .models import UploadFile
from .models import RawData

p = os.path.abspath(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__))))+'/test'
sys.path.append(p)
# Create your views here.
import integrated_model

@csrf_exempt
def index(request):
    DBKeyword8 = CategoryData_8.objects.all().values()
    ResultData = pd.DataFrame(ResultData_8.objects.values())
    print(ResultData)
    ResultData = ResultData.drop(['id', 'raw_text'], axis=1)

    category_pos_cnt = ResultData.groupby("category").sum()
    category_total_cnt = ResultData.groupby("category").count()
    category_total_cnt["pos_cnt"] = category_pos_cnt["sentiment"]
    category_total_cnt["neg_cnt"] = category_total_cnt["sentiment"] - \
        category_total_cnt["pos_cnt"]

    category_total_cnt["pos_ratio"] = category_total_cnt["pos_cnt"] / \
        (category_total_cnt["pos_cnt"] + category_total_cnt["neg_cnt"])
    category_total_cnt["neg_ratio"] = category_total_cnt["neg_cnt"] / \
        (category_total_cnt["pos_cnt"] + category_total_cnt["neg_cnt"])

    category_total_cnt["pos_cnt_sqrt"] = category_total_cnt["pos_cnt"].apply(
        math.sqrt)
    category_total_cnt["neg_cnt_sqrt"] = category_total_cnt["neg_cnt"].apply(
        math.sqrt)

    scaling_val = max(
        category_total_cnt["pos_cnt_sqrt"] + category_total_cnt["neg_cnt_sqrt"])
    category_total_cnt["pos_cnt_sqrt_modified"] = category_total_cnt["pos_cnt_sqrt"] / \
        (scaling_val*8)
    category_total_cnt["neg_cnt_sqrt_modified"] = category_total_cnt["neg_cnt_sqrt"] / \
        (scaling_val*8)

    category_total_cnt["pos_cnt_sqrt_modified_normalized"] = (
        category_total_cnt["pos_cnt_sqrt_modified"] - category_total_cnt["pos_cnt_sqrt_modified"].mean()) / (category_total_cnt["pos_cnt_sqrt_modified"].std() * 50)
    category_total_cnt["neg_cnt_sqrt_modified_normalized"] = (
        category_total_cnt["neg_cnt_sqrt_modified"] - category_total_cnt["neg_cnt_sqrt_modified"].mean()) / (category_total_cnt["neg_cnt_sqrt_modified"].std() * 50)

    category_total_cnt["pos_ratio_calib"] = category_total_cnt["pos_ratio"] + \
        category_total_cnt["pos_cnt_sqrt_modified_normalized"]
    category_total_cnt["neg_ratio_calib"] = category_total_cnt["neg_ratio"] + \
        category_total_cnt["neg_cnt_sqrt_modified_normalized"]

    category_total_cnt["pos_score"] = (
        category_total_cnt["pos_ratio_calib"] + category_total_cnt["pos_cnt_sqrt_modified"])
    category_total_cnt["neg_score"] = (
        category_total_cnt["neg_ratio_calib"] + category_total_cnt["neg_cnt_sqrt_modified"])

    category_total_cnt["pos_score_scaled"] = category_total_cnt["pos_score"] * 100
    category_total_cnt["neg_score_scaled"] = category_total_cnt["neg_score"] * 100

    category_total_cnt = category_total_cnt.reset_index()

    category_dic = {}
    for i in category_total_cnt:
        category_dic[i] = [str(category_total_cnt[i][size])
                           for size in range(len(category_total_cnt["category"]))]

    category_json = json.dumps(category_dic)
    pos_score_json = json.dumps(category_dic["pos_score"])

    total_cnt = {"긍정적 리뷰": int(category_total_cnt["pos_cnt"].sum()), "부정적 리뷰": int(
        category_total_cnt["neg_cnt"].sum())}
    total_json = json.dumps(total_cnt)

    keyword = {}
    for item in DBKeyword8:
        keyword[item['title']] = [item['first'], item['second'], item['third']]
    #category_pos_cnt = txtfile.groupby("category").sum()
    #__tmp = ResultData_8.objects.values()

    data = ResultData.values.tolist()
    
    header = ["<span style='color:red;'>", "<span style='color:blue;'>"]
    footer = "</span>"
    for idx, item in enumerate(data):
        for tmp in keyword[item[1]]:
            data[idx][0] = data[idx][0].replace(tmp, header[item[2]]+tmp+footer)
        if item[2] == 0:
            data[idx][2] = '부정👿'
        else:
            data[idx][2] = '긍정😊'
    data = json.dumps(data)
    # sents8_json = pd.read_csv(os.path.join(BASE_DIR, 'nlp_proj/dummydata/FastText_8_sentiment_results.txt') , sep=",", names=["txt", "category", "sentiment", "rawIdx"])
    # overall = txtfile.groupby("label").count().iloc[:3, 1].values
    # overall_dic = {"neg" : overall[0], "pos" : overall[1]}
    # overall_json = json.dumps(overall_dic)

    # sents17_json = pd.read_csv(os.path.join(BASE_DIR, 'nlp_proj/dummydata/FastText_17_sentiment_results.txt') , sep=",", names=["txt", "category", "sentiment", "rawIdx"])

    # review_all = Hotel.objects.all()  # .get(), .filter(), ...
    # request가 POST -> Form을 완성.
    # Form이 유효하면 저장.\
    # if request.method == "POST":
    #     form = CoffeeForm(request.POST)  # 완성된 Form
    #     if form.is_valid():  # 채워진 Form이 유효하다면
    #         form.save()  # Form을 Model에 저장

    # form = CoffeeForm()
    return render(request, 'index.html', {"total_json": total_json, "category_json": category_json, "pos_score_json": pos_score_json, "data": data})


@csrf_exempt
def index2(request):
    DBKeyword = CategoryData_17.objects.all().values()
    ResultData = pd.DataFrame(ResultData_17.objects.values())
    ResultData = ResultData.drop(['id', 'raw_text'], axis=1)

    category_pos_cnt = ResultData.groupby("category").sum()
    category_total_cnt = ResultData.groupby("category").count()
    category_total_cnt["pos_cnt"] = category_pos_cnt["sentiment"]
    category_total_cnt["neg_cnt"] = category_total_cnt["sentiment"] - \
        category_total_cnt["pos_cnt"]

    category_total_cnt["pos_ratio"] = category_total_cnt["pos_cnt"] / \
        (category_total_cnt["pos_cnt"] + category_total_cnt["neg_cnt"])
    category_total_cnt["neg_ratio"] = category_total_cnt["neg_cnt"] / \
        (category_total_cnt["pos_cnt"] + category_total_cnt["neg_cnt"])

    category_total_cnt["pos_cnt_sqrt"] = category_total_cnt["pos_cnt"].apply(
        math.sqrt)
    category_total_cnt["neg_cnt_sqrt"] = category_total_cnt["neg_cnt"].apply(
        math.sqrt)

    scaling_val = max(
        category_total_cnt["pos_cnt_sqrt"] + category_total_cnt["neg_cnt_sqrt"])
    category_total_cnt["pos_cnt_sqrt_modified"] = category_total_cnt["pos_cnt_sqrt"] / \
        (scaling_val*8)
    category_total_cnt["neg_cnt_sqrt_modified"] = category_total_cnt["neg_cnt_sqrt"] / \
        (scaling_val*8)

    category_total_cnt["pos_cnt_sqrt_modified_normalized"] = (
        category_total_cnt["pos_cnt_sqrt_modified"] - category_total_cnt["pos_cnt_sqrt_modified"].mean()) / (category_total_cnt["pos_cnt_sqrt_modified"].std() * 50)
    category_total_cnt["neg_cnt_sqrt_modified_normalized"] = (
        category_total_cnt["neg_cnt_sqrt_modified"] - category_total_cnt["neg_cnt_sqrt_modified"].mean()) / (category_total_cnt["neg_cnt_sqrt_modified"].std() * 50)

    category_total_cnt["pos_ratio_calib"] = category_total_cnt["pos_ratio"] + \
        category_total_cnt["pos_cnt_sqrt_modified_normalized"]
    category_total_cnt["neg_ratio_calib"] = category_total_cnt["neg_ratio"] + \
        category_total_cnt["neg_cnt_sqrt_modified_normalized"]

    category_total_cnt["pos_score"] = (
        category_total_cnt["pos_ratio_calib"] + category_total_cnt["pos_cnt_sqrt_modified"])
    category_total_cnt["neg_score"] = (
        category_total_cnt["neg_ratio_calib"] + category_total_cnt["neg_cnt_sqrt_modified"])

    category_total_cnt["pos_score_scaled"] = category_total_cnt["pos_score"] * 100
    category_total_cnt["neg_score_scaled"] = category_total_cnt["neg_score"] * 100

    category_total_cnt = category_total_cnt.reset_index()

    category_dic = {}
    for i in category_total_cnt:
        category_dic[i] = [str(category_total_cnt[i][size])
                           for size in range(len(category_total_cnt["category"]))]

    category_json = json.dumps(category_dic)
    pos_score_json = json.dumps(category_dic["pos_score"])

    total_cnt = {"긍정적 리뷰": int(category_total_cnt["pos_cnt"].sum()), "부정적 리뷰": int(
        category_total_cnt["neg_cnt"].sum())}
    total_json = json.dumps(total_cnt)

    keyword = {}
    for item in DBKeyword:
        keyword[item['title']] = [item['first'], item['second'], item['third']]
    #category_pos_cnt = txtfile.groupby("category").sum()
    #__tmp = ResultData_8.objects.values()

    data = ResultData.values.tolist()
    header = ["<span style='color:red;'>", "<span style='color:blue;'>"]
    footer = "</span>"
    for idx, item in enumerate(data):
        for tmp in keyword[item[1]]:
            data[idx][0] = data[idx][0].replace(
                tmp, header[item[2]]+tmp+footer)
        if item[2] == 0:
            data[idx][2] = '부정👿'
        else:
            data[idx][2] = '긍정😊'
    data = json.dumps(data)
    # sents8_json = pd.read_csv(os.path.join(BASE_DIR, 'nlp_proj/dummydata/FastText_8_sentiment_results.txt') , sep=",", names=["txt", "category", "sentiment", "rawIdx"])
    # overall = txtfile.groupby("label").count().iloc[:3, 1].values
    # overall_dic = {"neg" : overall[0], "pos" : overall[1]}
    # overall_json = json.dumps(overall_dic)

    # sents17_json = pd.read_csv(os.path.join(BASE_DIR, 'nlp_proj/dummydata/FastText_17_sentiment_results.txt') , sep=",", names=["txt", "category", "sentiment", "rawIdx"])

    # review_all = Hotel.objects.all()  # .get(), .filter(), ...
    # request가 POST -> Form을 완성.
    # Form이 유효하면 저장.\
    # if request.method == "POST":
    #     form = CoffeeForm(request.POST)  # 완성된 Form
    #     if form.is_valid():  # 채워진 Form이 유효하다면
    #         form.save()  # Form을 Model에 저장

    # form = CoffeeForm()
    return render(request, 'index2.html', {"total_json": total_json, "category_json": category_json, "pos_score_json": pos_score_json, "data": data})


def upload_view(request):
    file_all = UploadFile.objects.all()
    # RawData.objects.all().delete()
    # ResultData_8.objects.all().delete()
    # ResultData_17.objects.all().delete()
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            integrated_model.ModelTest()
            file_all.delete()
        return redirect(index)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html')


@csrf_exempt
def lineChart(request):
    DBKeyword = CategoryData_8.objects.all().values()
    ResultData = pd.DataFrame(ResultData_8.objects.values())
    ResultData = ResultData.drop(['id', 'raw_text'], axis=1)
    keyword = {}
    for item in DBKeyword:
        keyword[item['title']] = [item['first'], item['second'], item['third']]
    #category_pos_cnt = txtfile.groupby("category").sum()
    #__tmp = ResultData_8.objects.values()

    data = ResultData.values.tolist()
    header = ["<span style='color:red;'>", "<span style='color:blue;'>"]
    footer = "</span>"
    for idx, item in enumerate(data):
        for tmp in keyword[item[1]]:
            data[idx][0] = data[idx][0].replace(
                tmp, header[item[2]]+tmp+footer)
        if item[2] == 0:
            data[idx][2] = '부정👿'
        else:
            data[idx][2] = '긍정😊'
    data = json.dumps(data)
    # 각 항목별 긍정 부정
    # data_1 = results_after_sentimental_col8[results_after_sentimental_col8["sentiment"] == True].count()["id"]
    # data_2 = results_after_sentimental_col8[results_after_sentimental_col8["sentiment"] == False].count()["id"]
    # df.groupby('key1')['key2'].apply(lambda x: x[x == 'one'].count())
   #대교님파트
    results_after_sentimental_col8 = pd.DataFrame(ResultData_8.objects.all().values())
   
    # 각 항목별 긍정 부정
    # data_1 = results_after_sentimental_col8[results_after_sentimental_col8["sentiment"] == True].count()["id"]
    # data_2 = results_after_sentimental_col8[results_after_sentimental_col8["sentiment"] == False].count()["id"]
    # df.groupby('key1')['key2'].apply(lambda x: x[x == 'one'].count())
   
    data_3 = results_after_sentimental_col8[results_after_sentimental_col8['sentiment'] == True].groupby('category').count()['sentiment']
    data_4 = results_after_sentimental_col8[results_after_sentimental_col8['sentiment'] == False].groupby('category').count()['sentiment']
    pos_by_cat = pd.DataFrame(data_3)
    neg_by_cat = pd.DataFrame(data_4)

    categories = pos_by_cat.index.tolist()
    pos_by_cat["pos_rate"] = pos_by_cat.iloc[:,0]/(pos_by_cat.iloc[:,0] + neg_by_cat.iloc[:,0]) * 100
    pos_by_cat["pos_rate"] = pos_by_cat["pos_rate"].apply(lambda x : int(x))

    pos_by_cat["neg_rate"] = neg_by_cat.iloc[:,0]/(pos_by_cat.iloc[:,0]+ neg_by_cat.iloc[:,0]) * 100
    pos_by_cat["neg_rate"] = pos_by_cat["neg_rate"].apply(lambda x : int(x))

    positive_nums = pos_by_cat['pos_rate'].tolist()
    positive_nums = json.dumps(positive_nums)
    negative_nums = pos_by_cat['neg_rate'].tolist()
    negative_nums = json.dumps(negative_nums)
    print(positive_nums,negative_nums)

    #각 카테고리의 날짜별 긍정숫자
    data_5 = results_after_sentimental_col8[results_after_sentimental_col8['sentiment'] == True].groupby(['category', 'date']).count()['sentiment']
    data_6 = results_after_sentimental_col8[results_after_sentimental_col8['sentiment'] == False].groupby(['category', 'date']).count()['sentiment']
    total_dic= dict()
    print(data_6)
    for i, key in enumerate(categories):
        #각 데이트별 dic만들어줌 
        date_dic = dict()
        pos_pd =  data_5[key]
        pos_pd =  pd.DataFrame(pos_pd)
        neg_pd =  data_6[key]
        neg_pd =  pd.DataFrame(neg_pd)
        pos_dates = pos_pd.index.tolist()
        neg_dates = neg_pd.index.tolist()
        both_dates =[]
        for date in pos_dates:
            if date in neg_dates:
                both_dates.append(date)
        pos_dates_value = pos_pd["sentiment"].tolist()
        neg_dates_value = neg_pd["sentiment"].tolist()

        
        for new_date in pos_dates:
            
            p =int(pos_pd.loc[new_date,"sentiment"])
            if new_date in neg_dates:
                n =int(neg_pd.loc[new_date,"sentiment"])
            else:
                n = 0
            date_dic[new_date] = [p,n]
        for new_date in neg_dates:
            if new_date not in pos_dates:
                p = 0
                n =int(neg_pd.loc[new_date,"sentiment"])
            date_dic[new_date] = [p,n]
        for new_date in both_dates:
            p =int(pos_pd.loc[new_date,"sentiment"])
            n =int(neg_pd.loc[new_date,"sentiment"])
            date_dic[new_date] = [p,n]        

        date_dic = {key:value for key, value in sorted(((key,value) for key,value in date_dic.items()), key = lambda x:x[0])}
        total_dic[key] = date_dic
    categories = json.dumps(categories)
    cleanness_timeseries_pos_neg = json.dumps(total_dic)


    if request.method == "POST":
        form = barChart(request.POST)
        if form.is_valid():
            print(form)

    return render(request, 'lineChart.html', {'categories': categories, 'clean_data': cleanness_timeseries_pos_neg,
                                              "positive": positive_nums, "negative": negative_nums, "data": data})
def lineChart2(request):
    DBKeyword = CategoryData_17.objects.all().values()
    ResultData = pd.DataFrame(ResultData_17.objects.values())
    ResultData = ResultData.drop(['id', 'raw_text'], axis=1)
    keyword = {}
    for item in DBKeyword:
        keyword[item['title']] = [item['first'], item['second'], item['third']]
    #category_pos_cnt = txtfile.groupby("category").sum()
    #__tmp = ResultData_8.objects.values()

    data = ResultData.values.tolist()
    header = ["<span style='color:red;'>", "<span style='color:blue;'>"]
    footer = "</span>"
    for idx, item in enumerate(data):
        for tmp in keyword[item[1]]:
            data[idx][0] = data[idx][0].replace(
                tmp, header[item[2]]+tmp+footer)
        if item[2] == 0:
            data[idx][2] = '부정👿'
        else:
            data[idx][2] = '긍정😊'
    data = json.dumps(data)
    # 각 항목별 긍정 부정
    # data_1 = results_after_sentimental_col8[results_after_sentimental_col8["sentiment"] == True].count()["id"]
    # data_2 = results_after_sentimental_col8[results_after_sentimental_col8["sentiment"] == False].count()["id"]
    # df.groupby('key1')['key2'].apply(lambda x: x[x == 'one'].count())
   #대교님파트
    results_after_sentimental_col8 = pd.DataFrame(ResultData_17.objects.all().values())
   
    # 각 항목별 긍정 부정
    # data_1 = results_after_sentimental_col8[results_after_sentimental_col8["sentiment"] == True].count()["id"]
    # data_2 = results_after_sentimental_col8[results_after_sentimental_col8["sentiment"] == False].count()["id"]
    # df.groupby('key1')['key2'].apply(lambda x: x[x == 'one'].count())
   
    data_3 = results_after_sentimental_col8[results_after_sentimental_col8['sentiment'] == True].groupby('category').count()['sentiment']
    data_4 = results_after_sentimental_col8[results_after_sentimental_col8['sentiment'] == False].groupby('category').count()['sentiment']
    pos_by_cat = pd.DataFrame(data_3)
    neg_by_cat = pd.DataFrame(data_4)

    categories = pos_by_cat.index.tolist()
    pos_by_cat["pos_rate"] = pos_by_cat.iloc[:,0]/(pos_by_cat.iloc[:,0] + neg_by_cat.iloc[:,0]) * 100
    pos_by_cat["pos_rate"] = pos_by_cat["pos_rate"].apply(lambda x : int(x))

    pos_by_cat["neg_rate"] = neg_by_cat.iloc[:,0]/(pos_by_cat.iloc[:,0]+ neg_by_cat.iloc[:,0]) * 100
    pos_by_cat["neg_rate"] = pos_by_cat["neg_rate"].apply(lambda x : int(x))

    positive_nums = pos_by_cat['pos_rate'].tolist()
    positive_nums = json.dumps(positive_nums)
    negative_nums = pos_by_cat['neg_rate'].tolist()
    negative_nums = json.dumps(negative_nums)
    print(positive_nums,negative_nums)

    #각 카테고리의 날짜별 긍정숫자
    data_5 = results_after_sentimental_col8[results_after_sentimental_col8['sentiment'] == True].groupby(['category', 'date']).count()['sentiment']
    data_6 = results_after_sentimental_col8[results_after_sentimental_col8['sentiment'] == False].groupby(['category', 'date']).count()['sentiment']
    total_dic= dict()
    print(data_6)
    for i, key in enumerate(categories):
        #각 데이트별 dic만들어줌 
        date_dic = dict()
        pos_pd =  data_5[key]
        pos_pd =  pd.DataFrame(pos_pd)
        neg_pd =  data_6[key]
        neg_pd =  pd.DataFrame(neg_pd)
        pos_dates = pos_pd.index.tolist()
        neg_dates = neg_pd.index.tolist()
        both_dates =[]
        for date in pos_dates:
            if date in neg_dates:
                both_dates.append(date)
        pos_dates_value = pos_pd["sentiment"].tolist()
        neg_dates_value = neg_pd["sentiment"].tolist()

        
        for new_date in pos_dates:
            
            p =int(pos_pd.loc[new_date,"sentiment"])
            if new_date in neg_dates:
                n =int(neg_pd.loc[new_date,"sentiment"])
            else:
                n = 0
            date_dic[new_date] = [p,n]
        for new_date in neg_dates:
            if new_date not in pos_dates:
                p = 0
                n =int(neg_pd.loc[new_date,"sentiment"])
            date_dic[new_date] = [p,n]
        for new_date in both_dates:
            p =int(pos_pd.loc[new_date,"sentiment"])
            n =int(neg_pd.loc[new_date,"sentiment"])
            date_dic[new_date] = [p,n]        

        date_dic = {key:value for key, value in sorted(((key,value) for key,value in date_dic.items()), key = lambda x:x[0])}
        total_dic[key] = date_dic
    categories = json.dumps(categories)
    cleanness_timeseries_pos_neg = json.dumps(total_dic)

    # if request.method == "POST":
    #     form = request.POST.get(colidx)
    #     print(form)

    return render(request, 'lineChart.html', {'categories': categories, 'clean_data': cleanness_timeseries_pos_neg,
                                              "positive": positive_nums, "negative": negative_nums, "data": data})

