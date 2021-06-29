from django.http import HttpResponse
from django.shortcuts import render,redirect

from . import models
from datetime import datetime, timezone
import pytz 

from rai_modules.rai_user.models import RAIUser
from django.contrib.auth.decorators import login_required

localtime = pytz.timezone('Asia/Bangkok')

@login_required
def home(request):
    return render(request,"rai_smartInventory/inventory/inventory_home.html")

##############################      Request List              ##################################
@login_required
def requestList(request):
    orders = models.Order.objects.filter(is_approved = 0).order_by('-id')
    orders_dict = []
    for order in orders:
        orders_dict.append(order.dict())
    
    return render(request,"rai_smartInventory/inventory/requestlist.html"
    ,{'orders':orders_dict})

@login_required
def itemOrderinside(request,order_id):
    orders = models.Order.objects.get(id=order_id)

    if request.method == 'POST' and 'approveOrder' in request.POST:
        pickup_date = request.POST.get('pickup_date')
        pickup_place = request.POST.get('pick-up-place')
        description = request.POST.get('description')
        is_approved_order = request.POST.get('is_approvedorder')

        pickup_date_obj = datetime.strptime(pickup_date,"%m/%d/%Y %I:%M %p")
        orders.pickup_date = localtime.localize(pickup_date_obj)

        orders.pickup_place = pickup_place
        orders.description = description

        orders.is_approved = True

        orders.save()

        print(orders.is_approved)
        print(orders.is_rejected)

        return redirect(requestList)

    if request.method == 'POST' and 'approveItem' in request.POST:
        which_item = request.POST.get('which_item')
        which_serial = request.POST.get('which_serial')
        is_approved = request.POST.get('is_approved')
        given_date = request.POST.get('given_date')
        return_date = request.POST.get('return_date')

        given_date_obj = datetime.strptime(given_date,"%m/%d/%Y %I:%M %p")
        return_date_obj = datetime.strptime(return_date,"%m/%d/%Y %I:%M %p")
        


        item = orders.items.get(id=which_item)
        outstock = models.Item.objects.get(id=which_serial)
        item.which_serial = outstock



        item.given_date = localtime.localize(given_date_obj)
        item.return_date = localtime.localize(return_date_obj)

        if is_approved == 'True':
            item.is_approved = True
            outstock.status = False
            outstock.is_assigned = True
            outstock.save()
        else:
            item.is_approved = False
        item.save()

    if request.method == 'POST' and 'rejectItem' in request.POST:
        which_item = request.POST.get('which_item')
        item = orders.items.get(id=which_item)
        item.is_rejected = True
        item.save()

    items = orders.items.all()
    itemlist = []
    is_showable = True
    reject_count = 0
    all_reject = False
    for item in items:
        item_available = models.Item.objects.filter(group=item.product,status=True)
        if (item.is_approved or item.is_rejected) != True:
            is_showable = False
        if item.is_rejected == True:
            reject_count = reject_count+1
        itemlist.append({
            'id':item.id,
            'product':item.product.dict(),
            'is_approved':item.is_approved,
            'is_rejected':item.is_rejected,
            'item_available':item_available,
            'which_serial':item.which_serial,
            'given_date':item.given_date.isoformat() if item.given_date != None else "",
            'return_date':item.return_date.isoformat() if item.return_date != None else "",
            'is_returned':item.is_returned,
        })
    if reject_count == items.count():
        all_reject = True
        orders.is_rejected = all_reject
        orders.save()
    return render(request,"rai_smartInventory/inventory/itemorderinside.html"
    ,{'items':itemlist,'order':orders.dict(),'is_showable':is_showable})



##############################      History              ##################################
@login_required
def showHistory(request):
    return render(request,"rai_smartInventory/inventory/history.html")

@login_required
def inventoryHistory(request):
    groupchanged = models.GroupofitemChanged.objects.all().order_by('-id')
    groupchanged_dict = []
    for changed in groupchanged:
        groupchanged_dict.append(changed.dict())
    return render(request,"rai_smartInventory/inventory/inventorychanged.html"
    ,{'groupchanged':groupchanged_dict})

@login_required
def requestlistHistory(request):
    orders = models.Order.objects.filter(is_approved = 1,is_returned=0,is_rejected=0).order_by('-id')
    orders_dict = []
    for order in orders:
        orders_dict.append(order.dict())
    return render(request,"rai_smartInventory/inventory/requestlist_history.html"
    ,{'orders':orders_dict})

@login_required
def iteminsiderequeslistHistory(request,order_id):
    orders = models.Order.objects.get(id=order_id)
    items = orders.items.filter(is_returned=0,is_rejected=0)

    if request.method == 'POST' and 'returnItem' in request.POST:
        which_item = request.POST.get('which_item')
        item = orders.items.get(id=which_item)
        serial = item.which_serial
        
        which_item = models.Item.objects.get(id=serial.id)
        which_item.status = True
        which_item.is_assigned = False

        item.is_returned = True

        which_item.save()
        item.save()
    
    if request.method == 'POST' and 'returnOrder' in request.POST:
        orders.is_returned = True
        orders.save()
        return redirect(requestlistHistory)
    
    itemlist = []
    is_showable = True
    for item in items:
        item_available = models.Item.objects.filter(group=item.product,status=True)
        if item.is_returned == False:
            is_showable = False
        itemlist.append({
            'id':item.id,
            'product':item.product.dict(),
            'is_approved':item.is_approved,
            'item_available':item_available,
            'which_serial':item.which_serial,
            'given_date':item.given_date.isoformat() if item.given_date != None else "",
            'return_date':item.return_date.isoformat() if item.return_date != None else "",
            'is_returned':item.is_returned,
        })
    return render(request,"rai_smartInventory/inventory/itemorderinsidehistory.html"
    ,{'items':itemlist,'order':orders.dict(),'is_showable':is_showable})

@login_required
def returnlistHistory(request):
    orders = models.Order.objects.filter(is_returned=1).order_by('-id')
    orders_dict = []
    for order in orders:
        orders_dict.append(order.dict())
    return render(request,"rai_smartInventory/inventory/returnlist.html"
    ,{'orders':orders_dict})

@login_required
def iteminsidereturnList(request,order_id):
    orders = models.Order.objects.get(id=order_id)
    items = orders.items.filter(is_rejected=False)
    itemlist = []
    for item in items:
        item_available = models.Item.objects.filter(group=item.product,status=True)
        itemlist.append({
            'id':item.id,
            'product':item.product.dict(),
            'is_approved':item.is_approved,
            'item_available':item_available,
            'which_serial':item.which_serial,
            'given_date':item.given_date.isoformat() if item.given_date != None else "",
            'return_date':item.return_date.isoformat() if item.return_date != None else "",
            'is_returned':item.is_returned,
        })
    return render(request,"rai_smartInventory/inventory/iteminsidereturnlist.html"
    ,{'items':itemlist,'order':orders.dict()})



##############################      Inventory management             ##################################
@login_required
def management(request): #For show all of group of item (click edit button to edit group of item, click on them to see item inside and also add category)
    groupofitems = models.GroupofItem.objects.all()
    groupofitems_dict = []
    for groupofitem in groupofitems:
        items = models.Item.objects.filter(group=groupofitem.id)
        count_available = 0
        for item in items:
            if item.status == True:
                count_available = count_available + 1
        if count_available == 0:
            groupofitem.status = False
            groupofitem.save()
        else:
            groupofitem.status = True
            groupofitem.save()
    groupofitems_dict.append(groupofitem.dict())
    return render(request,"rai_smartInventory/inventory/inventory_management.html",
        {'groupofitems':groupofitems_dict})

#These two is the same frist one will give item id = 0 and save, second will load information from id to edit.
@login_required
def addGroupofItem(request):
    return redirect(editGroupofItem,0)

@login_required
def editGroupofItem(request,group_id):
    if group_id == 0:
        group = models.GroupofItem()
        groupchanged = models.GroupofitemChanged()
        groupchanged.changetype = '1'
    else:
        group = models.GroupofItem.objects.get(id=group_id)
        groupchanged = models.GroupofitemChanged()
        groupchanged.changetype = '2'

    categories = models.Category.objects.all()
    categories_dict = []
    for category in categories:
        categories_dict.append(category.dict)
    
    if request.method == 'POST':
        if 'inpFile' in request.FILES:
            image = request.FILES["inpFile"]
            group.image.delete(save=True)
            group.image = image
        category = request.POST.get('categories')
        brand = request.POST.get('brand')
        series = request.POST.get('series')
        description = request.POST.get('description')
        status = request.POST.get('status')
        category_obj = models.Category.objects.get(id=category)
        group.category = category_obj
        group.series = series
        group.brand = brand
        group.description = description
        if status == 'True':
            group.status = True
        else:
            group.status = False
        groupchanged.group = str(brand)+'/'+str(series)
        group.save()
        groupchanged.save()
        return redirect(management)
    is_removable = models.Item.objects.filter(group=group).count()==0
    return render(request,"rai_smartInventory/inventory/addgroupofitem.html",{'group':group.dict(),'groupchanged':groupchanged.dict(),'categories':categories_dict,'remove':group_id,'is_removable':is_removable})

@login_required
def removeGroupofItem(request,group_id):
    group = models.GroupofItem.objects.get(id=group_id)
    brand = group.brand
    serie = group.series
    groupchanged = models.GroupofitemChanged()
    groupchanged.changetype = '3'
    groupchanged.group = str(brand)+'/'+str(serie)
    groupchanged.save()
    group.delete()
    return redirect(management)

@login_required
def addCategory(request):
    categories = models.Category.objects.all()
    categories_dict = []
    for category in categories:
        is_removable_dict = category.dict()
        is_removable_dict['is_removable'] = models.GroupofItem.objects.filter(category=category).count() == 0
        categories_dict.append(is_removable_dict)
    if request.method == 'POST':
        category = models.Category()
        newcategory = request.POST.get('newcategory')
        category.name = newcategory
        category.save()
        return redirect(addCategory)
    return render(request,"rai_smartInventory/inventory/addcategory.html",{
        'categories':categories_dict
    })

@login_required
def removeCategory(request,category_id):
    category = models.Category.objects.get(id=category_id)
    category.delete()
    return redirect(addCategory)

@login_required
def itemingroup(request,group_id): 
    group = models.GroupofItem.objects.get(id=group_id)
    items = models.Item.objects.all().filter(group=group_id)
    item_dict =[]
    for item in items:
        item_dict.append(item.dict())
    return render(request,"rai_smartInventory/inventory/iteminside.html",{
        'items':item_dict,
        'group':group.dict()
    })

@login_required
def addItem(request,group_id):
    return redirect(editItem,group_id,0)

@login_required
def editItem(request,group_id,item_id):
    group = models.GroupofItem.objects.get(id=group_id)
    if item_id == 0:
        item = models.Item()
        item.group = group 
    else:
        item = models.Item.objects.get(id=item_id)
    if request.method == 'POST':
        serial = request.POST.get('serial')
        cabinet = request.POST.get('cabinet')
        status = request.POST.get('status')
        item.serial = serial
        item.cabinet = cabinet
        item.status = status
        item.group = group
        if status == 'True':
            item.status = True
        else:
            item.status = False
        item.save()
        return redirect(itemingroup,group_id)
    return render(request,'rai_smartInventory/inventory/additem.html',{'remove':item_id,
    'group':group.dict(),
    'item':item.dict(),
    })

@login_required
def removeItem(request,group_id,item_id):
    item = models.Item.objects.get(id=item_id)
    item.delete()
    return redirect(itemingroup,group_id)

