from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Profile, Question, Tag, Answer


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15,required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


    def clean_username(self):
        username = self.cleaned_data['username']
        username.strip()
        username.lower()
        if(len(username)<6):
            self.add_error('username', "Логин должен быть не меньше 6 сиволов")
        return username
    def clean(self):
        super().clean()
        return self.cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(label="Login", max_length=15, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Username",max_length=30, required=True)

    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    avatar = forms.ImageField(allow_empty_file=True, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        username.strip()
        username.lower()
        if(len(username)<6):
            self.add_error('username', "Логин должен быть не меньше 6 сиволов")
        if(User.objects.filter(username=username).exists()):
            self.add_error('username', "Пользователь с таким логином уже существует")
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        if(User.objects.filter(email=email).exists()):
            self.add_error('email', "Пользователь с такой почтой уже существует")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.data['confirm_password']

        if(len(password)<8):
            self.add_error('password', "Пароль должен быть не меньше 8 сиволов")
        if(password != confirm_password):
            self.add_error('confirm_password', "Пароли не совпадают")
        return password
    def clean(self):
        super().clean()
        return self.cleaned_data

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'], email=self.cleaned_data['email'], first_name=self.cleaned_data['first_name'])

        # profile = Profile(user=user,avatar=self.cleaned_data['avatar'])
        profile = Profile(user=user)
        if self.cleaned_data['avatar']:
            setattr(profile, 'avatar', self.cleaned_data['avatar'])
        profile.save()

        return user

class SettingsForm(forms.ModelForm):
    username = forms.CharField(label="Login", max_length=15, required=True)
    email = forms.EmailField()
    first_name = forms.CharField(label="Username", max_length=30, required=True)
    avatar = forms.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = User
        fields = ('username','first_name', 'email')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists() and self.initial.get('username')!=username:
            self.add_error('username', 'Пользователь с таким логином уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() and self.initial.get('email')!=email:
            self.add_error('email', 'Пользователь с такой почтой уже существует')
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        profile = Profile.objects.filter(user=self.instance).get()

        if avatar:
            profile.avatar = avatar
            profile.save()
        return avatar

    def clean(self):
        super().clean()
        return self.cleaned_data


class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    text = forms.CharField(widget=forms.Textarea ,max_length=300, required=True)
    tags = forms.CharField(required=False)

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        for tag in tags.split():
            if any(c in "!@#$%^&*()-+?_=,<>/" for c in tag):
                self.add_error('tags', 'В тегах запрещено использовать специальные символы')
                break
        return tags
    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')

    def save(self, profile):
        question = Question.objects.create(profile=profile,title=self.cleaned_data['title'],text=self.cleaned_data['text'])
        tags = self.cleaned_data['tags'].split()
        tagsModel = []
        for tag in tags:
            if Tag.objects.filter(name=tag).exists():
                tagsModel.append(Tag.objects.filter(name=tag).get())
            else:
                newTag = Tag.objects.create(name=tag)
                tagsModel.append(newTag)
        question.tags.set(tagsModel)
        question.save()
        return question

class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"style": "height: 200px; resize: none;"}),max_length=300, required=True)

    class Meta:
        model = Answer
        fields = ('text',)

    def save(self, question, profile):
        answer = Answer.objects.create(question=question, text=self.cleaned_data['text'], profile=profile)
        answer.save()
        return answer