from urllib.parse import urlencode, quote_plus, unquote
import pandas as pd
from datetime import datetime
import requests
import json

def getVilageFcst(nx, ny):
    skey = unquote('ceF8dIKXadDdqQImvanWTbjo8BTIMAp2x6%2FfGd2PEx%2FR5VlSHGfTWr4SESySZT8UtLjpioddno97lcqRNIQ6tw%3D%3D')
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst'
    today = datetime.today().strftime("%Y%m%d")
    params = {'ServiceKey': skey,
              'pageNo': '1',
              'numOfRows': '50',
              'dataType': 'json',
              'base_date': today,
              'base_time': '0200', #9 12 15 18 21 하루 데이터 가지고 가공
              'nx': nx,
              'ny': ny
    }

    res = requests.get(url, params=params)
    data = json.loads(res.text)
    items = data['response']['body']['items']['item']

    #pandas 모듈을 통해 DateFrame(표) 생성
    df = pd.DataFrame()
    for item in items:
        item_dict = {}
        item_dict['baseDate'] = item['baseDate']
        item_dict['baseTime'] = item['baseTime']
        item_dict['category'] = item['category']
        item_dict['fcstDate'] = item['fcstDate']
        item_dict['fcstTime'] = int(item['fcstTime'])
        item_dict['fcstValue'] = float(item['fcstValue'])
        item_dict['nx'] = item['nx']
        item_dict['ny'] = item['ny']
        df = df.append(item_dict, ignore_index=True)

    return df

#     baseDate baseTime category  fcstDate fcstTime fcstValue  nx   ny
# 0   20210711     0500      POP  20210711     0900        30  55  127
# 1   20210711     0500      PTY  20210711     0900         0  55  127
# 2   20210711     0500      REH  20210711     0900        90  55  127
# 3   20210711     0500      SKY  20210711     0900         4  55  127
# 4   20210711     0500      T3H  20210711     0900        25  55  127
# 5   20210711     0500      UUU  20210711     0900      -0.7  55  127
# 6   20210711     0500      VEC  20210711     0900       135  55  127
# 7   20210711     0500      VVV  20210711     0900       0.8  55  127
# 8   20210711     0500      WSD  20210711     0900       1.1  55  127


# 9   20210711     0500      POP  20210711     1200        30  55  127
# 10  20210711     0500      PTY  20210711     1200         0  55  127
# 11  20210711     0500      R06  20210711     1200         0  55  127
# 12  20210711     0500      REH  20210711     1200        85  55  127
# 13  20210711     0500      S06  20210711     1200         0  55  127
# 14  20210711     0500      SKY  20210711     1200         4  55  127
# 15  20210711     0500      T3H  20210711     1200        26  55  127
# 16  20210711     0500      UUU  20210711     1200       1.2  55  127
# 17  20210711     0500      VEC  20210711     1200       202  55  127
# 18  20210711     0500      VVV  20210711     1200       2.9  55  127
# 19  20210711     0500      WSD  20210711     1200       3.1  55  127

