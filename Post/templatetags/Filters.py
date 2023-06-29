from django import template
from Post.models import Msg

register = template.Library()


@register.filter
def get_index(value, arg):
    return value[int(arg)]


@register.filter
def attach(value):
    val = value.split('/')
    val[6] = str('fl_attachment')
    return '/'.join(val)


@register.filter
def get_cnt(value):
    if int(value) == 69420:
        return 'Nice'
    else:
        msg = Msg.objects.get(id=int(value))
        if msg.Edited == '0':
            return msg.cnt
        elif msg.Edited == '1':
            return msg.Edit_1
        elif msg.Edited == '2':
            return msg.Edit_2
        else:
            return 'Frick You'


@register.filter
def get_clr(value):
    if int(value) == 69420:
        return 'Nice'
    else:
        if Msg.objects.get(id=int(value)).side == '0':
            return 'red'
        elif Msg.objects.get(id=int(value)).side == '1':
            return 'blue'
        else:
            return 'grey'
