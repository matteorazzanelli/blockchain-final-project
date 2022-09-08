
from django.db import models

from django_ethereum.fields import EthereumAddressField
  
class AuctionModelForm(models.Model):

  TYPE = [
    ('new', 'new'),
    ('contribute', 'contribute'),
  ]
  STATUS = [
    ('pending', 'pending'),
    ('closed', 'closed'),
  ]
  
  type = models.CharField(max_length=50, choices=TYPE)
  id = models.IntegerField(primary_key=True, blank=True, default=0)
  beneficiary = EthereumAddressField(blank=True, default='0x0000000000000000000000000000000000000000')
  description = models.CharField(blank=True, max_length=500, default=' ')
  deadline = models.FloatField(blank=True, default=0) # since is unix epoch can be trated as float
  amount = models.FloatField(blank=True, default=0)
  biggest_for_now = models.FloatField()
  highest_bidder = EthereumAddressField(blank=True, default='0x0000000000000000000000000000000000000000')
  status = models.CharField(max_length=50, choices=STATUS, default='pending')