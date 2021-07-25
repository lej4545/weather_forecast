from get_refresh_token import *
from vilageFcst import *
from ultraSrtNcst import *
import set_text
import pandas as pd
from random_picture import *

access_token = get_refresh_token()
friend_url = "https://kapi.kakao.com/v1/api/talk/friends"

# eunjin
# GET /v1/api/talk/friends HTTP/1.1
# Host: kapi.kakao.com
# Authorization: Bearer {ACCESS_TOKEN}

headers={"Authorization" : "Bearer " + access_token}
result = json.loads(requests.get(friend_url, headers=headers).text)

print("=============================================")
print(result)
print("=============================================")
friends_list = result["elements"]
print(friends_list)
print("=============================================")
print(friends_list[0].get("uuid"))
friend_id = friends_list[0].get("uuid")
print(friend_id)

familys = [
    {
        "id": 1806945511,
        "nx": "60",
        "ny" : "121"
     },
    {
        "id": 1806947703,
        "nx": "61",
        "ny": "121"
    },
    {
        "id": 1810629941,
        "nx": "52",
        "ny": "38"
    }
]
df = pd.DataFrame()
for family in familys:
    family_dict = {}
    family_dict['id'] = family['id']
    family_dict['nx'] = family['nx']
    family_dict['ny'] = family['ny']
    df = df.append(family_dict, ignore_index=True)

for idx in friends_list:
    id = idx["id"]
    uuid = idx["uuid"]
    nx = df[df["id"] == id]["nx"].values[0]
    ny = df[df["id"] == id]["ny"].values[0]
    weather_data = getVilageFcst(nx, ny)
    yesterday_data = getultraSrtNcst(nx, ny)
    text_middle = set_text.set_text(weather_data, yesterday_data)

    if id == 1806945511:
        text_head = "자기!!\n"
    elif id == 1806947703:
        text_head = "언니!!\n"
    elif id == 1810629941:
        text_head = "엄마!!\n"

    text = text_head + text_middle
    print(text)
    send_url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    picture_url = random_picture()
    data = {
        'receiver_uuids': '["{}"]'.format(uuid),
        "template_object": json.dumps({
            "object_type": "text",
            "text": text,
            "link": {
                "web_url": "https://m.weather.naver.com",
                "mobile_web_url": "https://m.weather.naver.com"
            },
            "buttons": [
                {
                    "title": "은진이 사진",
                    "link": {
                        "web_url": picture_url,
                        "mobile_web_url": picture_url
                    }
                },
                {
                    "title": "네이버 날씨",
                    "link": {
                        "web_url": "https://m.weather.naver.com",
                        "mobile_web_url": "https://m.weather.naver.com"
                    }
                }
            ]
        })
    }

    response = requests.post(send_url, headers=headers, data=data)
    print(response.text)