from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TodoTask
from django.core.serializers import serialize
from django.http import JsonResponse

# Create your views here.
@login_required(login_url='accounts/')
def home(request):
    user = request.user
    return render(request, 'home_task.html', {'user':user})

def get_tasks(request):
    if request.method == 'GET':
        user = request.user
        tasks = TodoTask.objects.filter(user=user)
        task_list = [{'id': task.id, 'title': task.title, 'description': task.description, 'color': task.color, 'due_date': task.due_date} for task in tasks]
        return JsonResponse(task_list, safe=False)

@login_required(login_url='accounts/')
def create_tasks(request):
    # print('create reached')
    if request.method == 'POST':
        # print('post reached')
        user = request.user
        title = request.POST.get('title')
        description = request.POST.get('description')
        color = request.POST.get('color')
        date = request.POST.get('due_date')
        task = TodoTask.objects.create(title=title,description=description,color=color,due_date=date,user=user)
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})

def get_task_id(request, id):
    try:
        task = TodoTask.objects.get(pk=id)
        serialized_task = serialize('json', [task])
        return JsonResponse({'taskInfo': serialized_task})
    except TodoTask.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

def update_task(request, id):
    if request.method == 'POST':
        try:
            task = TodoTask.objects.get(pk=id)
            if 'title' in request.POST:
                task.title = request.POST['title']
            if 'description' in request.POST:
                task.description = request.POST['description']
            if 'color' in request.POST:
                task.color = request.POST['color']
            if 'due_date' in request.POST:
                task.due_date = request.POST['due_date']
            task.save()
            return JsonResponse({'status': True})
        except TodoTask.DoesNotExist:
            return JsonResponse({'status': False, 'error': 'Task not found'})
    else:
        return JsonResponse({'status': False, 'error': 'Invalid request method'})

def delete_task(request,id):
    if request.method == 'GET':
        print('post reached')
        print(TodoTask.objects.get(pk=id))
        task = TodoTask.objects.get(pk=id)
        print('got task')
        task.delete()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})