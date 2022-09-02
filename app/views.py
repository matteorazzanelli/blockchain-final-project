################################# Connect to redis server
import redis
redis_host = '127.0.0.1'
client = redis.StrictRedis(host=redis_host, port=6379, password='',db=0)

try:
  client.client_list()
  print('CONNECTION TO REDIS OK')
except:
  print('CONNECTION TO REDIS SERVER FAILED.')
  # sys.exit('No valid blockchain provided: exiting...')
  

################################# Fetch deployed conract
import sys
from django.conf import settings
BLOCKCHAIN = settings.BLOCKCHAIN
if BLOCKCHAIN == 'ganache':
  blockchain_address = 'http://127.0.0.1:7545'
  chain_id = 1337 # ganache
elif BLOCKCHAIN == 'ropsten':
  blockchain_address = 'https://ropsten.infura.io/v3/7340ba294b4f4b1da1ffdd1d23ef3022'
  chain_id = 3
else:
  sys.exit('No valid blockchain provided: exiting...')

from web3 import Web3
w3 = Web3(Web3.HTTPProvider(blockchain_address))
if not w3.isConnected():
  print('BLOCKCHAIN NOT CONNECTED.')
  # sys.exit('No valid blockchain provided: exiting...')
else:
  print('CONNECTION TO WEB3 OK')

# retrieve contract vars
import json
deployed_contract_address = ''
if not w3.isAddress(deployed_contract_address):
  print('CONTRACT ADDRESS NOT VALID')
  # sys.exit('No valid blockchain provided: exiting...')
else:
  print('CONTRACT ADDRESS OK')
compiled_contract_path = 'truffle/build/Platform.json'
with open(compiled_contract_path) as file:
  contract_json = json.load(file)  # load contract info as JSON
  contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# create contract instance
contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)

# set as default account as empty for safety reason
w3.eth.default_account = '' # client.get("account").decode("utf-8")

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

@csrf_exempt
def new(request):
  try:
    # save account in redis db
    result = json.loads(request.body)
    print(request)
    # client.set("account", result['account'])
    # print(type(client.get("account").decode("utf-8") ))
  except (ValueError, KeyError):
    raise ValueError('Invalid POST parameters')
  return JsonResponse({'result': 'ok'})

@csrf_exempt
def contribute(request):
  try:
    # save account in redis db
    result = json.loads(request.body)
    print(request)
    # client.set("account", result['account'])
    # print(type(client.get("account").decode("utf-8") ))
  except (ValueError, KeyError):
    raise ValueError('Invalid POST parameters')
  return JsonResponse({'result': 'ok'})

###############################################################
def get_pending_auctions():
  # acts = []
  # # check if contract has been completed, and eventually make its status to 'closed'
  # # closed contracts are not shown
  # num_of_contracts = contract.functions.numContract_().call()
  # for i in range(num_of_contracts):
  #   t = contract.functions.getTitleDeed(i).call()
  #   if t[6] is True:
  #     record = NotaryModelForm.objects.filter(id=i).first()
  #     if record is not None:
  #       record.status = 'closed' # todo: this is redundant for already closed contracts
  #   else:
  #     acts.append({'id': i, 'buyer':t[0], 'seller':t[1], 'description':t[2],
  #                'amount': t[3], 'amount_for_now': t[4],
  #                'deadline':round((t[5]-time.time())/(7*24*3600))})
  # return acts

  output = []
  return output

###############################################################
def homepage(request):
  print('################## PYTHON ###################')
  form = AuctionForm()
  
  pending_auctions = get_pending_auctions()
  context = {
    "pending_auctions": pending_auctions,
    "form": form
  }
  return render(request=request, template_name='app/home.html', context=context)