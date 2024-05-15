from django.shortcuts import render
from django.conf import settings
from .models import Blog
from django.db.models import Q
from accounts.models import blogchatUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os, ast, random, re
from chats.models import Topic

# Create your views here.
# shows all current blogs
@login_required(login_url='accounts/')
def blog_home(request):
    q = request.GET.get('q', '')
    blogs = Blog.objects.all()
    if q:
        blogs = blogs.filter(
            Q(topic__name__icontains=q) |
            Q(title__icontains=q)
        )
    for blog in blogs:
        if blog.images:
            blog_img_list = ast.literal_eval(blog.images)
            # Split the images string and getting the first element
            first_image_name = blog_img_list[0]
            setattr(blog, 'first_image', first_image_name)
    topics = Topic.objects.all()
    context = {'blogs':blogs,'topics':topics}
    return render(request,'blog_home.html',context)

# blog view.
def blog_view(request,id):
    blogInfo = Blog.objects.get(pk=id)
    context = {'blogTnfo':blogInfo}
    return render(request,'blog/blog_view.html',context)

# blog creation form
@login_required(login_url='accounts/')
def blog_create(request):
    topic_list = Topic.objects.all()
    return render(request,'blog/blog_create.html',{'topic_list':topic_list})

# blog saving procedure
def blog_saving(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        images = request.FILES.getlist('images')
        # userInfo = request.POST.get('request_user')
        topic_ids = request.POST.getlist('topic')
        userInfo = request.user

        new_title_img = re.sub(r'[^\w\s]', '', title).replace(" ", "")
        image_list = []

        # Saving the images and giving names
        for index, image in enumerate(images, start=1):
            _, extension = os.path.splitext(image.name)
            random_number = random.randint(1,1000000)
            image_name = f"{new_title_img}_{index}_{random_number}{extension}"
            image_list.append(image_name)
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            with open(image_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)

        # Save the blog entry
        image_list_str = str(image_list)
        blog = Blog.objects.create(title=title, content=content, images=image_list_str, user=userInfo)
        for topic_id in topic_ids:
            topic = Topic.objects.get(pk=topic_id)
            blog.topic.add(topic)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})