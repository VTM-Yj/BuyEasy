from django.db import models

# Create your models here.
class Area(models.Model):
    area_id = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=50)
    parent_id = models.IntegerField()
    area_level = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area'

class UserInfo(models.Model):
    user_name = models.EmailField(max_length=100)
    pwd = models.CharField(max_length=100)

    def __str__(self):
        return f'<UserInfo:{self.user_name}>'

class Address(models.Model):
    consignee = models.CharField(max_length=30)
    consignee_phone = models.CharField(max_length=10)
    addr = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f'<Address:{self.consignee}>'

