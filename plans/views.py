from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from plans.models import *
from plans.forms import NewProjectForm

from datetime import date, timedelta
import json


def index(request):
    # placeholder
    return redirect(calendar)


@login_required(login_url='/sign-in/')
def calendar(request):

    users = request.GET.getlist('users')
    projects = request.GET.getlist('projects')
    start_date_input = request.GET.get('start-date')
    end_date_input = request.GET.get('end-date')
    
    if start_date_input is None and end_date_input is None:
        # with no date range specified, default is today +/- 14 days
        start_date = date.today() - timedelta(days=14)
        end_date = date.today() + timedelta(days=14)
    else:
        # use specified date range
        d1 = start_date_input.split('-')
        d2 = end_date_input.split('-')
        start_date = date(int(d1[0]), int(d1[1]), int(d1[2]))
        end_date = date(int(d2[0]), int(d2[1]), int(d2[2]))
    
    time_diff = (end_date - start_date).days
    dates = [start_date + timedelta(days=x) for x in range(0, time_diff+1)]

    if len(projects) == 0:
        project_list = Project.objects.filter(contributors__user=request.user).exclude(status='D')
    else:
        project_list = Project.objects.filter(pk__in=projects)

    experiments = Experiment.objects.exclude(status='D').filter(project__in=project_list).order_by('-status','-order')
    experiment_list = []
    for e in experiments:
        if e.status == 'O':
            experiment_list.append(e)
        else:
            for task in e.task_set.all():
                if task.date in dates:
                    experiment_list.append(e)
                    break

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
    today = date.today()
    data = []
    for d in dates:
        datum = {
            'date': d,
            'tasks': [{ 'experiment_id': e.id, 'task_list': []} for e in experiment_list],
        }
        if d == today:
            datum['today'] = True
        data.append(datum)
    tasks = Task.objects.exclude(status='D').filter(date__in=dates).filter(experiment__in=experiment_list)
    for task in tasks:
        date_index = dates.index(task.date)
        experiment_index = experiment_list.index(task.experiment)
        data[date_index]['tasks'][experiment_index]['task_list'].append(task)

    context = {
        'all_projects': Project.objects.exclude(status='D'),     # for nav menu
        'projects': project_list,
        'experiments': experiment_list,
        'data': data,
        'dates': dates,
        'all_users': User.objects.all(),
    }
    return render(request, 'planner-table.html', context)


@login_required(login_url='/sign-in/')
def new_project(request):
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            objective = form.cleaned_data['objective']
            notes = form.cleaned_data['notes']
            user = request.user

            new_project = Project(
                name=name,
                objective=objective,
                notes=notes,
            )
            new_project.save()
            new_project.contributors.add(user.userprofile)
            new_project.save()

            return HttpResponseRedirect(reverse('confirm-project'))
    else:
        form = NewProjectForm()
    return render(request, 'new-project.html', { 'form': form })


@login_required(login_url='/sign-in/')
def confirm_project(request):
    return render(request, 'confirm-project.html')


@login_required(login_url='/sign-in/')
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


@login_required(login_url='/sign-in/')
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


@login_required(login_url='/sign-in/')
def save_new_task(request):
    # ajax endpoint for saving a new task
    if request.method == 'POST':
        experiment = request.POST.get('task_experiment')
        name = request.POST.get('task_name')
        date = request.POST.get('task_date')
        notes = request.POST.get('task_notes')
        contributors = request.POST.getlist('task_contributors')
        
        task = Task(name=name, notes=notes, experiment_id=experiment, date=date)
        task.save()
        for contributor in contributors:
            user = User.objects.get(pk=int(contributor))
            task.contributors.add(user.userprofile)
        task.save()

        result = {
            'id': task.id,
            'name': task.name,
            'experiment': task.experiment_id,
            'date': task.date,
            'notes': task.notes,
            'status': task.status,
            'contributor_initials_list': task.contributor_initials_list,
            'contributor_id_list': task.contributor_id_list,
        }
        return HttpResponse(json.dumps(result))


@login_required(login_url='/sign-in/')
def update_task(request):
    # ajax endpoint for updating a task
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        experiment = request.POST.get('task_experiment')
        name = request.POST.get('task_name')
        date = request.POST.get('task_date')
        notes = request.POST.get('task_notes')
        contributors = request.POST.getlist('task_contributors')

        task = Task.objects.get(pk=task_id)
        task.name = name
        task.experiment_id = experiment
        task.date = date
        task.notes = notes
        task.contributors.clear()
        for contributor in contributors:
            user = User.objects.get(pk=int(contributor))
            task.contributors.add(user.userprofile)

        task.save()

        result = {
            'id': task.id,
            'name': task.name,
            'experiment': task.experiment_id,
            'date': task.date,
            'notes': task.notes,
            'status': task.status,
            'contributor_initials_list': task.contributor_initials_list,
            'contributor_id_list': task.contributor_id_list,
        }
        return HttpResponse(json.dumps(result))


@login_required(login_url='/sign-in/')
def save_new_experiment(request):
    # ajax endpoint for saving a new experiment
    if request.method == 'POST':
        project = request.POST.get('experiment_project')
        name = request.POST.get('experiment_name')
        objective = request.POST.get('experiment_objective')
        notes = request.POST.get('experiment_notes')
        experiment = Experiment.objects.create_experiment(name=name, objective=objective, notes=notes, project_id=project)
        experiment.save()
        result = {
            'id': experiment.id,
            'name': experiment.name,
            'project_id': experiment.project.id,
            'project': experiment.project.name,
            'objective': experiment.objective,
            'notes': experiment.notes,
            'status': experiment.status,
            'order': experiment.order,
        }
        return HttpResponse(json.dumps(result))


@login_required(login_url='/sign-in/')
def update_experiment(request):
    # ajax endpoint for updating an experiment
    if request.method == 'POST':
        experiment_id = request.POST.get('experiment_id')
        project = request.POST.get('experiment_project')
        name = request.POST.get('experiment_name')
        objective = request.POST.get('experiment_objective')
        notes = request.POST.get('experiment_notes')

        experiment = Experiment.objects.get(pk=experiment_id)
        experiment.name = name
        experiment.project_id = project
        experiment.objective = objective
        experiment.notes = notes
        experiment.save()

        result = {
            'id': experiment.id,
            'name': experiment.name,
            'project_id': experiment.project_id,
            'project_name': experiment.project.name,
            'objective': experiment.objective,
            'notes': experiment.notes,
            'status': experiment.status,
            'order': experiment.order,
        }
        return HttpResponse(json.dumps(result))


@login_required(login_url='/sign-in/')
def toggle_experiment(request):
    # ajax endpoint for completing an experiment
    if request.method == 'POST':
        experiment_id = request.POST.get('experiment_id')
        action = request.POST.get('action')
        experiment = Experiment.objects.get(pk=experiment_id)
        if action == experiment.status:
            experiment.status = 'O'
        else:
            experiment.status = action
        experiment.save()
        result = {
            'experiment_id': experiment.id,
            'status': experiment.status,
        }
        return HttpResponse(json.dumps(result))


@login_required(login_url='/sign-in/')
def delete_experiment(request):
    # ajax endpoint for deleting an experiment
    if request.method == 'POST':
        experiment_id = request.POST.get('experiment_id')
        experiment = Experiment.objects.get(pk=experiment_id)
        experiment.status = 'D'
        experiment.save()
        result = {
            'experiment_id': experiment.id,
            'status': experiment.status,
        }
        return HttpResponse(json.dumps(result))


@login_required(login_url='/sign-in/')
def update_experiment_order(request):
    # ajax endpoint for updating the sort order of experiments
    if request.method == 'POST':
        experiment_id = request.POST.get('experiment_id')
        new_order = int(request.POST.get('new_order'))
        experiment = Experiment.objects.get(pk=experiment_id)
        list_of_updated_experiments = experiment.update_order(new_order)
        result = [{ 'experiment_id': e.id, 'order': e.order } for e in list_of_updated_experiments]
        return HttpResponse(json.dumps(result))
