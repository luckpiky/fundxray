from django.db import models

class FundInfo(models.Model):
	name = models.CharField(max_length = 64)
	code = models.CharField(max_length = 32)
	company = models.CharField(max_length = 64)
	type1 = models.CharField(max_length = 64)

	def __unicode__(self):
		return self.name

