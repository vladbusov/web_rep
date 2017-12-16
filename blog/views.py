from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf.urls import url
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponse, Http404, HttpResponseBadRequest,  JsonResponse, HttpResponseRedirect
from .models import Question, Answer, Tag,  QuestionLike, AnswerLike
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core import validators, serializers
from . import urls
from .forms import LoginForm, UserRegistrationForm, AskForm, AnswerForm
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import re

questions_per_page = 3

questions = []
for i in range(1, 30):
    questions.append({
        'title': 'title ' + str(i),
        'id': i,
        'text': 'text' + str(i),
    })

def paginate(request , qs):
    try:
        limit = int(request.GET.get('limit', 4))
    except ValueError:
        limit = 4
    if limit > 100:
        limit = 4
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    paginator.baseurl = '/?page='
    paginator.startnav = page.number - 2
    paginator.endnav = page.number + 2
    return page


def main(request):
    success = request.GET.get('continue')
    page = paginate(request, Question.objects.all())
    user = {}
    if request.user.is_authenticated():
        user['first_name'] = request.user.first_name
        user['last_name'] = request.user.last_name
    return render(request, 'index.html', {'posts': page.object_list ,
                                          'paginator': page.paginator, 'page': page, 'success': success, 'user':user})

def question(request, quest_num = 1):
    scroll = None
    if quest_num == None:
        raise Http404("No questions provided")
    if request.method == "POST":
        text = request.POST.get('text')
        question = Question.objects.get(id=quest_num)
        Answer.objects.create(content=text, question=question, author=request.user)
        scroll = True
    q = Question.objects.get(id=quest_num)
    form = AnswerForm()
    page = paginate(request, q.answers.all())
    user_name = None
    if request.user.is_authenticated():
        user_name = request.user.first_name
    page.paginator.baseurl = '/question/' + str(quest_num) + '/?page='
    if scroll == None:
        return render(request, 'pageOfOneQuestion.html', {'posts': page.object_list ,
                                          'paginator': page.paginator, 'page': page, 'id': quest_num, 'question': q, 'form':form, 'user_name': user_name })
    if scroll == True:
        return render(request, 'pageOfOneQuestion.html', {'posts': page.paginator.page(page.paginator.num_pages).object_list,
                                                          'paginator': page.paginator, 'page': page.paginator.page(page.paginator.num_pages), 'id': quest_num,
                                                          'question': q, 'form': form, 'user_name': user_name})

def hot(request):
    return render(request, 'thistag.html' )

def ask(request):
    return render(request, 'newquestion.html')

def signup(request):
    return render(request, 'registration.html')

def login(request):
    return render(request, 'login.html')

def tag(request, tag):
    return render(request, 'tag.html', {'tag': tag ,})

def settings(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            login_user = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password")
            password2 = request.POST.get("password2")
            if password1 != password2:
                return JsonResponse({'status': 'error',
                                     'message': 'Отсутсвует обязательный параметр',
                                     'fields': ['password', 'password2']})
            request.user.username = login_user
            request.user.set_password(password1)
            request.user.email = email
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            user = auth.authenticate(username=login_user, password=password1)
            if user is not None:
                auth.login(request, user)
            return HttpResponseRedirect('/?continue=saveset')
        form = UserRegistrationForm()
        return render(request, 'settings.html', {'form':form})
    return HttpResponseRedirect('/?continue=notlogin')

def questions_hot(request):
    page = paginate(request, Question.objects.hot())
    page.paginator.baseurl = "questions_hot/?page="
    return render(request, "questions_hot.html", {'posts': page.object_list ,
                                          'paginator': page.paginator, 'page': page,})

def questions_new(request):
    page = paginate(request, Question.objects.new())
    page.paginator.baseurl = "questions_new/?page="
    return render(request, "questions_new.html", {'posts': page.object_list ,
                                          'paginator': page.paginator, 'page': page,})

def questions_tag(request, tag):
    if tag == None:
        raise Http404("No tag provided")

    page = paginate(request, Question.objects.by_tag(tag))
    if page.end_index() == 0:
        raise Http404("No tag provided")

    page.paginator.baseurl = '/tag/' + tag + '/?page='
    return render(request, "questions_tag.html", {'posts': page.object_list ,
                                          'paginator': page.paginator, 'page': page, 'tag': tag})


def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect('/?continue=logout')

def make_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/?continue=relog')
    if request.method == "POST":
        login = request.POST.get('login')
        password = request.POST.get('password')
        user = auth.authenticate(username=login, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/?continue=login')
        return HttpResponseRedirect('/login/?error=login')
    else:
        error = request.GET.get('error')
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error })

def registration(request):
    error_fields = []
    if request.user.is_authenticated():
        return HttpResponseRedirect('/?continue=relog')
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        login_user = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")

        if not first_name or len(first_name) == 0:
            error_fields.append("first_name")
        if not last_name or len(last_name) == 0:
            error_fields.append("last_name")
        if not login_user or len(login_user) == 0:
            error_fields.append("username")
        if not email or len(email) == 0:
            error_fields.append("email")
        if not password1 or len(password1) == 0:
            error_fields.append("password")
        if not password2 or len(password2) == 0:
            error_fields.append("password2")

        if password1 != password2:
            error_fields.append("Пароли не совпадают")

        if len(error_fields) > 0:
            form = UserRegistrationForm()
            return render(request, 'registration.html', {'form': form, 'errors': error_fields})

        try:
            validators.validate_email(email)
        except ValidationError:
            error_fields.append("Неверный формат почты")

        if not re.compile("^([A-Za-z0-9]+)+$").match(login_user):
            error_fields.append("Неверный формат логина")
        try:
            user = User.objects.create_user(username=login_user,
                                       email=email,
                                       password=password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            error_fields.append("Нарушена уникальность вводимых данных")
        except:
            error_fields.append("Неизвестная ошибка сервера")
        if user is not None:
            return HttpResponseRedirect('/?continue=reg')
        else:
            error_fields.append("Неизвестная ошибка")
    form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form, 'errors': error_fields})

def ask_quest(request):
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error',
                             'message': 'Ошибка доступа'})
    if request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("text")
        tags = request.POST.get("tags")

        qst = Question.objects.create(title=title,
                                          text=text,
                                          author=request.user)
        tags = tags.split(",")
        for tag in tags:
            tag = (str(tag)).replace(' ', '')
            Tag.objects.add_qst(tag, qst)
        qst.save()
        return HttpResponseRedirect('/?page=1000000000')

    form = AskForm()
    return render(request, 'newquestion.html', {'form':form, })


@csrf_exempt
def app_like(request):
    is_questions = request.POST.get("question", True)
    id = request.POST.get("id", None)
    is_like = request.POST.get("is_like", True)
    rating = 0
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'error',
                             'message': 'Эта операция доступна только авторизованным пользователям'})
    if not id:
        return JsonResponse({'status': 'error',
                             'message': 'Отсутсвует id'})

    questions = None
    if is_questions:
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return JsonResponse({'status': 'error',
                                 'message': 'Такого вопроса не существует'})
        like, created = QuestionLike.objects.get_or_create(question=question, by_user=request.user)
        rating = len(QuestionLike.objects.filter(question=question))
        question.rating_num = rating
        question.save()
    else:
        try:
            answer = Answer.objects.get(id=id)
        except Question.DoesNotExist:
            return JsonResponse({'status': 'error',
                                 'message': 'Такого ответа не существует'})
        like, created = AnswerLike.objects.get_or_create(answer=answer, by_user=request.user)
        rating = AnswerLike.objects.filter(answer=answer)
        answer.rating_num = rating
        answer.save()
    like.is_like = is_like
    like.save()
    return JsonResponse({'status': 'ok',
                         'answer': {
                             'rating': rating
                         }})
