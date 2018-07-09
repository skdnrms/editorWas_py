import os
import requests, json
import zipfile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from .models import Post
from .forms import PostForm

def index(request):
    return render(request, 'testWas/index.html', {
        'post_list' : Post.objects.all(),
    })

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
    # with open('image/' + image.name, 'wb+') as destination:
    #     for chunk in image.chunks():
    #         destination.write(chunk)
    # return JsonResponse({
    #     'uploadPath' : request.build_absolute_uri('image/' + image.name)
    # })

@csrf_exempt
def importDoc(request):
    fileName = request.FILES['docFile'].name
    docFile = request.FILES['docFile'].file
    response = requests.post('http://synapeditor.iptime.org:8686/import', files = {'file': docFile})

    path = default_storage.save(fileName + '.zip', ContentFile(response.content))
    
    # zip 풀기
    zip_docFile = zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, path))
    zip_docFile.extractall(os.path.join(settings.MEDIA_ROOT, fileName))
    zip_docFile.close()

    # with open(os.path.join(settings.MEDIA_ROOT, fileName, 'document.word.pb'), 'r') as f:
    #     byte = f.read(1)
    #     while byte != b"":
    #         serializedData.push(byte)
    #         byte = f.read(1)

    # 바이너리 읽기
    serializedData = []
    with open(os.path.join(settings.MEDIA_ROOT, fileName, 'document.word.pb'), "rb") as f:
        content = f.read()   # 모두 읽음
        # for i in range(16, len(content)):
        #     serializedData.append(content[i])
        
        newFile = open(os.path.join(settings.MEDIA_ROOT, fileName, 'test.zip'), "wb")
        newFile.write(content[16:])

    zip_pbFile = zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, fileName, 'test.zip'))
    zip_pbFile.extractall(os.path.join(settings.MEDIA_ROOT, fileName, 'test'))
    zip_pbFile.close()

    with open(os.path.join(settings.MEDIA_ROOT, fileName, 'test'), "rb") as f:
        content = f.read()   # 모두 읽음
        for b in content:
            serializedData.append(b)

        # print(content[15])
        # for b in content:
        #     # "b'0xff'"
        #     serializedData.append(b)

    return JsonResponse({
        'serializedData' : serializedData,
        'importPath': ''
    })







# POST a Multipart-Encoded File
# 예1) 일반
# >>> url = 'http://httpbin.org/post'
# >>> files = {'file': open('report.xls', 'rb')}
# >>> r = requests.post(url, files=files)
# >>> r.text
# 예2) 타입 지정
# >>> url = 'http://httpbin.org/post'
# >>> files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
# >>> r = requests.post(url, files=files)
# >>> r.text

#     app.post('/getSerializedPbData', uploader.single('docFile'), (req, res) => {
#     const fileName = req.file.filename;
#     let rs = fs.createReadStream(path.join(__dirname, 'res', fileName));
#     let ws = fs.createWriteStream(path.join(__dirname, 'tmp', `${fileName}.zip`));
#     request.post('http://synapeditor.iptime.org:8686/import', {
#         formData: {
#             file: rs
#         }
#     }).pipe(ws);

#     ws.on('close', () => {
#         let serializedData = [];
#         const readStream = fs.createReadStream(path.join(__dirname, 'tmp', `${fileName}.zip`));
#         readStream.pipe(unzip.Extract({path: path.join(__dirname, 'tmp')})).on('close', () => {
#             fs.createReadStream(path.join(__dirname, 'tmp', 'document.word.pb'), {start: 16})
#             .pipe(zlib.createUnzip())
#             .on('data', (data) => {
#                 for (let i = 0, len = data.length; i < len; i++) {
#                     serializedData.push(data[i] & 0xFF);
#                 }
#             }).on('close', () => {
#                 res.json({serializedData: serializedData});
#                 res.end();
#             });
#         });
#     });
# });