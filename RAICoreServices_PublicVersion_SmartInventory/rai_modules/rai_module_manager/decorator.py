from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

import json

from rai_modules.rai_user.models import RAIUser
from rai_modules.rai_module_manager import models as ModuleManager

def raimodule_user_verify(module_id=None,redirect_url='/'):
	def decorator(view_func):
		def wrap(request, *args, **kwargs):
			module = ModuleManager.Module.objects.get(id=module_id)
			raiuser = RAIUser.objects.getFromUser(request.user)
			if module.can_access(raiuser): return view_func(request, *args, **kwargs)
			return redirect(redirect_url)
		return wrap
	return decorator

def raimodule_user_isadmin(module_id=None,redirect_url='/'):
	def decorator(view_func):
		def wrap(request, *args, **kwargs):
			module = ModuleManager.Module.objects.get(id=module_id)
			raiuser = RAIUser.objects.getFromUser(request.user)
			if module.is_admin(raiuser): return view_func(request, *args, **kwargs)
			return redirect(redirect_url)
		return wrap
	return decorator