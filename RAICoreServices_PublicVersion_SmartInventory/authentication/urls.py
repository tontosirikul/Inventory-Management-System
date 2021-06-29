from django.urls import path

from . import views

urlpatterns = [
	path('login',	views.authen_login, 			name='authen_login'),
	path('logout',	views.authen_logout, 			name='authen_logout'),
	path('info',	views.authen_info, 				name='authen_info'),
	path('password',views.authen_change_password, 	name='authen_change_password'),
]
