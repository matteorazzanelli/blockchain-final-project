################################# Connect to redis server
import redis
client = redis.StrictRedis(host='127.0.0.1', port=6379, password='',db=0)

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

# retrieve contract vars
import json
deployed_contract_address = ''
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

def homepage(request):
  return render(request, 'app/home.html')

# the following decorator allows to avoid 403 forbidden error since post methods is unsafe
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def test(request):
  try:
    print('-------------------------')
    result = json.loads(request.body)
    print(result)
    print(type(result))
    print(result['account'])
    print(type(result['account']))
    print('-------------------------')
    client.set("account", result['account'])
  except (ValueError, KeyError):
    raise ValueError('Invalid POST parameters')
  return JsonResponse({'result': result['account']})