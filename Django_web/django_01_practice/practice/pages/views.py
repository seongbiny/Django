import requests
import random
from django.shortcuts import render

# Create your views here.
def lotto(request):
    url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=1'
    response = requests.get(url)
    lotto = response.json()
    winno = []
    for i in range(1, 7):
        winno.append(lotto[f'drwtNo{i}'])

    cnt = {'1등':0, '2등':0, }
    for i in range(1000):
        my_number = random.sample(range(1, 46), 6)
        # 등수 확인 rule을 적용
    context = {
        #'lotto': lotto,
        'winno': winno,
        'bonusNo': lotto['bnusNo'],
        'win_rate': cnt,
    }
    return render(request, 'pages/lotto.html', context)

   