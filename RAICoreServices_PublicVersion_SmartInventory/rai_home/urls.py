from django.urls import path

from . import views

urlpatterns = [
	path('404',views.handler404),
	path('500',views.handler500),

	path('',views.home,name='web_home'),
]
