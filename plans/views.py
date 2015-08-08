from django.shortcuts import render, redirect
from django.http import HttpResponse
from plans.models import *
from datetime import date, timedelta
import json


def index(request):
    # placeholder
    return redirect(calendar)


def calendar(request, d1=None, d2=None):

    if d1 is None and d2 is None:
        # with no date range specified, default is today +/- 15 days
        start_date = date.today() - timedelta(days=15)
        end_date = date.today() + timedelta(days=15)
    else:
        # use specified date range
        start_date = date(int(d1[0:4]), int(d1[4:6]), int(d1[6:8]))
        end_date = date(int(d2[0:4]), int(d2[4:6]), int(d2[6:8]))
    
    time_diff = (end_date - start_date).days
    dates = [start_date + timedelta(days=x) for x in range(0, time_diff+1)]

    projects = Project.objects.all().exclude(status='D')

    experiments = Experiment.objects.all().exclude(status='D')
    experiment_list = [e for e in experiments]

    '''
    structure of the data variable:
    data = [
        {
            date: date,
            tasks: [
                { experiment_id: id, task_list: []},
                { experiment_id: id, task_list: []},
                { experiment_id: id, task_list: [task]},
                { experiment_id: id, task_list: []},
                { experiment_id: id, task_list: [task,task]},
            ]
        }
    ]
    '''

    data = []
    for d in dates:
        datum = {
            'date': d,
            'tasks': [{ 'experiment_id': e.id, 'task_list': []} for e in experiments],
        }
        data.append(datum)
    tasks = Task.objects.all().exclude(status='D').filter(date__in=dates)
    for task in tasks:
        date_index = dates.index(task.date)
        experiment_index = experiment_list.index(task.experiment)
        data[date_index]['tasks'][experiment_index]['task_list'].append(task)

    context = {
        'projects': projects,
        'experiments': experiment_list,
        'data': data,
        'dates': dates,
    }
    return render(request, 'planner-table.html', context)


def toggle_task(request):
    # ajax endpoint for completing a task
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        action = request.POST.get('action')
        task = Task.objects.get(pk=task_id)
        if action == task.status:
            task.status = 'O'
        else:
            task.status = action
        task.save()
        result = {
            'task_id': task.id,
            'status': task.status,
        }
        return HttpResponse(json.dumps(result))


def delete_task(request):
    # ajax endpoint for deleting a task
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = Task.objects.get(pk=task_id)
        task.status = 'D'
        task.save()
        result = {
            'task_id': task.id,
            'status': task.status,
        }
        return HttpResponse(json.dumps(result))


def save_new_task(request):
    # ajax endpoint for saving a new task
    if request.method == 'POST':
        experiment = request.POST.get('task_experiment')
        name = request.POST.get('task_name')
        date = request.POST.get('task_date')
        notes = request.POST.get('task_notes')
        task = Task(name=name, notes=notes, experiment_id=experiment, date=date)
        task.save()
        result = {
            'id': task.id,
            'name': task.name,
            'experiment': task.experiment_id,
            'date': task.date,
            'notes': task.notes,
            'status': task.status,
        }
        return HttpResponse(json.dumps(result))

def update_task(request):
    # ajax endpoint for updating a task
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        experiment = request.POST.get('task_experiment')
        name = request.POST.get('task_name')
        date = request.POST.get('task_date')
        notes = request.POST.get('task_notes')

        task = Task.objects.get(pk=task_id)
        task.name = name
        task.experiment_id = experiment
        task.date = date
        task.notes = notes
        task.save()

        result = {
            'id': task.id,
            'name': task.name,
            'experiment': task.experiment_id,
            'date': task.date,
            'notes': task.notes,
            'status': task.status,
        }
        return HttpResponse(json.dumps(result))
