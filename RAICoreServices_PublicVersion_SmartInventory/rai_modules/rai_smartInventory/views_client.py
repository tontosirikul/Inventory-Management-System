from django.http import HttpResponse
from django.shortcuts import render, redirect

from . import models
# change
from datetime import datetime, timezone
from rai_modules.rai_user.models import RAIUser
from django.contrib.auth.decorators import login_required
import pytz 
localtime = pytz.timezone('Asia/Bangkok')

@login_required
def index(request):
    categories = models.Category.objects.all()
    categories_dict = []
    for category in categories:
        categories_dict.append(category.dict)
    return render(request,"rai_smartInventory/client_inventory/index.html",{'categories':categories})

@login_required
def categoriesList(request, category_id):
    groupofitems = models.GroupofItem.objects.all().filter(category = category_id)
    groupofitems_dict = []
    for groupofitem in groupofitems:
        groupofitems_dict.append(groupofitem.dict())

    return render(request,"rai_smartInventory/client_inventory/item_name.html",{'groupofitems':groupofitems_dict, 'category_id':category_id})

# changes
@login_required
def your_cart(request):
    raiuser = RAIUser.objects.getFromUser(request.user)
    order = models.Order.objects.filter(owner = raiuser, is_ordered = False)
    if (len(order)==0):
        order = models.Order()
        order.owner = raiuser
        Items = []
    else:
        order = order[0]
        items = order.items.all()

     #changes for date and time below 
    order.save()
    items = order.items.all()
    if request.method == 'POST':
        demand_date = request.POST.get('demand_date')
        demand_date_obj = datetime.strptime(demand_date,"%m/%d/%Y %I:%M %p")
        order.demand_date = localtime.localize(demand_date_obj)
        order.save()
        return redirect(submit_item)
    return render(request, "rai_smartInventory/client_inventory/checkout.html", {'items':items})
    #end of changes
@login_required
def add_to_cart(request, groupofitem_id, category_id):
    raiuser = RAIUser.objects.getFromUser(request.user)
    group_of_item = models.GroupofItem.objects.filter(id = groupofitem_id)
    if (len(group_of_item)>0):
        group_of_item = group_of_item[0]    
        order = models.Order.objects.filter(owner = raiuser, is_ordered = False)
        if (len(order)==0):
            order = models.Order()
            order.owner = raiuser
        else:
            order = order[0]
        order.save()
        orderitem = models.OrderItem()
        orderitem.product = group_of_item
        orderitem.save()
        order.items.add(orderitem)

    return redirect(your_cart)

@login_required
def remove_Item(request, orderitem_id):
    raiuser = RAIUser.objects.getFromUser(request.user)
    orderitem = models.OrderItem.objects.filter(id = orderitem_id)
    orderitem.delete()
    return redirect(your_cart)

@login_required
def submit_item(request):
    raiuser = RAIUser.objects.getFromUser(request.user)
    order = models.Order.objects.filter(owner = raiuser, is_ordered = False)
    if(len(order)>0):
        order = order[0]
        order.is_ordered = True
        order.save()

    return render(request, "rai_smartInventory/client_inventory/success.html")

@login_required
def show_request(request):
    raiuser = RAIUser.objects.getFromUser(request.user)
    orders = models.Order.objects.filter(owner = raiuser, is_ordered = True)
    orders_dict = []
    for order in orders:
        orders_dict.append(order.dict())
    
    return render(request,"rai_smartInventory/client_inventory/request.html"
    ,{'orders':orders_dict})

@login_required
def show_itemInOrder(request, order_id):
    raiuser = RAIUser.objects.getFromUser(request.user)
    orders = models.Order.objects.get(id=order_id)
    items = orders.items.all()
    itemlist = []

    for item in items:
        item_available = models.Item.objects.filter(group=item.product)
        itemlist.append({
            'id':item.id,
            'is_rejected':item.is_rejected,
            'is_returned':item.is_returned,
            'product':item.product.dict(),
            'is_approved':item.is_approved,
            'item_available':item_available,
            'which_serial':item.which_serial,
            'given_date':item.given_date.isoformat() if item.given_date != None else "",
            'return_date':item.return_date.isoformat() if item.return_date != None else "",
            'is_returned':item.is_returned,
        })

    return render(request,"rai_smartInventory/client_inventory/requestItem.html",{'items':itemlist,'order':orders.dict()})
