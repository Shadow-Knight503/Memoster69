from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import MemeImg
from .forms import PostImg


# Create your views here.
def home(request):
    imgs = MemeImg.objects.all()
    ctx = {'imgs': imgs}
    return render(request, 'Home.html', ctx)


def post(request):
    if request.method == 'POST':
        form = PostImg(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('https://youtu.be/dQw4w9WgXcQ')
    form = PostImg()
    ctx = {'form': form}
    return render(request, 'Post.html', ctx)
