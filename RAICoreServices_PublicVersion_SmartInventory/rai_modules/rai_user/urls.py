from django.urls import path

from . import views

urlpatterns = [
	path('',views.home),
	path('view/<int:id>/',views.view),
	path('view/<int:id>/remove',views.remove),
	path('view/<int:id>/removeimage',views.removeIcon),

	path('line_account_connection',views.line_account_connection),
	path('line_account_disconnect',views.line_account_disconnect),

	path('api',views.api),
]
