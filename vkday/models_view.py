from .models import *

# Create your models here.
class Onedayk(models.Model):
    vdate = models.DateField()
    vtext = models.CharField(max_length=1024)
    class Meta:
        db_table = 'viewrecommend'

class Vkdayn(models.Model):
    vdate = models.DateField()
    vtext = models.CharField(max_length=2048)
    class Meta:
        db_table = 'recommend_vkdayn'        