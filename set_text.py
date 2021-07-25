def yesterday_temp(x):
    if x > 0:
        diff_speak = '높'
    elif x < 0:
        diff_speak = '낮'
    else:
        diff_speak = '같'
    return diff_speak

def set_text(df,yesterday_df):
    data_result = dict()

    #비/눈 여부에 따른 분류
    if len(df[(df['category'] == 'POP') & (df['fcstValue'] >= 60)]) > 0:
        rain = df[(df['category'] == 'POP') & (df['fcstValue'] >= 60)]
        pty_code = int(df[(df['category'] == 'PTY') & (df['fcstTime'] == rain['fcstTime'].values[0])]['fcstValue'].values[0])

        if pty_code == 1:
            data_result['pty_code'] = '비'
        elif pty_code == 2:
            data_result['pty_code'] = '비/눈'
        elif pty_code == 3:
            data_result['pty_code'] = '눈'
        elif pty_code == 4:
            data_result['pty_code'] = '소나기'
        elif pty_code == 5:
            data_result['pty_code'] = '빗방울'
        elif pty_code == 6:
            data_result['pty_code'] = '빗방울/눈날림'
        elif pty_code == 7:
            data_result['pty_code'] = '눈날림'

        speak = '오늘 {0}시부터 {1}% 확률로 {2}mm {3}이(가) 올 예정이니 우산 가지고 나가!'.format(int(rain['fcstTime'].values[0]/100), rain['fcstValue'].values[0], df[df['category'] == 'R06']['fcstValue'].sum(), data_result['pty_code'])
    else:
        speak = None

    # 기온에 따른 분류
    data_result['최고기온'] = df[df['category'] == 'T3H']['fcstValue'].max()
    data_result['최저기온'] = df[df['category'] == 'T3H']['fcstValue'].min()
    data_result['습도'] = df[df['category'] == 'REH']['fcstValue'].mean()

    if data_result['최고기온'] >= 33:
        temperature_speak = '오늘 한낮의 최고 기온이 {0}도로 폭염이래! 밖에 있을 땐 조심하고, 물 자주 마셔!'.format(data_result['최고기온'])
    elif 25 <= data_result['최고기온'] < 33:
        temperature_speak = '오늘은 하루종일 무더운 날씨가 계속될 것 같아! 더위에 지치지 않도록 조심해!'
    elif 10 <= data_result['최고기온'] < 25:
        temperature_speak = '오늘은 하루종일 따듯한 날씨야:)'
    elif 0 <= data_result['최고기온'] < 10:
        temperature_speak = '오늘은 살짝 쌀쌀하니 얇은 외투 챙기고 나가!'
    else:
        temperature_speak = '오늘은 최저 기온이 {0}도로 한파래! 따뜻하게 입고 나가!'.format(data_result['최저기온'])

    #어제와 기온 차이
    data_result['어제최고기온'] = yesterday_df[yesterday_df['category'] == 'T1H']['obsrValue'].max()
    data_result['어제최저기온'] = yesterday_df[yesterday_df['category'] == 'T1H']['obsrValue'].min()

    data_result['어제와 최고기온 차이'] = abs(data_result['최고기온'] - data_result['어제최고기온'])
    data_result['어제와 최저기온 차이'] = abs(data_result['최저기온'] - data_result['어제최저기온'])

    diff_yesterday_speak = '오늘 최고 기온은 어제보다 {0:.1f}도 {1}은 {2}도이고, 최저 기온은 어제보다 {3:.1f}도 {4}은 {5}도야.'.format(data_result['어제와 최고기온 차이'], yesterday_temp(data_result['어제와 최고기온 차이']), data_result['최고기온'],
                                                                                                 data_result['어제와 최저기온 차이'], yesterday_temp(data_result['어제와 최저기온 차이']), data_result['최저기온'])

    #일교차 분류
    data_result['일교차'] = data_result['최고기온'] - data_result['최저기온']
    diff_temperature_speak = None
    if data_result['일교차'] >= 10:
        diff_temperature_speak = '오늘은 낮과 밤의 기온 차가 {0}도로 크게 벌어지니 건강관리에 유의해.'.format(data_result['일교차'])

    if speak != None:
        if diff_temperature_speak != None:
            result_speak = speak + '\n그리고 ' + temperature_speak + '\n그리고 ' + diff_yesterday_speak + '\n아맞다! 그리고 ' + diff_temperature_speak
        else:
            result_speak = speak + '\n그리고 ' + temperature_speak + '\n그리고 ' + diff_yesterday_speak
    else:
        if diff_temperature_speak != None:
            result_speak = temperature_speak + '\n그리고 ' + diff_temperature_speak + '\n그리고 ' + diff_yesterday_speak
        else:
            result_speak = temperature_speak + '\n그리고 ' + diff_yesterday_speak

    result_speak = result_speak+ '\n오늘 하루도 건강하고 즐거운 하루 보내!'

    return result_speak