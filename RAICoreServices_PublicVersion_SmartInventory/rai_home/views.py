from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from datetime import datetime

from rai_modules.rai_user.models import RAIUser
from rai_modules.rai_module_manager import models as ModuleManager

def handler404(request, *args, **argv):
	response = render(request, 'rai_home/404.html', {})
	response.status_code = 404
	return response
def handler500(request, *args, **argv):
	response = render(request, 'rai_home/500.html', {})
	response.status_code = 500
	return response

def home(request):
	raiuser = RAIUser.objects.getFromUser(request.user)
	return render(request,'rai_home/web_home.html',{
		'raiuser':raiuser,
		'users':[x.dict() for x in RAIUser.objects.all()],
		'widgets':range(0),
		'modules':ModuleManager.Module.objects.all_accessible_dict(raiuser=raiuser),
		})