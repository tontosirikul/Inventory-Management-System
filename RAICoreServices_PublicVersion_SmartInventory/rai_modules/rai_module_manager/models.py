from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import datetime, date, time, timedelta

import json

from rai_modules.rai_user.models import RAIUser

class Module_ModelManager(models.Manager):
	# def get_queryset(self):
		# return super().get_queryset().all()
	# def all(self,token=None):
	# 	if token == 'acie12c09eb2c9qwscad8dc67as6dcac':
	# 		return super().get_queryset().all()
	# 	return super().get_queryset().none()
	def all_admin_dict(self,raiuser=None):
		all_modules = super().get_queryset().all()
		modules = []
		for module in all_modules:
			if module.is_admin(raiuser):
				modules.append(module.dict())
		return modules
	
	def all_accessible_dict(self,raiuser=None):
		all_modules = super().get_queryset().all()
		modules = []
		for module in all_modules:
			if module.can_access(raiuser):
				module_dict = module.dict()
				module_dict['is_admin'] = module.is_admin(raiuser)
				modules.append(module_dict)
		return modules

class Module(models.Model):
	name		= models.CharField(max_length=30,unique=True,default='Untitled')
	description	= models.CharField(max_length=50)
	path		= models.CharField(max_length=20,blank=True)
	creator 	= models.ForeignKey(RAIUser,on_delete=models.CASCADE)
	created 	= models.DateTimeField(default=timezone.now)
	admin		= models.TextField(default='[]')
	is_show		= models.BooleanField(default=False)
	icon		= models.ImageField(upload_to='rai_module_manager/icon',null=True)
	
	ACCESSIBILITY = [
		('0', 'Nobody'),
		('1', 'Everyone'),
		('2', 'Login Required'),
		('3', 'Staff Only (Gen0)'),
	]
	accessibility = models.CharField(choices=ACCESSIBILITY,max_length=1,default='0')

	objects 	= Module_ModelManager()

	def dict(self):
		return {
			'id'			:self.id,
			'name'			:self.name,
			'description'	:self.description,
			'path'			:self.path,
			'creator'		:self.creator.id,
			'created'		:self.created.isoformat(),
			'admin'			:json.loads(self.admin),
			'is_show'		:self.is_show,
			'icon'			:str(self.icon),
			'accessibility'	:self.accessibility,
			'accessibility_str'	:self.get_accessibility_display(),
		}

	def is_admin(self,raiuser):
		if raiuser is None: return False
		return raiuser.id in json.loads(self.admin) or raiuser == self.creator
	def can_access(self,raiuser):
		if self.is_admin(raiuser): return True
		else:
			if self.accessibility == '0': return False
			elif self.accessibility == '1': return True
			elif self.accessibility == '2':  return raiuser != None
			elif self.accessibility == '3': 
				if raiuser != None: 
					return raiuser.generation == 0
				else:
					return False
		return False