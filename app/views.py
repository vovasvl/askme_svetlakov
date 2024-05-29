from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from math import ceil

from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from app.forms import LoginForm, RegisterForm, SettingsForm, QuestionForm, AnswerForm
from app.models import Question, Tag, Answer, Profile, AnswerLike, QuestionLike

PAGANATION_PER_PAGE = 5
# Create your views here.

def pagination(objects_list, request,per_page=PAGANATION_PER_PAGE):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page_obj = paginator.page(page_num)
    except EmptyPage:
        page_obj = paginator.page(1)


    return page_obj

def index(request):
    if request.user.is_authenticated:
        avatar = Profile.objects.filter(user=request.user).get().avatar
        print(avatar.url)
    else:
        avatar = None
    questions=pagination(Question.objects.order_by_created_at(), request)

    return render(request, "index.html", {"questions": questions, "avatar": avatar})

def hot(request):

    questions=pagination(Question.objects.order_by_score(), request)
    return render(request, "hot_questions.html", {"questions": questions})

def question(request, question_id):
    try:
        question = Question.objects.get_question(question_id)
    except Question.DoesNotExist:
        raise Http404("(wrong question, buddy)")

    answers = pagination(Answer.objects.get_by_question(question), request)

    if request.user.is_authenticated:
        avatar = Profile.objects.filter(user=request.user).get().avatar
    else:
        avatar = None

    if request.method == "GET":
        answerForm = AnswerForm()
    if request.method == "POST":
        answerForm = AnswerForm(data=request.POST)
        if answerForm.is_valid():
            answer = answerForm.save(question, Profile.objects.filter(user=request.user).get())
            answer.save()
            ind = list(Answer.objects.get_by_question(question)).index(answer)
            return redirect('{}?{}'.format(reverse('question', kwargs={'question_id': answer.question.id}),'page=' + str(ind // PAGANATION_PER_PAGE + 1)))
    return render(request, "question_detail.html",
                  {"question": question, "answers": answers, "form": answerForm, "avatar": avatar})
@csrf_protect
@login_required(login_url="login")
def ask(request):
    avatar = Profile.objects.filter(user=request.user).get().avatar

    if request.method == "GET":
        questionForm = QuestionForm()
    if request.method == "POST":
        questionForm = QuestionForm(data=request.POST)
        if questionForm.is_valid():
            question = questionForm.save(Profile.objects.filter(user=request.user).get())
            question.save()
            return redirect(reverse('question', kwargs={'question_id': question.id}))
    return render(request, "ask.html", {"form": questionForm, "avatar": avatar})
@csrf_protect
def Login(request):
    if request.method == 'GET':
        loginForm = LoginForm()
    if request.method == 'POST':
        loginForm = LoginForm(data=request.POST)
        if loginForm.is_valid():
            user = authenticate(request, **loginForm.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                loginForm.add_error(None, "Пользователя с такими данными не существует")
    return render(request, "login.html", context={"form": loginForm})

@csrf_protect
def signup(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        registerForm = RegisterForm()
    if request.method == 'POST':
        print(request.POST)
        registerForm = RegisterForm(data=request.POST, files=request.FILES)
        print("registerForm",registerForm.data)
        if registerForm.is_valid():
            user = registerForm.save()
            if user:
                login(request,user)
                return redirect(reverse('index'))
            else:
                registerForm.add_error(field=None, error="User saving error!")
    return render(request, "signup.html", context={"form": registerForm})

@csrf_protect
@login_required(login_url="login")
def Logout(request):
    logout(request)
    return redirect(reverse('login'))
@csrf_protect
@login_required(login_url="login")
def settings(request):
    avatar = Profile.objects.filter(user=request.user).get().avatar
    if request.method == 'GET':
        settingsForm = SettingsForm(data={"first_name": request.user.first_name, "email": request.user.email, "username": request.user.username}, instance=request.user)
    if request.method == 'POST':
        settingsForm = SettingsForm(data=request.POST, instance=request.user,files=request.FILES)
        if settingsForm.is_valid():
            settingsForm.save()
            return redirect(reverse('settings'))

    return render(request, "settings.html", context={"form": settingsForm, "avatar": avatar})
    #return render(request, "settings.html")
def tag(request, tag_name):
    try:
        tag = Tag.objects.get_tag(tag_name)
    except Tag.DoesNotExist:
        raise Http404("(wrong tag, buddy)")

    questions = pagination(Question.objects.filter_by_tag(tag), request)

    return render(request, "tag.html", {"tag_name": tag_name, "questions": questions})

@require_http_methods(["POST"])
@login_required(login_url="login")
@csrf_protect
def like_async(request, question_id):
    body = QuestionLike.objects.like_async(request, question_id)

    return JsonResponse(body)


@require_http_methods(["POST"])
@login_required(login_url="login")
@csrf_protect
def like_async_answer(request, answer_id):
    body = AnswerLike.objects.like_async(request, answer_id)

    return JsonResponse(body)

@require_http_methods(["POST"])
@login_required(login_url="login")
@csrf_protect
def correct_async(request, answer_id):
    body = Answer.objects.correct_async(request, answer_id)

    return JsonResponse(body)