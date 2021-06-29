from django.urls import path

from . import views

urlpatterns = [
	path('',views.home),
	path('view/<int:id>/',views.view),
	path('view/<int:id>/remove',views.remove),
	path('view/<int:id>/removeicon',views.removeIcon),

	path('test/1',views.test1),
	path('test/2',views.test2),
	path('test/3',views.test3),


]