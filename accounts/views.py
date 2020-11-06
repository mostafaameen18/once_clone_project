from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import *
import string
from random import *


def checkAuthEmail(request):

	email = request.POST['email']
	print(email)

	if len(User.objects.filter(username=email)) > 0:
		user = User.objects.get(username=email)
	else:
		user = User.objects.create(username=email, email=email)
		user.first_name = "once"
		user.last_name = "clone"
		user.set_password("mostpass")
		user.save()

	
	letters = string.ascii_letters
	digits = string.digits
	chars = letters + digits
	min_length = 6
	max_length = 6
	code = "".join(choice(chars) for x in range(randint(min_length, max_length)))

	if len(hanguser.objects.filter(user=user)) > 0:
		insertuser = hanguser.objects.get(user=user)
		insertuser.code = code
		insertuser.save()
	else:
		insertuser = hanguser(user=user, code=code)
		insertuser.save()

	subject = 'Email verification link'
	message = 'Copy 6 digit number or follow the link bellow'
	msg_html = render_to_string('email.html', {'code': code})
	from_email = settings.EMAIL_HOST_USER
	to_list = [email, settings.EMAIL_HOST_USER]
	send_mail(subject, message, from_email, to_list, html_message=msg_html, fail_silently=False)
	res = redirect('verifyLogin')
	res.set_cookie('pendingEmail',email)
	return res


def resendVerificationEmail(request):

	if "pendingEmail" in request.COOKIES:
		email = request.COOKIES['pendingEmail']

		
		letters = string.ascii_letters
		digits = string.digits
		chars = letters + digits
		min_length = 6
		max_length = 6
		code = "".join(choice(chars) for x in range(randint(min_length, max_length)))		

		hunguser = hanguser.objects.get(user=User.objects.get(username=email))
		hunguser.code = code
		hunguser.save()

		subject = 'Email verification link'
		message = 'Copy 6 digit number or follow the link bellow'
		msg_html = render_to_string('email.html', {'code': code})
		from_email = settings.EMAIL_HOST_USER
		to_list = [email, settings.EMAIL_HOST_USER]
		send_mail(subject, message, from_email, to_list, html_message=msg_html, fail_silently=False)
		return redirect('verifyLogin')
	else:
		return HttpResponse('wrong email address')




def verifyLogin(request):
	email = request.COOKIES['pendingEmail']

	return render(request, 'verifyLogin.html', {'email':email})


def verifyLoginPro(request, code):
	if len(hanguser.objects.filter(code=code)) > 0:
		hunguser = hanguser.objects.get(code=code)
		user = hunguser.user
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request, user)
		hunguser.delete()
		return HttpResponse('done')
	else:
		return HttpResponse('wrong')


def verifyLoginRedirect(request, code):
	if len(hanguser.objects.filter(code=code)) > 0:
		hunguser = hanguser.objects.get(code=code)
		user = hunguser.user
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request, user)
		hunguser.delete()
		return redirect('storiesList')
	else:
		return redirect('storiesList')


