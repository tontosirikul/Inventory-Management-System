from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from rai_modules.rai_module_manager.decorator import raimodule_user_verify
from rai_modules.rai_module_manager.decorator import raimodule_user_isadmin

import json

from rai_modules.rai_user.models import RAIUser
from rai_modules.rai_module_manager import models as ModuleManager

@login_required
def home(request):
	raiuser = RAIUser.objects.getFromUser(request.user)
	return render(request,'rai_module_manager/home.html',{
		'raiuser':raiuser,
		'users':[x.dict() for x in RAIUser.objects.all()],
		'modules':ModuleManager.Module.objects.all_admin_dict(raiuser=raiuser),
		'is_admin':ModuleManager.Module.objects.get(id=1).is_admin(raiuser),
		})

@login_required
def view(request,id):
	raiuser = RAIUser.objects.getFromUser(request.user)
	if id == 0:
		# check user is admin of ModuleManager or not
		if not ModuleManager.Module.objects.get(id=1).is_admin(raiuser): return redirect(home)
		module = ModuleManager.Module()
		module.creator = raiuser
	else:
		try: module = ModuleManager.Module.objects.get(id=id)
		except: return redirect(home)
	if request.method == 'POST':
		if not module.is_admin(raiuser): return redirect(home)
		module.name			= request.POST.get('info-name','Untitled')
		module.description	= request.POST.get('info-description','No description')
		module.path			= request.POST.get('info-path','/')
		module.admin		= request.POST.get('info-admin','[]')
		module.is_show		= request.POST.get('info-is_show') == 'on'
		module.accessibility= request.POST.get('info-accessibility','0')
		if 'info-icon' in request.FILES:
			icon_img	= request.FILES['info-icon']
			module.icon.delete(save=True)
			module.icon.save(str(module.id)+'.'+str(icon_img).split('.')[1],icon_img)
		module.save()
		return redirect(home)
	users = [x.dict() for x in RAIUser.objects.all()]
	return render(request,'rai_module_manager/view.html',{
		'raiuser':raiuser,
		'module':module.dict(),
		'module_json':json.dumps(module.dict()),
		'module_accessibility_list':ModuleManager.Module.ACCESSIBILITY,
		'users':users,
		'users_json':json.dumps(users),
		'users_key_list':RAIUser.SORT_LIST,
		'users_filter_list':RAIUser.filter_list_function(),
	})

@login_required
@raimodule_user_isadmin(1)
def removeIcon(request,id):
	try: 
		module = ModuleManager.Module.objects.get(id=id)
		module.icon.delete(save=True)
	except: pass
	return redirect(view,id)

@login_required
@raimodule_user_isadmin(1)
def remove(request,id):
	try: 
		module = ModuleManager.Module.objects.get(id=id)
		module.delete()
	except: pass
	return redirect(home)

@raimodule_user_verify(module_id=4)
def test1(request):
	return HttpResponse('modulemanager_test1')

@raimodule_user_verify(module_id=5)
def test2(request):
	return HttpResponse('modulemanager_test2')

@raimodule_user_verify(module_id=6)
def test3(request):
	return HttpResponse('modulemanager_test3')
