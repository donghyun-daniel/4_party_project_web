import django
from django.core.wsgi import get_wsgi_application
import csv
import pandas as pd
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'nlp.settings'
django.setup()

from nlp_proj.models import Hotel

application = get_wsgi_application()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_data():
    data = {}
    df = pd.read_csv(os.path.join(BASE_DIR, 'hotel.txt'), sep="\t", encoding='utf-8')
    for i in range(len(df)):
        data[i] = (df["text"][i], df['label'][i])
    return data


if __name__ == '__main__':
    hotel_data = load_data()
    for key, value in hotel_data.items():
        Hotel(idx=key, text=value[0], label=value[1]).save()
