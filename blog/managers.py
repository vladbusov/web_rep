from django.db import models
from django.template.loaders import cached
from django.core.cache import caches, cache

class QuestionManager(models.Manager):
    def hot(self):
        return self.order_by('-rating_num')

    def new(self):
        return self.order_by('-added_on')

    def by_tag(self, tag):
        return self.filter(tags__name__iexact=tag).order_by('-added_on')


class QuestionVoteManager(models.Manager):
    def by_question(self, question_id):
        return self.filter(question__id=question_id)

    def update_rating(self, question_id):
        rating = 0
        votes = self.filter(question__id=question_id).all()
        for vote in votes:
            if vote.is_like:
                rating += 1
            else:
                rating -= 1
        self.Question.rating_num = rating
        self.Question.save()

    def add_vote(self, question, vote):
        new_vote = self.Vote.create(question=question)
        new_vote.is_like = vote
        new_vote
        question.objects.update_rating()

class UserManager(models.Manager):
    def get_user(self, login):
        try:
            return self.get(login=login)
        except self.DoesNotExist:
            return None

class TagManager(models.Manager):
    def add_qst(self, tag_str, question):
        tag, created = self.get_or_create(name=tag_str)
        question.tags.add(tag)
        return tag

    def by_tag(self, tag_str):
        return self.filter(title=tag_str).first().questions.all()

    def popular(self):
        return cache.get('test')
