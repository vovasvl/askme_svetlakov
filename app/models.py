import json

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

from askme_svetlakov.settings import STATIC_URL


class TagManager(models.Manager):
    def get_tag(self, tag_name):
        return self.get(name=tag_name)
    #!def order_by_questions_count(self, n=5):
    #!!!    return sorted(self.get_queryset(), key=lambda x: Question.objects.get_by_tag(x).count(), reverse=True)
class Tag(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TagManager()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to="images", default="/static/img/default.jpg", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_username()

class QuestionManager(models.Manager):
    def get_question(self, question_id):
        return self.get(id=question_id)
    def order_by_created_at(self):
        return self.get_queryset().order_by('-created_at')
    def order_by_score(self):
        return self.get_queryset().annotate(score_count=Count('questionlike')).order_by('-score_count')
        #return sorted(self.get_queryset(), key=lambda x: x.get_score(), reverse=True)
    def filter_by_tag(self, tag):
        return self.filter(tags=tag)
class Question(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags_to_questions')

    title = models.CharField(max_length=255)
    text = models.TextField(max_length=255)

    objects = QuestionManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_score(self):
        return QuestionLike.objects.filter(question=self).count()
    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()
    def __str__(self):
        return self.title

class AnswerManager(models.Manager):
    def get_by_question(self, question):
        return self.filter(question=question).order_by('created_at')

    def correct_async(self, request, answer_id):
        body = json.loads(request.body)
        answer = Answer.objects.filter(id=answer_id).get()
        correct = answer.correct

        if correct == "c":
            answer.correct = "i"
        else:
            answer.correct = "c"
        answer.save()

        body['correct'] = answer.correct
        return body
class Answer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    CORRECT="c"
    INCORRECT="i"
    CORRECT_CHOICES = {("c", "Correct"), ("i", "Incorrect")}
    text = models.TextField(max_length=255)
    correct = models.CharField(choices=CORRECT_CHOICES, max_length=1, default=INCORRECT)

    objects = AnswerManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_score(self):
        return AnswerLike.objects.filter(answer=self).count()

    def __str__(self):
        return f"Answer by {self.profile}"

class QuestionManager(models.Manager):
    def like_async(self, request, question_id):
        body = json.loads(request.body)
        question = Question.objects.filter(id=question_id).get()
        profile = Profile.objects.filter(user=request.user).get()
        try:
            question_like, question_like_created = QuestionLike.objects.get_or_create(question=question, profile=profile)
        except QuestionLike.MultipleObjectsReturned:
            question_like = QuestionLike.objects.filter(question=question, profile=profile).first()
            question_like_created = 0

        if not question_like_created:
            question_like.delete()

        body['likes_count'] = QuestionLike.objects.filter(question=question).count()
        question.likes = QuestionLike.objects.filter(question=question).count()
        question.save()
        return body
class QuestionLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)

    objects = QuestionManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["profile", "question"]
    def __str__(self):
        return f"Like by {self.profile}"


class AnswerLikeManager(models.Manager):
    def like_async(self, request, answer_id):
        body = json.loads(request.body)
        answer = Answer.objects.filter(id=answer_id).get()
        profile = Profile.objects.filter(user=request.user).get()
        answer_like, answer_like_created = AnswerLike.objects.get_or_create(answer=answer, profile=profile)

        if not answer_like_created:
            answer_like.delete()

        body['likes_count'] = AnswerLike.objects.filter(answer=answer).count()
        answer.likes = AnswerLike.objects.filter(answer=answer).count()
        answer.save()
        return body

class AnswerLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

    objects = AnswerLikeManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Like by {self.profile}"
