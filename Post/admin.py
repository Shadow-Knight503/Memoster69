from django.contrib import admin
from .models import Meme, Comment, Vote, DayDecor, Ring, Msg, Cmnt_Vote

# Register your models here.
admin.site.register(Meme)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(DayDecor)
admin.site.register(Ring)
admin.site.register(Msg)
admin.site.register(Cmnt_Vote)
