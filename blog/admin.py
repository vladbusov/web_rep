from django.contrib import admin
from .models import Question, Tag, Answer, UserProfile, QuestionLike, AnswerLike

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(UserProfile)
admin.site.register(QuestionLike)
admin.site.register(AnswerLike)