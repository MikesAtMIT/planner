from django.shortcuts import render, redirect
from django.http import HttpResponse
from plans.models import *
import json


def index(request):
    # placeholder
    return redirect(calendar)


def calendar(request):
    dates = [
        date(2015,7,21),
        date(2015,7,22),
        date(2015,7,23),
        date(2015,7,24),
        date(2015,7,25),
        date(2015,7,26),
    ]

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
    tasks = Task.objects.all().exclude(status='D')
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
