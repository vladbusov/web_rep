from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from blog.models import Question, Answer

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        u = User.objects.get(pk=1)
        q = Question(author=u, text='Как научиться ходить на пары?')
        q.save()
        a = Answer(question_id=1, content='Никто не знает ответа на этот вопрос!', author=u)
        a.save()