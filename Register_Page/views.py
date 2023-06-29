import cloudinary.uploader
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from Register_Page.forms import CreateUser, VerifyUser, UserProfilePage, UserEdit
from .models import UserProfile, Theme
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_user


# Create your views here.
def data(request):
    username = request.user.id
    users = UserProfile.objects.get(user_id=username)
    theme = Theme.objects.get(user_id=users.id)
    url = users.Profile_pic.url
    name = users.Nick_Name
    date = users.date_created
    return url, name, date, theme


def register(request):
    profiles = UserProfilePage()
    forms = CreateUser()
    if request.method == 'POST':
        profiles = UserProfilePage(request.POST, request.FILES)
        forms = CreateUser(request.POST)
        if forms.is_valid() and profiles.is_valid():
            user = forms.save(commit=False)
            username = forms.cleaned_data.get('username')
            user.username = username
            forms.save()
            group = Group.objects.get(name='user')
            user.groups.add(group)
            profile = profiles.save(commit=False)
            profile.user = user
            profile.save()
            theme = Theme()
            theme.save()
            messages.success(request, 'Account was successfully created for ' + username)
            return redirect('Login_Page')
    ctx = {
        'forms': forms,
        'profiles': profiles,
    }
    return render(request, 'Register.html', ctx)


def login_page(request):
    forms = VerifyUser()
    ctx = {'forms': forms}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.info(request, "Username or Password is Incorrect")
    return render(request, 'Login.html', ctx)


def logout_user(request):
    logout(request)
    return redirect('Home_Page')


def edit(request):
    func = data(request)
    form = UserEdit(initial={'email': request.user.email})
    profile = UserProfilePage(initial={'Nick_Name': request.user.userprofile.Nick_Name,
                                       'Profile_pic': request.user.userprofile.Profile_pic.url})
    if request.method == "POST":
        form = UserEdit(data=request.POST or None, instance=request.user)
        profile = UserProfilePage(data=request.POST or None, instance=request.user.userprofile, files=request.FILES)
        if form.is_valid() and profile.is_valid():
            model = UserProfile.objects.get(user=request.user)
            cloudinary.uploader.destroy(model.Profile_pic.public_id, invalidate=True)
            user = form.save()
            profiles = profile.save()
            return redirect("Profile_Page")
    ctx = {
        'form': form,
        'profile': profile,
        'url': func[0],
        'name': func[1],
        'date': func[2],
    }
    return render(request, "Edit_User.html", ctx)


def navbar(request):
    profiles = UserProfilePage(request=request)
    ctx = {'profiles': profiles}
    return render(request, "Navbar.html", ctx)


def show_profile(request):
    func = data(request)
    ctx = {
        'url': func[0],
        'name': func[1],
        'date': func[2],
    }
    return render(request, "User_Profile.html", ctx)


def user_list(request):
    func = data(request)
    users = UserProfile.objects.all()
    ctx = {
        'users': users,
    }
    return render(request, "User_List.html", ctx)


def theme_builder(request):
    func = data(request)
    if request.POST.get("Act") == "ChangeTheme" and request.is_ajax():
        theme = Theme.objects.get(user_id=request.user.userprofile.id)
        theme.Nav_Back = request.POST.get("Nav_Back")
        theme.Nav_Color = request.POST.get("Nav_Color")
        theme.Nav_Line = request.POST.get("Nav_Line")
        theme.Card_Back = request.POST.get("Card_Back")
        theme.Card_Color = request.POST.get("Card_Color")
        theme.Card_Border = request.POST.get("Card_Border")
        theme.Body_Back = request.POST.get("Body_Back")
        theme.save()
        return redirect("Profile_Page")
    else:
        ctx = {
            'url': func[0],
            'name': func[1],
            'date': func[2],
            'theme': func[3],
        }
        return render(request, "Theme.html", ctx)