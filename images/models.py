from __future__ import unicode_literals
from django.db import models

class Tokens(models.Model):
	token = models.CharField(unique = True, primary_key = True, max_length= 20)

class Images(models.Model):
	token = models.CharField(max_length= 20)
	orignal_name = models.CharField(primary_key = True, max_length = 100)
	filename = models.CharField(unique = True, max_length = 100)
	path = models.CharField(max_length = 250)
	compression_percentage = models.FloatField(default = 0.0)