
from urllib.parse import unquote
import pandas as pd
import requests
import json
import datetime

def getultraSrtNcst(nx, ny):
    skey = unquote('ceF8dIKXadDdqQImvanWTbjo8BTIMAp2x6%2FfGd2PEx%2FR5VlSHGfTWr4SESySZT8UtLjpioddno97lcqRNIQ6tw%3D%3D')
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst'

    yesterday = (datetime.date.today() - datetime.timedelta(1)).strftime("%Y%m%d")
    today = datetime.date.today().strftime("%Y%m%d")

    time_list = ["0900", "1200", "1500", "1800", "2100"]
    df = pd.DataFrame()
    for time_idx in time_list:
        params = {
            'serviceKey': skey,
            'pageNo': '1',
            'numOfRows': '10',
            'dataType': 'json',
            'base_date': yesterday,
            'base_time': time_idx,
            'nx': nx,
            'ny': ny
        }

        res = requests.get(url, params=params)
        data = json.loads(res.text)
        items = data['response']['body']['items']['item']
        # print(items)
        for item in items:
            item_dict1 = {}
            item_dict1['baseDate'] = item['baseDate']
            item_dict1['baseTime'] = item['baseTime']
            item_dict1['category'] = item['category']
            item_dict1['nx'] = item['nx']
            item_dict1['ny'] = item['ny']
            item_dict1['obsrValue'] = float(item['obsrValue'])
            df = df.append(item_dict1, ignore_index=True)

    return df
