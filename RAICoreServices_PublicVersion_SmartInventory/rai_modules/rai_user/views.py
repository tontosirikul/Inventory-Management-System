from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect

import json

from rai_modules.rai_module_manager import models as ModuleManager
from rai_modules.rai_user.models import RAIUser

from rai_modules.rai_module_manager.decorator import raimodule_user_verify

@raimodule_user_verify(module_id=2)
def home(request):
	users = [x.dict() for x in RAIUser.objects.all()]
	return render(request,'rai_user/home.html',{
		'raiuser':RAIUser.objects.get(id=request.user.id) if request.user.is_authenticated else None,
		'users':users,
		'users_json':json.dumps(users),
		'users_key_list':RAIUser.SORT_LIST,
		'users_filter_list':RAIUser.filter_list_function(),
	})

@raimodule_user_verify(module_id=2)
def view(request,id):
	if id==0:
		request_raiuser = RAIUser.objects.getFromUser(request.user)
		if not ModuleManager.Module.objects.get(id=2).is_admin(request_raiuser): return redirect(home)
		raiuser = RAIUser()
	else:
		try: raiuser = RAIUser.objects.get(id=id)
		except: return redirect(home)
	if request.method == 'POST':
		raiuser.username			= request.POST.get('info-username')
		raiuser.first_name			= request.POST.get('info-first_name','')
		raiuser.last_name			= request.POST.get('info-last_name','')
		raiuser.nickname			= request.POST.get('info-nickname','')
		raiuser.email				= request.POST.get('info-email','')
		raiuser.phone				= request.POST.get('info-phone','')
		raiuser.line_userid			= request.POST.get('info-line_userid','')
		raw_generation 				= request.POST.get('info-generation','')
		raiuser.generation			= int(raw_generation) if raw_generation.isdigit() else None
		raiuser.is_active			= request.POST.get('info-is_active') == 'on'
		password = request.POST.get('info-password','')
		if password != '': raiuser.set_password(password)
		if 'info-image' in request.FILES:
			raiuser_img	= request.FILES['info-image']
			raiuser.image.delete(save=True)
			raiuser.image.save(str(raiuser.id)+'.'+str(raiuser_img).split('.')[1],raiuser_img)
		raiuser.save()
		return redirect(home)
	return render(request,'rai_user/view.html',{
		'raiuser':RAIUser.objects.get(id=request.user.id) if request.user.is_authenticated else None,
		'user':raiuser.dict(),
		'user_json':json.dumps(raiuser.dict()),
	})

@raimodule_user_verify(module_id=2)
def removeIcon(request,id):
	try: 
		user = RAIUser.objects.get(id=id)
		user.image.delete(save=True)
	except: pass
	return redirect(view,id)

@raimodule_user_verify(module_id=2)
def remove(request,id):
	try: 
		user = RAIUser.objects.get(id=id)
		user.delete()
	except: pass
	return redirect(home)

@login_required
def line_account_connection(request):
	raiuser = RAIUser.objects.getFromUser(request.user)
	if request.method == 'POST':
		raiuser.line_userid = request.POST.get('line-userId','')
		raiuser.save()
		return redirect('authen_login')
	return render(request,'rai_user/line_account_connection.html',{
		'raiuser':raiuser,
	})

@login_required
def line_account_disconnect(request):
	raiuser = RAIUser.objects.getFromUser(request.user)
	raiuser.line_userid = ''
	raiuser.save()
	return redirect('authen_login')

@csrf_exempt
def api(request):
	raiuser = None
	token = 'gNpYN4}-FZJ$weWvtyVFX0Xw9(F#n=5O'
	if request.method == 'POST':
		accessing_token = request.POST.get('token','')
		if 	token != accessing_token:
			return JsonResponse({'error','invalid token'}, safe=False)
		if 'line_userid' in request.POST:
			raiuser = RAIUser.objects.get(line_userid=request.POST['line_userid'])
	result = raiuser.dict() if raiuser is not None else None
	return JsonResponse(result, safe=False)