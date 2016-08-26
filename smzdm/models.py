from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class case_info(models.Model):
    # Django auto add _id after filter
    case_id=models.AutoField(primary_key=True)
    e_mail=models.EmailField()
    type=models.SmallIntegerField()
    keyword=models.CharField(max_length=100)
    count=models.IntegerField(default=0)
    fromwhere=models.SmallIntegerField(default=0)

class filter(models.Model):
    # Django auto add _id after filter
    filter=models.ForeignKey(case_info)
    type=models.SmallIntegerField()
    keyword=models.CharField(max_length=100)

class his(models.Model):
    case=models.ForeignKey(case_info)
    article_id=models.CharField(max_length=50)
    timesort=models.BigIntegerField()
    user_email=models.EmailField()
    inserted_timesort=models.CharField(max_length=50,default=0)


class item(models.Model):
    article_id=models.CharField(max_length=50,blank=True,default=0)
    article_title=models.CharField(max_length=300,blank=True,default=0)
    brand=models.CharField(max_length=50,blank=True,default=0)
    # 这里从int改成char
    rmb_price=models.CharField(max_length=50,blank=True,default=0)
    article_price=models.CharField(max_length=200,blank=True,default=0)
    article_mall=models.CharField(max_length=50,blank=True,default=0)
    article_content=models.CharField(max_length=1000,blank=True,default=0)
    article_comment=models.IntegerField(blank=True,default=0)
    article_collection=models.IntegerField(blank=True,default=0)
    # 改为int
    worthy_percentage=models.IntegerField(blank=True,default=0)
    article_worthy=models.IntegerField(blank=True,default=0)
    article_unworthy=models.IntegerField(blank=True,default=0)
    article_rating=models.IntegerField(blank=True,default=0)
    price_dimension=models.CharField(max_length=50,blank=True,default=0)
    channel_dimension=models.CharField(max_length=50,blank=True,default=0)
    cates_str=models.CharField(max_length=100,blank=True,default=0)
    timesort=models.BigIntegerField(blank=True,default=0)
    article_url=models.CharField(max_length=200,blank=True,default=0)
    article_pic=models.CharField(max_length=200,blank=True,default=0)
    article_link=models.CharField(max_length=200,blank=True,default=0)
    article_data=models.CharField(max_length=100,blank=True,default=0)
    article_download_pic=models.CharField(max_length=100,blank=True,default=0)

class My_user(models.Model):
    user = models.OneToOneField(User)
    username=models.CharField(max_length=50,default='')
    register_ip=models.CharField(max_length=50,default='0.0.0.0')
    nick_name=models.CharField(max_length=50,default='')

    page_limit=models.SmallIntegerField(default=50)

    count=models.IntegerField(default=0)
    is_forbid=models.SmallIntegerField(default=0)
    is_superuser=models.SmallIntegerField(default=1)

    meta=models.CharField(max_length=1000,default='')


