from django.urls import path
from . import views

app_name = 'app'   

urlpatterns = [
  path('', views.homepage, name='homepage'),
  path('test', views.test, name='test'),
  path('new', views.new, name='new'),
  path('contribute', views.contribute, name='contribute'),
  # path('auctions/list', views.auctionsList, name='auctionsList'),
  # path('auctions/new', views.auctionNew, name='auctionNew'),
  # path('auctions/<int:pk>/detail', views.auctionDetail, name='auctionDetail'),
]
