from django.core.management.base import BaseCommand, CommandError
from app.models import User, Profile, Tag, Question, Answer, QuestionLike, AnswerLike
from faker import Faker
from random import randint, sample
from django import db

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)
    def handle(self, *args, **options):
        ratio = options['ratio']
        locale_list=['dk_DK', 'el_GR', 'en_AU', 'en_CA', 'en_GB', 'en_IN', 'en_NZ', 'en_US', 'es_ES', 'es_MX', 'et_EE', 'fa_IR', 'fi_FI', 'fr_FR', 'hi_IN', 'hr_HR', 'hu_HU', 'hy_AM', 'it_IT', 'ja_JP', 'ko_KR', 'lt_LT', 'lv_LV', 'ne_NP', 'nl_NL', 'no_NO', 'pl_PL', 'pt_BR', 'pt_PT', 'ro_RO', 'ru_RU', 'sk_SK', 'sl_SI', 'sv_SE', 'tr_TR', 'uk_UA', 'zh_CN', 'zh_TW']
        fake= Faker('en_US')
        fakeMultiLang = Faker(locale_list)


        users=[User(username=fake.unique.name(), password=fake.password(), email=fake.email(), first_name=fake.first_name()) for i in range(ratio)]
        User.objects.bulk_create(users)
        print("user")

        profiles=[Profile(user=users[i]) for i in range(ratio)]
        Profile.objects.bulk_create(profiles)
        print("profile")

        generated_words = set()
        def generate_unique_word():
            k=0
            flag = 0
            while True:
                if k>2000:
                    k=0
                    flag+=1

                if flag==0:
                    word = fakeMultiLang.word()
                elif flag==1:
                    word = fakeMultiLang.job().split('/')[0]
                elif flag==2:
                    word = fakeMultiLang.country()
                else:
                    word = fakeMultiLang.first_name()
                if word not in generated_words:
                    generated_words.add(word)
                    print(len(generated_words)*100/ratio)
                    return word
                k+=1

        tags = [Tag(name=generate_unique_word()) for i in range(ratio)]
        Tag.objects.bulk_create(tags)
        print("tags")

        db.reset_queries()

        questions = [Question(profile=profiles[randint(0,ratio-1)], title=fake.sentence(), text=fake.text(max_nb_chars=150)) for i in range(10*ratio)]
        Question.objects.bulk_create(questions)
        for i in range(10*ratio):
            questions[i].tags.add(*sample(tags,randint(2,5)))
            print(i*10/ratio)
        print("questions")

        db.reset_queries()

        answers = [Answer(profile=profiles[randint(0,ratio-1)], question=questions[randint(0,10*ratio-1)], text=fakeMultiLang.text(max_nb_chars=200), correct=['c','i'][randint(0,1)] ) for i in range(100*ratio)]
        batch_size = 500

        for i in range(0, 100*ratio, batch_size):
            batch = answers[i:i + batch_size]
            Answer.objects.bulk_create(batch)


        print("answers")

        db.reset_queries()

        questionLikes = []
        for i in range(ratio):
            for j in sample(questions, 20):
                questionLikes.append(QuestionLike(profile=profiles[i], question=j))
        QuestionLike.objects.bulk_create(questionLikes)
        print("questionLikes")


        for i in range(ratio):
            answerLikes=[]
            for j in sample(answers,180):
                answerLikes.append(AnswerLike(profile=profiles[i], answer=j))
            AnswerLike.objects.bulk_create(answerLikes)
        print("answerLikes")

