import requests

print("Are you deploying the model from the Railway web service?(y/n)")

response = input().strip().lower()
if response == 'y':
    url = 'https://midterm-project-mlzoomcamp2026-datapipeline-production.up.railway.app/predict'
else:
    url = 'http://localhost:9696/predict'

trading_session_date = '2018-02-20'
todays_data = {
 'open': 6.03683106811,
 'high': 6.21244794283,
 'low': 6.03313095394,
 'close': 6.14363193512,
 'volume': 686240000,
 'daily_return_pct': 2.14892725681,
 'log_return': 0.0212616335739,
 'intraday_return_pct': 1.76915447529,
 'daily_range_pct': 2.97038275324,
 'overnight_gap_pct': 0.373170813375,
 'sma_20': 5.82466084957,
 'sma_50': 5.38304859161,
 'volatility_20_pct': 56.5811193023,
 'volume_sma_20': 755583600.0,
 'drawdown_pct': 0.0,
 'year': 2018,
 'month': 2,
 'day_of_week': 'Tuesday'
 }

response = requests.post(url, json=todays_data)

print(f"Response status code: {response.status_code}")   # e.g. 200
#response.raise_for_status()   # raises an error if the server returned 4xx or 5xx
#print(response.text)
print(f"Date of trading session: {trading_session_date}, Closing price: {todays_data['close']}")
response_data = response.json()
print(response_data)