import os
import requests, json
import zipfile
import zlib  
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from .models import Post
from .forms import PostForm, PageForm

def index(request):
    return render(request, 'testWas/index.html', {
        'post_list' : Post.objects.all(),
    })

def froala(request):
    return render(request, 'testWas/froala.html', {'form': PageForm()})

def edit(request):
    if request.method == "POST":
        id = request.POST['id']
        if id != '-1':
            post = get_object_or_404(Post, pk=id)
            form = PostForm(request.POST, instance=post)
        else :
            form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/')
            # return redirect('edit?id=' + id)
    else:
        id = request.GET['id']
        if id != '-1':
            post = Post.objects.get(id=id)
            form = PostForm(instance=post)
        else :
            post = {"id": id}
            form = PostForm()
    return render(request, 'testWas/edit.html', {'post' : post, 'form': form})

@csrf_exempt
def upload(request):
    imageName = request.FILES['file'].name
    path = default_storage.save(imageName, request.FILES['file'])
    return JsonResponse({
        'uploadPath' : request.build_absolute_uri('image/' + imageName)
    })

@csrf_exempt
def importDoc(request):
    fileName = request.FILES['docFile'].name
    docFile = request.FILES['docFile'].file
    response = requests.post('http://synapeditor.iptime.org:8686/import', files = {'file': docFile})

    path = default_storage.save(fileName, ContentFile(response.content))
    result_fileName = path.split('.')[0]

    # 파일압축풀기
    zip_docFile = zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, path))
    zip_docFile.extractall(os.path.join(settings.MEDIA_ROOT, result_fileName))
    zip_docFile.close()

    # pb압축풀기
    with open(os.path.join(settings.MEDIA_ROOT, result_fileName, 'document.word.pb'), "rb") as f:
        bytes_data = f.read()
        data = zlib.decompress(bytes_data[16:])

        # 바이너리 읽기
        serializedData = []
        for b in data:
            serializedData.append(b)

    return JsonResponse({
        'serializedData' : serializedData,
        'importPath': settings.MEDIA_URL + result_fileName
    })
