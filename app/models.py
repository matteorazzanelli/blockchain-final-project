
from django.db import models
  
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
  id = models.FloatField(primary_key=True, blank=True, default=0)
  description = models.CharField(blank=True, max_length=500, default=' ')
  amount = models.FloatField(blank=True, default=0)
  biggest_for_now = models.FloatField()
  status = models.CharField(max_length=50, choices=STATUS, default='pending')