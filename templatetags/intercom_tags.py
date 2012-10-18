import time

from django import template
from django.conf import settings
from django.utils import simplejson
from django.utils.hashcompat import sha_constructor

register = template.Library()

@register.inclusion_tag("intercom/_intercom_js.html")
def intercom_js(request):
	
	user = request.user
	
	if hasattr(settings, "INTERCOM_APP_ID") and user.is_authenticated():

		if hasattr(settings, "INTERCOM_USER_HASH_KEY"):

			user_hash = sha_constructor(settings.INTERCOM_USER_HASH_KEY + str(user.id)).hexdigest()

		else:

			user_hash = None
			
		custom_data = {}
			
		if hasattr(request, 'company'):
			
			company = request.company
			
			try:
			
				custom_data.update({
				
					'company_name' : company.company_name,
					
					'account_status' : company.account_status,
				
				})
	
			except AttributeError: pass
		
		return {
			
			"app_id": settings.INTERCOM_APP_ID,
			
			"email": user.email,
			
			'name' : user.get_full_name(),
			
			'user_id' : user.id,
			
			"user_hash": user_hash,
			
			"created_at": int(time.mktime(user.date_joined.timetuple())),
			
			"custom_data": simplejson.dumps(custom_data, ensure_ascii=False)
		}
		
	else:

		return {}
