from django.urls import path

from . import views

# you can add any url that you want in your app
urlpatterns = [
	path('',views.home),
	path('page2',views.page2),
	path('page3',views.page3),
]