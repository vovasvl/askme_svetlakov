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

    avatar = models.ImageField(upload_to="images", default=STATIC_URL + 'img/imgg.jpg', blank=True, null=True)

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
class QuestionLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["profile", "question"]
    def __str__(self):
        return f"Like by {self.profile}"

class AnswerLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Like by {self.profile}"
