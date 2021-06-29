from django.shortcuts import render

from rai_modules.rai_module_manager import models as ModuleManager
from rai_modules.rai_user.models import RAIUser

from rai_modules.rai_module_manager.decorator import raimodule_user_verify

@raimodule_user_verify(module_id=3)
def home(request):
	raiuser = RAIUser.objects.getFromUser(request.user)
	return render(request,'rai_exampleapp/home.html',{
		'raiuser':raiuser,
	})

@raimodule_user_verify(module_id=3)
def page2(request):
	raiuser = RAIUser.objects.getFromUser(request.user)
	return render(request,'rai_exampleapp/page2.html',{
		'raiuser':raiuser,
	})

@raimodule_user_verify(module_id=3)
def page3(request):
	return render(request,'rai_exampleapp/page3.html')