from .models import *

# Create your models here.
class Onedayk(models.Model):
    vdate = models.DateField()
    vtext = models.CharField(max_length=1024)
    class Meta:
        db_table = 'v1'