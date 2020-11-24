from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import json
from django.contrib.auth.models import User
from .models import Article
from django.contrib.auth import logout

from django.db import transaction


def logout_view(request):
    request.session.flush()
    return redirect('/login')


def home(request):
    if request.user.is_authenticated:
        try:
            data = Article.objects.filter(author__id=request.user.id)
        except:
            data = None

        return render(request, 'home.html', {'data': data})
    else:
        return redirect('/login')


def upload(request):
    if request.user.is_superuser:
        if request.method == "GET":
            message = ''
            return render(request, 'upload.html', {'message': message})
        else:
            # read and save the file
            try:
                myfile = request.FILES['filename']
                fs = FileSystemStorage()
                fs.save(myfile.name, myfile)

                json_data = open(''+myfile.name)
                data1 = json.load(json_data)  # deserialises it
                json_data.close()
                if save_json(data1):
                    message = "Uploaded Successfully"
                else:
                    message = "Upload Failed or partially uploaded"
            except:
                message = "File Error"
            return render(request, 'upload.html', {'message': message})
    else:
        return redirect('/')


def save_json(data):

    try:
        Article.objects.all().delete()
    except:
        pass
    try:
        for d in data:
            new = Article(id=d['id'], title=d['title'],
                          body=d['body'], author=User.objects.get(id=d['userId']))
            new.save()
        return True
    except Exception as e:
        transaction.rollback()
        return False
