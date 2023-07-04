from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Meme, Comment, Vote, DayDecor, Ring, Msg, Cmnt_Vote
from .forms import PostMemes, CommentSection, MsgBuild
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from Register_Page.models import UserProfile, Theme
from Register_Page.decorators import unauthenticated_user
import json
import urllib.parse
from datetime import datetime


# Create your views here.
def data(request):
    username = request.user.id
    users = UserProfile.objects.get(user_id=username)
    theme = Theme.objects.get(user_id=users.id)
    url = users.Profile_pic.url
    name = users.Nick_Name
    date = users.date_created
    return url, name, date, theme


def home(request):
    imgs = Meme.objects.all()
    ctx = {'imgs': imgs}
    return render(request, 'Home.html', ctx)


#@login_required(login_url='/home')
def user_home(request):
    print("Initiating...")
    if not request.user.is_authenticated:
        user = authenticate(request, username="Shadow", password="zxc123asd")
        login(request, user)
    user = request.user
    func = data(request)
    url = func[0]
    name = func[1]
    posts = {}
    comment = CommentSection()
    date = datetime.today().date()
    day = datetime.today().strftime('%A')
    if DayDecor.objects.filter(Day=day):
        day_decor = DayDecor.objects.get(Day=day)
    else:
        day_decor = "None"
    daily_memes = Meme.objects.filter(Daily=1, Day=day)
    date_memes = Meme.objects.filter(Daily=1, Date=date)
    pin_memes = Meme.objects.filter(Pinned=1)
    admin_memes = [daily_memes, date_memes, pin_memes]
    for memes in admin_memes:
        for meme in memes:
            posts[meme] = "None"
    memes = Meme.objects.filter(Pinned=0, Daily=0)
    for meme in memes.order_by('-Points'):
        prpty = []
        if Vote.objects.filter(op=user, meme=meme).exists():
            vote = Vote.objects.get(op=user, meme=meme)
            if vote.voted == '1':
                prpty.append(1)
            elif vote.voted == '2':
                prpty.append(2)
            else:
                prpty.append(3)
        else:
            prpty.append(0)
        posts[meme] = prpty
    if request.POST.get("Act") == "Upvote" and request.is_ajax():
        meme_id = request.POST.get("Id")
        meme = Meme.objects.get(id=meme_id)
        values = posts.get(meme)
        if not values[0] == 0:
            vote = Vote.objects.get(meme_id=meme_id, op_id=user.id)
            if values[0] == 3:
                vote.voted = '1'
                meme.Points += 1
            elif values[0] == 2:
                vote.voted = '1'
                meme.Points += 2
            elif values[0] == 1:
                vote.voted = '3'
                meme.Points -= 1
            meme.save()
            vote.save()
        else:
            Vote.objects.create(meme=meme, op=request.user, voted='1')
            meme.Points += 1
            meme.save()
    elif request.POST.get("Act") == "Downvote" and request.is_ajax():
        meme_id = request.POST.get("Id")
        meme = Meme.objects.get(id=meme_id)
        values = posts.get(meme)
        if not values[0] == 0:
            vote = Vote.objects.get(meme_id=meme_id, op_id=user.id)
            if values[0] == 3:
                vote.voted = '2'
                meme.Points -= 1
            elif values[0] == 2:
                vote.voted = '3'
                meme.Points += 1
            elif values[0] == 1:
                vote.voted = '2'
                meme.Points -= 2
            meme.save()
            vote.save()
        else:
            Vote.objects.create(meme=meme, op=user, voted='2')
            meme.Points -= 1
            meme.save()
    elif request.POST.get("Act") == "Reply":
        meme_id = request.POST.get("the_effing_id")
        chn = str(request.POST.get("Cmnt_Chn"))
        cmnt = request.POST.get("comment")
        reply = Comment.objects.create(op=user, reply='1', not_post_method_ok_id=meme_id, comment=cmnt, cmnt_chn=chn)
        reply.save()
        return HttpResponse(reply.id)
    elif request.POST.get("Act") == "Ring_Send":
        msg = Msg()
        msg.op = request.user
        msg.ring.id = request.POST.get("Id")
        msg.side = request.POST.get("Color")
        msg.cnt = request.POST.get("Cnt")
        msg.save()
    elif request.POST.get("Act") == "Msg_Edit":
        msg_id = request.POST.get("Id")
        msg = Msg.objects.get(id=msg_id)
        if msg.Edited == "0":
            msg.Edit_1 = request.POST.get("Cnt")
            msg.Edited = '1'
            msg.Edit_Time = datetime.utcnow()
        elif msg.Edited == "1":
            msg.Edit_2 = request.POST.get("Cnt")
            msg.Edited = '2'
            msg.Edit_Time = datetime.utcnow()
        msg.save()
    elif request.POST.get("Act") == "Ring_Reply":
        msg = Msg()
        msg.op = request.user
        msg.ring.id = request.POST.get("Id")
        msg.side = request.POST.get("Color")
        msg.cnt = request.POST.get("Cnt")
        msg.Reply = request.POST.get("Reply_ID")
        msg.save()
    elif request.POST.get("Act") == "Cmnt_Upvote":
        vote_val = request.POST.get("Prpty")
        cmnt = Comment.objects.get(id=request.POST.get("Id"))
        if not vote_val == '0':
            vote = Cmnt_Vote.objects.get(Cmnt=cmnt, op=user)
            if vote_val == '3':
                vote.voted = '1'
                cmnt.Points += 1
            elif vote_val == '2':
                vote.voted = '1'
                cmnt.Points += 2
            elif vote_val == '1':
                vote.voted = '3'
                cmnt.Points -= 1
            cmnt.save()
            vote.save()
        else:
            Cmnt_Vote.objects.create(Cmnt=cmnt, op=user, voted='1')
            cmnt.Points += 1
            cmnt.save()
    elif request.POST.get("Act") == "Cmnt_Downvote":
        vote_val = request.POST.get("Prpty")
        cmnt = Comment.objects.get(id=request.POST.get("Id"))
        if not vote_val == '0':
            vote = Cmnt_Vote.objects.get(Cmnt=cmnt, op=user)
            if vote_val == '3':
                vote.voted = '2'
                cmnt.Points -= 1
            elif vote_val == '2':
                vote.voted = '3'
                cmnt.Points += 1
            elif vote_val == '1':
                vote.voted = '2'
                cmnt.Points -= 2
            cmnt.save()
            vote.save()
        else:
            Cmnt_Vote.objects.create(Cmnt=cmnt, op=user, voted='2')
            cmnt.Points -= 1
            cmnt.save()
    elif request.method == 'POST' and request.is_ajax:
        print("Comment Command being used")
        comment = CommentSection(request.POST, initial={'comment': None})
        body = json.loads(request.body.decode('UTF-8'))
        text = body['comment'][93:].replace("+", " ")
        better_txt = urllib.parse.unquote(text)
        the_effing_id = int(body['the_effing_id'])
        if comment.is_valid():
            instance = comment.save(commit=False)
            the_right_meme = Meme.objects.get(id=the_effing_id)
            instance.not_post_method_ok = the_right_meme
            instance.op = request.user
            instance.comment = str(better_txt)
            instance.save()
            instance.cmnt_chn = f'{instance.id}+1'
            instance.save()
    comments = Comment.objects.all()
    ctx = {
        'user': user,
        'posts': posts,
        'url': url,
        'name': name,
        'theme': func[3],
        'comment': comment,
        'comments': comments,
        'day': day,
        'Decor': day_decor,
        'Static_Gif': 'https://res.cloudinary.com/meme-topia/image/upload/v1647493481/image_2022-03-17_103302_saszcw.png',
    }
    return render(request, 'User_Home.html', ctx)


def get_cmnt_replies(cmnt_id, num, op):
    replies = {}
    for reply in Comment.objects.filter(cmnt_chn=f"{cmnt_id}+{num}").order_by('-Points'):
        replies[reply] = cmnt_vote_getter(reply, op)
        if Comment.objects.filter(cmnt_chn=f"{cmnt_id}-{reply.id}+{int(num) + 1}").exists():
            replies.update(get_cmnt_replies(f'{cmnt_id}-{reply.id}', f'{int(num) + 1}', op))
    return replies


def cmnt_vote_getter(comment, op):
    prpty = []
    if Cmnt_Vote.objects.filter(op=op, Cmnt=comment).exists():
        cmnt = Cmnt_Vote.objects.get(op=op, Cmnt=comment)
        if cmnt.voted == '1':
            prpty.append(1)
        elif cmnt.voted == '2':
            prpty.append(2)
        else:
            prpty.append(3)
    else:
        prpty.append(0)
    return prpty


def comment_update(request, identity):
    func = data(request)
    com_sec = {}
    replies = {}
    meme = Meme.objects.get(id=identity)
    for ringed in Ring.objects.filter(Post_id=identity):
        com_sec[ringed] = "None"
    for comment in Comment.objects.filter(not_post_method_ok_id=identity, reply='0')[:15]:
        prpty = cmnt_vote_getter(comment, request.user)
        com_sec[comment] = prpty
        replies.update(get_cmnt_replies(f'{comment.id}', '1', request.user))
    count = len(com_sec) + len(replies)
    ctx = {
        'meme': meme,
        'com_sec': com_sec,
        'replies': replies,
        'theme': func[3],
        'count': count,
    }
    return render(request, 'Comment_Section.html', ctx)


@login_required(login_url='/login')
def post(request):
    func = data(request)
    posts = PostMemes()
    if request.method == 'POST':
        posts = PostMemes(request.POST, request.FILES)
        if posts.is_valid():
            posts.op = request.user
            posts.save()
        else:
            print(posts.errors)
        return HttpResponseRedirect('https://youtu.be/dQw4w9WgXcQ')
    ctx = {
        'user': request.user,
        'posts': posts,
        'url': func[0],
        'name': func[1],
        'date': func[2],
    }
    return render(request, 'Post.html', ctx)


def ring(request, reload, len_msgs, edit_msgs, ring_id):
    all_msgs = Msg.objects.filter(ring_id=ring_id).count()
    edit1_len = Msg.objects.filter(Edited='1', ring_id=ring_id).count()
    edit2_len = Msg.objects.filter(Edited='2', ring_id=ring_id).count()
    if reload == '1':
        new_msgs = []
        edit_list = []
        edited = 0
        new = 0
        if int(len_msgs) < all_msgs:
            new = 1
            new_msg = Msg.objects.filter(ring_id=ring_id).order_by('-time_stamp')[:(all_msgs - int(len_msgs))]
            for msg in new_msg:
                if msg.Reply == '0':
                    new_msgs.append([msg.id, msg.op.userprofile.Nick_Name, msg.op.userprofile.Profile_pic.url, msg.cnt,
                                     msg.side, '0', '0', msg.op.userprofile.id, msg.Reply])
                else:
                    reply_msg = Msg.objects.get(id=msg.Reply)
                    if msg.Edited == '0':
                        cnt = reply_msg.cnt
                    elif msg.Edited == '1':
                        cnt = reply_msg.Edit_1
                    else:
                        cnt = reply_msg.Edit_2
                    if reply_msg.side == '0':
                        clr = 'Red'
                    else:
                        clr = 'Blue'
                    new_msgs.append([msg.id, msg.op.userprofile.Nick_Name, msg.op.userprofile.Profile_pic.url, msg.cnt,
                                     msg.side, '0', '0', msg.op.userprofile.id, msg.Reply, cnt, clr])
        elif int(edit_msgs.split(',')[0]) < edit1_len:
            edited = 1
            edit_msg = Msg.objects.filter(Edited='1', ring_id=ring_id).order_by('-Edit_Time')[
                       :(edit1_len - int(edit_msgs.split(',')[0]))]
            for edit in edit_msg:
                edit_list.append([edit.id, edit.op.userprofile.Nick_Name, edit.op.userprofile.Profile_pic.url,
                                  edit.cnt, edit.side, edit.Edited, edit.Edit_1])
        elif int(edit_msgs.split(',')[1]) < edit2_len:
            edited = 1
            edit_msg = Msg.objects.filter(Edited='2', ring_id=ring_id).order_by('-Edit_Time')[
                       :(edit2_len - int(edit_msgs.split(',')[1]))]
            for edit in edit_msg:
                edit_list.append([edit.id, edit.op.userprofile.Nick_Name, edit.op.userprofile.Profile_pic.url,
                                  edit.cnt, edit.side, edit.Edited, edit.Edit_1, edit.Edit_2])
        else:
            return HttpResponse(json.dumps({
                "New": 0,
                "Edit": 0,
            }))
        return HttpResponse(json.dumps({
            "New": new,
            "Edit": edited,
            "New_Msgs": new_msgs,
            "Edit_Msgs": edit_list,
            "Len": all_msgs,
            "Edit_Len": f'{edit1_len},{edit2_len}',
        }))
    elif reload == '2':
        more_msgs = Msg.objects.filter(ring_id=ring_id).order_by('-time_stamp')[int(len_msgs):(int(len_msgs) + 20)]
        load_msgs = []
        for msg in more_msgs:
            if msg.Reply == '0':
                load_msgs.append([msg.id, msg.op.userprofile.Nick_Name, msg.op.userprofile.Profile_pic.url, msg.cnt,
                                 msg.side, '0', '0', msg.op.userprofile.id, msg.Reply])
            else:
                reply_msg = Msg.objects.get(id=msg.Reply)
                if msg.Edited == '0':
                    cnt = reply_msg.cnt
                elif msg.Edited == '1':
                    cnt = reply_msg.Edit_1
                else:
                    cnt = reply_msg.Edit_2
                if reply_msg.side == '0':
                    clr = 'Red'
                else:
                    clr = 'Blue'
                load_msgs.append([msg.id, msg.op.userprofile.Nick_Name, msg.op.userprofile.Profile_pic.url, msg.cnt,
                                 msg.side, '0', '0', msg.op.userprofile.id, msg.Reply, cnt, clr])
        return HttpResponse(json.dumps({
            "More_Msgs": load_msgs
        }))
    func = data(request)
    rings = Ring.objects.get(id=ring_id)
    msgs = Msg.objects.filter(ring_id=ring_id).order_by('time_stamp')[(all_msgs - 20):]
    ctx = {
        'user': request.user,
        'theme': func[3],
        'Ring': rings,
        'Msgs': msgs,
        'Ring_ID': ring_id,
        'Len_Msg': all_msgs,
        'Len_Edit1': edit1_len,
        'Len_Edit2': edit2_len,
    }
    return render(request, 'Ring.html', ctx)


def test(request, test_val):
    if test_val == 1:
        return HttpResponse(json.dumps({
            'Hi': ['Msg_1', 'Msg_5', 'Msg_9'],
            'Hey': (['Hey', 'Hi', 'Ho'], ['Jk', 'Jam'], ['Kill', 'Stupid'])}))
    return render(request, 'Test.html')


def god(request):
    func = data(request)
    ctx = {
        'url': func[0],
        'name': func[1],
        'date': func[2],
    }
    return render(request, 'Shrek.html', ctx)
