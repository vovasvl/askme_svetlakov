from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from math import ceil
# Create your views here.

QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"There is question number {i}"
    } for i in range(200)
]
ANSWERS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"There is question number {i}"
    } for i in range(200)
]

TAGS={"tagtag": {"id": 1, "questions": QUESTIONS[10:100]}, "lol": {"id": 2, "questions": QUESTIONS[100:195]}}

def pagination(objects_list, request,per_page=5):
    page_num = request.GET.get('page', 1)
    try:
        if (int(page_num)<1 or int(page_num) > ceil(len(objects_list) / per_page)):
            raise Http404("That page contains no results (Wrong numbers, my man...)")
    except ValueError:
        raise Http404("That page contains no results (try typing integer page number, maybe)")
    paginator = Paginator(objects_list, per_page)
    page_obj = paginator.page(page_num)
    return page_obj

def index(request):

    questions=pagination(QUESTIONS,request)
    return render(request, "index.html", {"questions": questions})

def hot(request):

    questions=pagination(QUESTIONS[::-1],request)

    return render(request, "hot_questions.html", {"questions": questions})

def question(request, question_id):

    question = QUESTIONS[question_id]
    answers=pagination(ANSWERS,request)

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
    item = TAGS.get(tag_name)
    if(item==None):
        raise Http404('hello there, you seem lost')

    questions = pagination(TAGS.get(tag_name).get('questions'),request)
    return render(request, "tag.html", {"tag_name": tag_name, "questions": questions})
