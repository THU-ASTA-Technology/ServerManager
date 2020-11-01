from django.http import HttpResponse
from django.shortcuts import render, redirect
import crypto
from ServerManager import settings
from datetime import datetime, timedelta
import subprocess
import string
import random
import datetime
from database.models import Reservation

def changePassword(username):
    passwd = ''.join([random.choice(string.ascii_letters) for i in range(16)])

    control = subprocess.run("echo '%s\n%s' | sudo passwd %s" %(passwd,passwd,username), shell = True)
    assert control.returncode == 0
    return passwd

def submitToken(request):
    aes = crypto.myAES(key = settings.RESERVATION_TOKEN_KEY, iv = settings.RESERVATION_TOKEN_IV)
    try:
        startTime, endTime = aes.decrypt(request.GET['token'])
        #return HttpResponse(startTime.timestamp())
        assert(startTime <= datetime.datetime.now())
        assert(endTime >= datetime.datetime.now())
    except:
        return HttpResponse('Token error.', status = 400)

    dataList = Reservation.objects.all()
    for item in dataList:
        changePassword(item.username)
        item.delete()

    username = 'user_%03d'%random.randint(0,99)
    try:
        passwd = changePassword(username)
    except:
        return HttpResponse('System error.', status = 400)
    
    Reservation.objects.create(startTime = startTime, endTime = endTime, username = username)
    
    res = '{username:%s, password: %s}'%(username, passwd)

    #return HttpResponse(res, content_type = 'application/json')
    return HttpResponse('username:  %s<br>password:  %s'%(username, passwd))

def checkTimeUp():
    dataList = Reservation.objects.filter(endTime__lte = datetime.datetime.now())
    for item in dataList:
        changePassword(item.username)
        item.delete()

