from django.urls import path,include

from . import views
from . import views_client

urlpatterns = [
    path('admin/', views.home, name='home'),
    path('admin/requestlist/', views.requestList),
    path('admin/requestlist/<int:order_id>',views.itemOrderinside),

    path('admin/history/',views.showHistory),
    path('admin/history/inventoryhistory',views.inventoryHistory),
    path('admin/history/requestlisthistory',views.requestlistHistory),
    path('admin/history/requestlisthistory/<int:order_id>',views.iteminsiderequeslistHistory),
    path('admin/history/returnlist',views.returnlistHistory),
    path('admin/history/returnlist/<int:order_id>',views.iteminsidereturnList),

    path('admin/management/',views.management),
    path('admin/management/addgroupofitem',views.addGroupofItem),
    path('admin/management/editgroupofitem/<int:group_id>',views.editGroupofItem),
    path('admin/management/editgroupofitem/<int:group_id>/removegroup',views.removeGroupofItem),

    path('admin/management/addcategory/',views.addCategory),
    path('admin/management/addcategory/removeitem/<int:category_id>/',views.removeCategory),


    path('admin/management/<int:group_id>/',views.itemingroup),
    
    path('admin/management/<int:group_id>/additem',views.addItem),
    path('admin/management/<int:group_id>/edititem/<int:item_id>',views.editItem),
    path('admin/management/<int:group_id>/edititem/<int:item_id>/removeitem',views.removeItem),
    


    # Clients
    path('homepage/',views_client.index),
    path('homepage/<int:category_id>',views_client.categoriesList),
    path('homepage/checkout', views_client.your_cart),
    path('homepage/<int:category_id>/add_item/<int:groupofitem_id>', views_client.add_to_cart),
    path('homepage/success', views_client.submit_item),
    path('homepage/request', views_client.show_request),
    path('homepage/request/<int:order_id>',views_client.show_itemInOrder),
    path('homepage/checkout/<int:orderitem_id>/remove', views_client.remove_Item),
    # path('rai_smart_inventory/<int:category_id>',)

]