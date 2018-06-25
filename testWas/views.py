from django.shortcuts import render, redirect, get_object_or_404
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