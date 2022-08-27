from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

# from flask import request, Flask, render_template
# app = Flask(__name__)

def homepage(request):
  return render(request, 'app/home.html')

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
  except (ValueError, KeyError):
    raise ValueError('Invalid POST parameters')
  # redirect("app:homepage")
  return JsonResponse({'result': result['account']})