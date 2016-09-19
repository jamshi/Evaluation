from django.shortcuts import render
import json, requests
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import HttpResponse
# Create your views here.

@csrf_exempt
def home(request):
	if request.is_ajax():
		selected_date =  datetime.datetime.strptime(request.POST['date'], "%m/%d/%Y").date().strftime("%Y%m%d")
		params = dict(bypass='true',date=selected_date)
		resp = requests.get(url='https://finance.yahoo.com/connection/currency-converter-cache', params=params)
		data = json.loads(resp.text[resp.text.index('(')+1:-3])
		for x in data['list']['resources']:
			if x['resource']['fields']['symbol'] == 'SGD=X':
				response_data = {}
				response_data['exchangeRate'] = float(x['resource']['fields']['price'])
				response_data['totalAmt'] = float(request.POST['amt']) * float(x['resource']['fields']['price'])
				return HttpResponse(json.dumps(response_data), content_type="application/json")
	return render(request, 'index.html')
