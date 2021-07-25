import requests
import json

# 최초로 발급받은 access token의 유효기간은 12시간, refresh token은 30일 입니다.
# refresh token 만료가 1주일 이내로 남은 시점에서 사용자 토큰 갱신 요청을 하면 갱신된 access token과 갱신된 refresh token이 함께 반환됩니다.

# curl -v -X POST "https://kauth.kakao.com/oauth/token" \
#  -d "grant_type=refresh_token" \
#  -d "client_id={REST_API_KEY}" \
#  -d "refresh_token={USER_REFRESH_TOKEN}"

def get_refresh_token():
    refresh_token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        'grant_type': 'refresh_token',
        'client_id': '30a9a96815d96026af18329255990a86',
        'refresh_token': 'L66IK9vuDPgDdjrirSUtYVFGSv84aBZEmM22kQo9dVsAAAF6tRb0gg'
    }

    res = requests.post(refresh_token_url, data=data)
    result = json.loads(res.text)

    return result["access_token"]
