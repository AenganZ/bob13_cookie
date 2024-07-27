from django.shortcuts import render, redirect
from .models import User
from django.core.exceptions import ObjectDoesNotExist

import hashlib
import random

def index(request):
    cookie = request.COOKIES.get('session_id')
    context = {}
    
    if cookie:
            user = User.objects.get(sessionid = cookie)
            
            if user:
                context = {
                    'msg': 'qwer1234님 로그인 하셨습니다.',
                    'session': user.sessionid,
                    }
    
    else:
        context = {
            'msg': '로그인 해주세요.'
        }        
    
    return render(request, 'index.html', context)
    
    
def login(request):
    if request.method == "POST":
        userid = request.POST.get("userid")
        userpw = request.POST.get("userpw")
        
        try:
            user = User.objects.get(userid=userid)
            
            if user.userpw == userpw:
                if user.sessionid:
                    session_value = user.sessionid
                else:
                    session_value = create_session(user)
                    
                context = {
                    'session': session_value,
                    'msg': f'{user.userid}님이 로그인하셨습니다.'
                    }

                response = render(request, 'index.html', context) 
                response.set_cookie(key='session_id', value=session_value)                
                return response
            
            else:
                context = {'msg': "로그인에 실패했습니다."}
                return render(request, 'index.html', context)
            
        except ObjectDoesNotExist:
            context = {'msg': "로그인에 실패했습니다."}
            return render(request, 'index.html', context)
        
    return render(request, 'index.html')

def create_session(user):
    nonce = random.random()
    hash_value = (user.userid + user.userpw + str(nonce)).encode('utf-8')
    session = hashlib.sha256(hash_value).hexdigest()
    user.sessionid = session
    user.save()
    return session