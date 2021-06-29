from django.db import models
from datetime import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    last_edited = models.DateTimeField(auto_now=True)
    def dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'last_edited':self.last_edited.isoformat() if self.last_edited != None else '',
        }

class GroupofItem(models.Model):
    category = models.ForeignKey('Category',on_delete=models.PROTECT,null=True)
    brand = models.CharField(max_length=100,default='')
    series = models.CharField(max_length=100,default='')
    description = models.CharField(max_length=200,default='')
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='rai_smartInventory',null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    def dict(self):
        return{
            'id':self.id,
            'categories':self.category.name if self.category != None else '',
            'series':self.series,
            'brand':self.brand,
            'description':self.description,
            'status':'Available' if self.status == True else 'Not Available',
            'image':self.image,
            'created':self.created.isoformat() if self.created != None else '',
            'last_edited':self.last_edited.isoformat() if self.last_edited != None else '',
        }

class Item(models.Model):
    serial = models.CharField(max_length=100,default='')
    status = models.BooleanField(default=True)
    cabinet = models.CharField(max_length=100,default='')
    group = models.ForeignKey('GroupofItem',on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    is_assigned = models.BooleanField(default=False)
    def dict(self):
        return {
            'id':self.id,
            'group':self.group.id,
            'serial':self.serial,
            'status':'Available' if self.status == True else 'Not Available',
            'cabinet':self.cabinet,
            'created':self.created.isoformat() if self.created != None else '',
            'last_edited':self.last_edited.isoformat() if self.last_edited != None else '' ,
            'is_assigned':self.is_assigned
        }

class GroupofitemChanged(models.Model):
    typeofchanged = [
        ('1','Create'),
        ('2','Edit'),
        ('3','Remove')
    ]
    group = models.CharField(max_length=3,default='')
    changetype = models.CharField(max_length=1,choices=typeofchanged,default='0')
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    def dict(self):
        return {
            'id':self.id,
            'group':self.group,
            'type':self.get_changetype_display(),
            'created':self.created.isoformat() if self.created != None else '',
            'last_edited':self.last_edited.isoformat() if self.last_edited != None else '' ,
        }

# changes
class OrderItem(models.Model):
    product = models.ForeignKey(GroupofItem, on_delete=models.DO_NOTHING)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    which_serial = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    given_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)
    def __str__(self):
        return self.product


class Order(models.Model):
    owner = models.ForeignKey('rai_user.RAIUser', on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now_add=True)
    pickup_date = models.DateTimeField(blank=True, null=True)
    pickup_place = models.CharField(max_length=100,default='')
    description = models.CharField(max_length=100,default='')
    is_approved = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    demand_date = models.DateTimeField(blank=True, null=True)
    is_rejected = models.BooleanField(default=False)
    def get_cart_items(self):
        return self.items.all()
    def __str__(self):
        return '{0}'.format(self.owner)
    def dict(self):
        return {
            'id':self.id,
            'owner':self.owner,
            'date_ordered':self.date_ordered.isoformat() if self.date_ordered != None else '',
            'is_approved':'Approved' if self.is_approved == True else 'Declined',
            'pickup_date':self.pickup_date.isoformat() if self.pickup_date != None else '',
            'pickup_place':self.pickup_place,
            'description':self.description,
            'is_returned':self.is_returned,
            'demand_date':self.demand_date.isoformat() if self.demand_date != None else '',
            'is_rejected':self.is_rejected,
        }

