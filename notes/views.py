from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import UserForm, NoteForm

from django.utils import timezone

# Create your views here.

def index(request):
    return render(request, 'notes/index.html')

def user_signup(request):
    registred = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            print('valid')
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registred = True
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'notes/signup.html', context={'form':user_form})
    else:
        return render(request, 'notes/signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse('<h1>You need to activate your account. Inform administrator about your problem.</h1>')
        else:
            return render(request, 'notes/signin.html', context={'errors':'Invalid login credentials supplied.'})
    else:
        return render(request, 'notes/signin.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def add_note(request, group_id):
    context = {'group_name': Group.objects.get(id=group_id)}
    if request.method == 'POST':
        form = NoteForm(data=request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.create_date = timezone.now()
            note.group = Group.objects.get_or_create(group_name = form.cleaned_data['group_name'].lower())[0]
            note.save()
            return redirect('index')
        else:
            context['errors'] = form.errors
            return render(request, 'notes/add_note.html', context=context)
    else:
        return render(request, 'notes/add_note.html', context=context)

@login_required
def change_note(request, note_id):
    note = Note.objects.get(id=note_id)
    context = {
        'note': note
    }
    if request.user != note.user:
        return HttpResponse("<h1>You don't have permissions to do that!</h1>")
    else:
        if request.method == 'POST':
            form = NoteForm(data=request.POST)
            if form.is_valid():
                note.text = form.cleaned_data['text']
                note.planned_date = form.cleaned_data['planned_date']
                note.group = Group.objects.get_or_create(group_name = form.cleaned_data['group_name'].lower())[0]
                note.save()
                return redirect('index')
            else:
                context['errors'] = form.errors
                return render(request, 'notes/change_note.html', context=context)
        else:
            return render(request, 'notes/change_note.html', context=context)


@login_required
def delete_note(request):
    if request.method == 'GET':
        note_id = request.GET.get('note_id')
        note = Note.objects.get(id=note_id)
        if request.user != note.user:
            return HttpResponse("<h1>You don't have permissions to do that!</h1>")
        else:
            note.delete()

            notes = request.user.notes.order_by('planned_date')
            context = {}
            context[Group.objects.get(id=1)] = []
            for note in notes:
                if note.group not in context:
                    context[note.group] = [note]
                else:
                    context[note.group].append(note)

            return render(request, 'notes/notes.html', context={'notes':context})
    else:
        return redirect('index')
