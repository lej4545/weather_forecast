import requests
import json
from get_refresh_token import *
from random_picture import *
access_token = get_refresh_token()

friend_url = "https://kapi.kakao.com/v1/api/talk/friends"

# GET /v1/api/talk/friends HTTP/1.1
# Host: kapi.kakao.com
# Authorization: Bearer {ACCESS_TOKEN}

headers={"Authorization" : "Bearer " + access_token}

result = json.loads(requests.get(friend_url, headers=headers).text)

print(type(result))
print("=============================================")
print(result)
print("=============================================")
friends_list = result.get("elements")
print(friends_list)
# print(type(friends_list))
print("=============================================")
print(friends_list[0].get("uuid"))
friend_id = friends_list[0].get("uuid")
print(friend_id)

send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
picture_url = random_picture()
data = {
    'receiver_uuids': '["{}"]'.format(friend_id),
    "template_object": json.dumps({
        "object_type": "text",
        "text": "자기 테스트",
        "link": {
            "web_url" : "https://m.weather.naver.com",
            "mobile_web_url" : "https://m.weather.naver.com"
        },
        "buttons": [
            {
                "title": "은진이 사진",
                "link": {
                    "web_url" : picture_url,
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