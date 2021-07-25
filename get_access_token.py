import requests

# 카카오톡 api 를 활용하여 톡을 보내기 위한 access token 발급
# 최초로 발급받은 access token의 유효기간은 12시간, refresh token은 30일 입니다.
# refresh token 만료가 1주일 이내로 남은 시점에서 사용자 토큰 갱신 요청을 하면 갱신된 access token과 갱신된 refresh token이 함께 반환됩니다.

# https://example.com/oauth?code=Mw1HYGpNLgvpIiwhwm4b3whtzh7u2Qt2xUZNumJ4drp55ci5fvlG39uPAoY-xND6W_7KoQorDSAAAAF6tQ6Dtw
url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = '30a9a96815d96026af18329255990a86'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'NN4zEOwz0Gm9YrEKWQm-VdKEKkIKmxHDi3_ed-YmNRduxZms2b_3mcTvnYnsDELVZPQbmgo9dBEAAAF6tRae3Q'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# json 저장
import json
with open("kakao_code.json","w") as fp:
    json.dump(tokens, fp)