################################# Connect to redis server
import redis
redis_host = '127.0.0.1'
client = redis.StrictRedis(host=redis_host, port=6379, password='',db=0)
try:
  client.client_list()
except redis.ConnectionError:
  ValueError('CONNECTION TO REDIS SERVER FAILED.')
print('connected to redis "{}"'.format(redis_host)) 

################################# Fetch deployed conract
import sys
from django.conf import settings
BLOCKCHAIN = settings.BLOCKCHAIN
if BLOCKCHAIN == 'ganache':
  blockchain_address = 'http://127.0.0.1:7545'
elif BLOCKCHAIN == 'ropsten':
  blockchain_address = 'https://ropsten.infura.io/v3/7340ba294b4f4b1da1ffdd1d23ef3022'
else:
  sys.exit('No valid blockchain provided: exiting...')

from web3 import Web3
w3 = Web3(Web3.HTTPProvider(blockchain_address))
if not w3.isConnected():
  print('BLOCKCHAIN NOT CONNECTED.')
else:
  print('CONNECTION TO WEB3 OK')

# retrieve contract vars
import json
deployed_contract_address = ''
if not w3.isAddress(deployed_contract_address):
  print('CONTRACT ADDRESS NOT VALID')
else:
  print('CONTRACT ADDRESS OK')
compiled_contract_path = 'truffle/build/Platform.json'
with open(compiled_contract_path) as file:
  contract_json = json.load(file)  # load contract info as JSON
  contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# create contract instance
contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)

################################# Methods

from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .forms import AuctionForm

# the following decorator allows to avoid 403 forbidden error since post methods is unsafe
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def test(request):
  try:
    # save account in redis db
    result = json.loads(request.body)
    client.set("account", result['account'])
    # print(type(client.get("account").decode("utf-8") ))
  except (ValueError, KeyError):
    raise ValueError('Invalid POST parameters')
  return JsonResponse({'result': result['account']})

###############################################################
def get_pending_auctions():
  # for filter in filters:
  #   for event in filter.get_new_entries():
  #     # update records in db
  #     record = Event.objects.filter(type=event['event']).first()
  #     if record is not None:
  #       record.times += 1
  #       record.date = datetime.now()
  #       record.save()
  # # db is updated, now retrieve info we need
  output = []
  # for event in events:
  #   record = Event.objects.filter(type=event).first()
  #   output.append({'type':record.type, 'times':record.times, 'date':record.date})
  return output

###############################################################
def homepage(request):
  print('################## PYTHON ###################')
  form = AuctionForm()
  #if there is an incoming submitted form
  # if request.method == "POST":
  #   print('avevo ragione')
  #   form = AuctionForm(request.POST)
  #   if form.is_valid():
  #     processForm(form, request)
  #     return redirect('app:homepage')
  
  pending_auctions = get_pending_auctions()
  context = {
    "pending_auctions": pending_auctions,
    "form": form
  }
  return render(request=request, template_name='app/home.html', context=context)