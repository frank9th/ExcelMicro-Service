from django.db import models



class File(models.Model):
	name = models.CharField(max_length=150)
	sector = models.CharField(max_length=200)
	upload_at = models.DateTimeField(auto_now_add=True)
	xlsx = models.FileField(upload_to='files/xlsx/',)

	def __str__(self):
		return self.name 



# Create your models here.
