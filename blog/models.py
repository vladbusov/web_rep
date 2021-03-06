from django.db import models
from django.contrib.auth.models import User
from blog.managers import QuestionManager, UserManager, TagManager


class UserProfile(models.Model):
    avatar = models.ImageField(null=True, blank=True, verbose_name=u"аватар", upload_to='static/images/')
    register_date = models.DateField(null=False, blank=True, auto_now_add=True, verbose_name=u"дата регистрации")
    rating = models.IntegerField(blank=True, default=0, verbose_name=u"рейтинг")
    user = models.OneToOneField(User, related_name='userprofile', null=False, verbose_name="user",
                                on_delete=models.DO_NOTHING)
    objects = UserManager()

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = u'пользователь'
        verbose_name_plural = u'пользователи'


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name="заголовок")
    text = models.TextField(verbose_name="текст")
    author = models.ForeignKey(User, verbose_name="автор", on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField("Tag")
    rating_num = models.IntegerField(verbose_name='рейтинг', default=0)
    added_on = models.DateTimeField(verbose_name='дата и время добавления', auto_now_add=True)
    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'


class Answer(models.Model):
    content = models.TextField(verbose_name='текст ответа')
    author = models.ForeignKey(User, verbose_name='автор', on_delete=models.CASCADE)
    is_correct = models.BooleanField(verbose_name='верный?', default=False)
    rating_num = models.IntegerField(verbose_name='рейтинг', default=0)
    added_on = models.DateTimeField(blank=True, auto_now_add=True, verbose_name='дата и время добавления')
    question = models.ForeignKey(Question, related_name='answers', null=False, verbose_name="вопрос",
                                 on_delete=models.DO_NOTHING)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.answer_text = None

    def __str__(self):
        return 'Comment №{number} by {user}'.format(number=self.pk, user='Username')

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name="имя")
    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Like(models.Model):
    by_user = models.ForeignKey(User, null=False, verbose_name=u"пользователь", on_delete=models.DO_NOTHING)
    is_like = models.BooleanField(blank=True, default=True, verbose_name=u"лайк")

    def __unicode__(self):
        return "Лайк пользователя " + self.by_user.username

    class Meta:
        abstract = True
        verbose_name = u'лайк'
        verbose_name_plural = u'лайки'


class QuestionLike(Like):
    question = models.ForeignKey(Question, null=False, verbose_name="вопрос", on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return "Лайк пользователя " + self.by_user.username + " на вопрос " + self.question.title

    class Meta:
        unique_together = ("question", "by_user")


class AnswerLike(Like):
    answer = models.ForeignKey(Answer, null=False, verbose_name="ответ", on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return "Лайк пользователя " + self.by_user.username + " на ответ " + self.answer.answer_text

    class Meta:
        unique_together = ("answer", "by_user")
