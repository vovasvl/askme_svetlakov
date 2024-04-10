from django.core.management.base import BaseCommand, CommandError
from app.models import Question, Profile

class Command(BaseCommand):
    #help = 'The Zen of Python'

    def handle(self, *args, **options):
        profile = Profile.objects.first()
        questions = [Question(profile = profile, title=f'Вопрос {i}', text=f'Текст вопроса {i}') for i in range(50)]

        Question.objects.bulk_create(questions)

        print(profile)
