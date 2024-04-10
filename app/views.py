from django.core.paginator import Paginator
from django.shortcuts import render
from math import ceil

from app.models import Question, Tag, Answer
# Create your views here.

def pagination(objects_list, request,per_page=5):
    page_num = request.GET.get('page', 1)
    try:
        if (int(page_num)<1 or int(page_num) > ceil(len(objects_list) / per_page)):
            page_num=1

    except ValueError:
        page_num=1
    paginator = Paginator(objects_list, per_page)
    page_obj = paginator.page(page_num)
    return page_obj

def index(request):

    questions=pagination(Question.objects.order_by_created_at(), request)

    return render(request, "index.html", {"questions": questions})

def hot(request):

    questions=pagination(Question.objects.order_by_score(), request)

    return render(request, "hot_questions.html", {"questions": questions})

def question(request, question_id):

    try:
        question = Question.objects.get_question(question_id)
    except Question.DoesNotExist:
        return raiseError(request, text="(wrong question, buddy)")
    answers = Answer.objects.get_by_question(question)


    return render(request, "question_detail.html", {"question": question, "answers": answers})

def ask(request):
    return render(request, "ask.html")
def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")
def settings(request):
    return render(request, "settings.html")
def tag(request, tag_name):
    try:
        tag = Tag.objects.get_tag(tag_name)
    except Tag.DoesNotExist:
        return raiseError(request, text="(wrong tag, buddy)")

    questions = pagination(Question.objects.filter_by_tag(tag), request)

    return render(request, "tag.html", {"tag_name": tag_name, "questions": questions})

def raiseError(request, code=404, title="Page not found", text=""):
    return render(request, "error.html", {"code": code, "title": title, "text": f'hello there, you seem lost '+text})