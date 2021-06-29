from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from rai_modules.rai_user.models import RAIUser

def staff_check(user):
	return user.is_staff

def authen_login(request):
	login_msg = ""
	if request.method == 'POST':
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)
		remember = request.POST.get('remember',False)
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if remember:
				request.session.set_expiry(30*24*60*60) # a month
			else:
				request.session.set_expiry(24*60*60) # 1 day
			next = request.GET.get('next', '/')
			return redirect(next)
		else:
			# login_msg = "Invalid login"
			login_msg = "Username or Password is invalid"
	raiuser = RAIUser.objects.getFromUser(request.user)
	if request.user.is_authenticated:
		login_msg = "You are already logged in"
	return render(request,"authen_login.html",{'login_msg':login_msg,'raiuser':raiuser})


def authen_logout(request):
	logout(request)
	return redirect(authen_login)

@login_required
def authen_change_password(request):
	messages = ""
	if request.method == 'POST':
		current_password 	= request.POST['current_password']
		new_password 		= request.POST['new_password']
		confirm_password 	= request.POST['confirm_password']
		is_valid = request.user.check_password(current_password)
		if not is_valid:
			messages = "The current password is incorrect"
		else:
			if len(new_password) < 8:
				messages = "New password must be more than 8 characters"
			else:
				if new_password != confirm_password:
					messages = "The confirm password does not match"
				else:
					request.user.set_password(new_password)
					request.user.save()
					return redirect(authen_login)
	return render(request,"authen_password.html",{'messages':messages})

def authen_info(request):
	raiuser = RAIUser.objects.getFromUser(request.user)
	if request.method == 'POST':
		raiuser.first_name			= request.POST.get('info-first_name','No Name')
		raiuser.last_name			= request.POST.get('info-last_name','')
		raiuser.nickname			= request.POST.get('info-nickname','')
		raiuser.email				= request.POST.get('info-email','')
		raiuser.phone				= request.POST.get('info-phone','')
		raiuser.line_id				= request.POST.get('info-line_id','')
		raiuser.save()
		return redirect(authen_login)
	return render(request,"authen_info.html",{'raiuser':raiuser})