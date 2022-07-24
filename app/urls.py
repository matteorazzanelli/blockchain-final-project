from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
  # app
  path('', views.homepage, name="homepage"),
  path('orders', views.all_orders, name="view_all_orders"),
]    