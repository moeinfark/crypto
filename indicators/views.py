from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import time
from decimal import Decimal


def request_to_main_api(request_text):
    while True:
        try:
            response__ = requests.get(request_text)
            return response__
        except Exception as error:
            print("Main api can't response, in line 15 error is: " + str(error))
            print("Bot will go sleep for 10 seconds!")
            time.sleep(10)


@api_view(['POST'])
def atr(request):
    symbol = request.data['symbol']
    interval = request.data['interval']
    request_atr = "https://api2.binance.com/api/v3/klines?symbol=" + str(symbol).upper() + "&interval=" + str(interval).lower() + "&limit=1000"
    response_atr = request_to_main_api(request_atr)
    data_atr = response_atr.json()
    # print(data)
    atr_ = Decimal(0.0)
    atr_pre = Decimal(max(Decimal(data_atr[1][2]) - Decimal(data_atr[1][3]),
                          Decimal(abs(Decimal(data_atr[1][2]) - Decimal(data_atr[1 - 1][4]))),
                          Decimal(abs(Decimal(data_atr[1][3]) - Decimal(data_atr[1 - 1][4])))))

    for i in range(2, len(data_atr) - 1):
        tr = Decimal(max(Decimal(data_atr[i][2]) - Decimal(data_atr[i][3]),
                         Decimal(abs(Decimal(data_atr[i][2]) - Decimal(data_atr[i - 1][4]))),
                         Decimal(abs(Decimal(data_atr[i][3]) - Decimal(data_atr[i - 1][4])))))
        atr_ = (atr_pre * 13 + tr) / 14
        atr_pre = atr_

    return Response({
        "value": atr_
    }, status=status.HTTP_200_OK)


'''
candle values

yek seri chizayi mixad ke aval ejbaria ro migam oonayi ke khode tapi khaste

1-secret : ino vaghti api key mixay tappi mifreste va ma nadarim tu codemoon ehtemalan

2-exchange : ke masalan binance ya okex ya ... va ma dar avale kar faghat binance e

3-symbol : ke che arzi ro mixay

4- interval : ke che time yi bashe candle masalan 15m, 30m, 1h, 4h, 1d ,...


hala ekhtiary ha ro darim : 

1-backtrack : mige az alan chand candle ghablo behem begoo, agar hichi nazad candl alano mige
agar khast candle ghablio bebine 1 mizane va 5 candle ghabl 5, yek saghf ham gozashte taapi ke
balaye 50 nemishe zad va default gozashte 0

2-backtracks : age chand candle akhar ro bekham mizani backtracks va meghdaro midi masalan 2 taye akhar mishe
"backtracks = 2"

3-chart : candle ha ro mishe be anvae mokhtalef rasm kard ye model darim esmesh "heikinashi" e ke open candle
avalin moamele nist miad ru miangin open o close candle ghabli. tu in motheghayer mige age nazadi chizi 
candle ro mige, agar zadi heikinashi meghdare heikinashi ro mixoone mide.

nemoone chizi ke pass mide:

{
  "timestampHuman": "2021-01-14 15:00:00 (Thursday) UTC",
  "timestamp": 1610636400,
  "open": 39577.53,
  "high": 39666,
  "low": 39294.7,
  "close": 39607.09,
  "volume": 1211.2841909999893
}

address refrence : https://taapi.io/indicators/candle/
'''








'''
bollinger band

refrence : https://taapi.io/indicators/bollinger-bands-another-implementation/

nemoone chizi ke tahesh mide 

{
    "valueUpperBand": 39541.935773866826,
    "valueMiddleBand": 37920.27099999998,
    "valueLowerBand": 36298.60622613313,
    "backtrack": 0
  }

variable hayi ke migire:
ejbari :

1-secret : ino vaghti api key mixay tappi mifreste va ma nadarim tu codemoon ehtemalan

2-exchange : ke masalan binance ya okex ya ... va ma dar avale kar faghat binance e

3-symbol : ke che arzi ro mixay

4- interval : ke che time yi bashe candle masalan 15m, 30m, 1h, 4h, 1d ,...

ekhtiari ha :

1-backtrack : mige az alan chand candle ghablo behem begoo, agar hichi nazad candl alano mige
agar khast candle ghablio bebine 1 mizane va 5 candle ghabl 5, yek saghf ham gozashte taapi ke
balaye 50 nemishe zad va default gozashte 0

2-backtracks : age chand candle akhar ro bekham mizani backtracks va meghdaro midi masalan 2 taye akhar mishe
"backtracks = 2"

3-chart : candle ha ro mishe be anvae mokhtalef rasm kard ye model darim esmesh "heikinashi" e ke open candle
avalin moamele nist miad ru miangin open o close candle ghabli. tu in motheghayer mige age nazadi chizi 
candle ro mige, agar zadi heikinashi meghdare heikinashi ro mixoone mide.

4-period : toole bazeyi ke az ruye oon meghdare andicator bara har noghte hesab mishe va age nade 
defaultesh 20 e

5-stddev : standard deviation e ke default 2 e

mohasebe :

middle band mishe miangine close baraye candle haye period dade shode (20 default)

upper band mishe miangine close candle haye period ( ke hamoon midle band e) + (be alave) 
(stddev * standard deviation hamin candle ha ( 20 ta default ) )

lower band ham mishe hamoon ghable faghat menha mikoni

age backtracks ham bede zire result bayad data bargarde ke in male candle chandome
'''