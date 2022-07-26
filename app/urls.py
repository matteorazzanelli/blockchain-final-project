from django.urls import path
from . import views

app_name = 'app'   

urlpatterns = [
  path('', views.homepage, name='homepage'),
  # path('auctions/list', views.auctionsList, name='auctionsList'),
  # path('auctions/new', views.auctionNew, name='auctionNew'),
  # path('auctions/<int:pk>/detail', views.auctionDetail, name='auctionDetail'),
]
