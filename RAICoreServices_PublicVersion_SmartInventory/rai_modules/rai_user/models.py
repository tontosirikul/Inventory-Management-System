from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import datetime, date, time, timedelta

from django.db.models import Max,Min
# change
from rai_modules.rai_smartInventory.models import GroupofItem

class RAIUser_ModelManager(models.Manager):
	def getFromUser(self,user):
		if not user.is_authenticated or user is None: return None
		return super().get_queryset().get(id=user.id)

class RAIUser(User):
	nickname 		= models.CharField(max_length=10, blank=True)
	phone 			= models.CharField(max_length=10, blank=True)
	generation		= models.IntegerField(default=0)
	image			= models.ImageField(upload_to='rai_user/image',default='')
	line_userid		= models.CharField(max_length=50, blank=True)

	objects 		= RAIUser_ModelManager()
	# change
	cart			= models.ManyToManyField(GroupofItem, blank=True)

	def __str__(self):
		return str(self.user_ptr)
	def dict(self):
		return {
			'id'			:self.id,
			'username'		:self.username,
			'first_name'	:self.first_name,
			'last_name'		:self.last_name,
			'nickname'		:self.nickname,
			'email'			:self.email,
			'last_login'	:self.last_login.isoformat() if self.last_login != None else None,
			'phone'			:self.phone,
			'line_userid'	:self.line_userid,
			'generation'	:self.generation,
			'is_staff'		:self.is_staff,
			'is_active'		:self.is_active,
			'image'			:str(self.image),
		}
	SORT_LIST = [
		{ 'key':'username','display':'Username'},
		{ 'key':'first_name','display':'First Name'},
		{ 'key':'last_name','display':'Last Name'},
		{ 'key':'nickname','display':'Nickname'},
		{ 'key':'generation','display':'Generation'}
	]

	def filter_list_function():
		users_filter_list = [{ 'key':'all','display':'All users'}]
		for x in range(
		RAIUser.objects.aggregate(Min('generation'))['generation__min'],
		RAIUser.objects.aggregate(Max('generation'))['generation__max']+1):
			users_filter_list.append({
				'key':'generation_'+str(x),
				'display':'Generation '+str(x)
				})
		return users_filter_list
