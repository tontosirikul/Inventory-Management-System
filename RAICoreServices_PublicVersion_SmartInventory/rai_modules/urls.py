from django.urls import path

from django.urls import include, path

urlpatterns = [
	path('module_manager/',	include('rai_modules.rai_module_manager.urls')),
	path('user/', 			include('rai_modules.rai_user.urls')),

	# change this url to your app name
	path('exampleapp/', 	include('rai_modules.rai_exampleapp.urls')),
	path('smart_inventory/', 	include('rai_modules.rai_smartInventory.urls')),
]