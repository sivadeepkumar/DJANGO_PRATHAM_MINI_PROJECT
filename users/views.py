from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from noticeboard.models import NoticeBoard
from django.contrib.auth.models import Group


def user_not_authenticated(user):
    print(user.is_authenticated)
    return not user.is_authenticated

@login_required
def noticeboard(request):
    user_type = request.user.last_name
    print(user_type)
    if user_type == 'student':
        Noticeboards = NoticeBoard.objects.filter(user__groups__name__in=['Student Group'])
    else:
        Noticeboards = NoticeBoard.objects.all()
    return render(request, 'noticeboard.html', {'Noticeboards': Noticeboards})



@login_required
@user_passes_test(lambda user: user.groups.filter(name__in=['Principal Group','Teacher Group']).exists(), login_url='/noticeboard/')
def addnotice(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        # Retrieve the notice details from the POST request
        notice_text = request.POST.get('notice')
        message_text = request.POST.get('message')
        if notice_text and message_text:
            # Create a new notice for the user
            notice = NoticeBoard(user=user, notice=notice_text, message=message_text)
            notice.save()
            return redirect('dummy')
    return render(request, 'addnotice.html', {'user': user})


@login_required
@user_passes_test(lambda user: user.groups.filter(name__in=['Principal Group','Teacher Group']).exists(), login_url='/noticeboard/')
def dummy(request):
    user_type = request.user.last_name
    print(user_type) 
    if user_type == 'teacher' :
        users = User.objects.exclude(last_name='principal')
    else:
        users = User.objects.all()
    # notices = NoticeBoard.objects.all()
    values = {'users': users}   #'Notices': notices
    return render(request,'dummy.html',values)

@login_required
def user_logout(request):
    logout(request)
    return redirect('login_page')


@user_passes_test(user_not_authenticated, login_url='/')
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        print(username,password,user_type)
        if not User.objects.filter(username = username).exists():
            messages.error(request,'User Not Availabe.....Create account ')
            return redirect('/register/')
        else:
            user_obj = authenticate(request,username=username,password=password,last_name=user_type)
            if user_obj and user_obj.last_name == user_type :
                # print('AAA',user_obj.last_name)
                login(request,user_obj)
                if user_type == 'teacher' or user_type == 'student':
                    return redirect('/')
                return redirect('/')
            
            else:
                messages.error(request,'In-Valid Details')
                return redirect('/login/')
        
    return render(request,'login.html')


@login_required
@user_passes_test(lambda user: user.groups.filter(name__in=['Principal Group']).exists(), login_url='/noticeboard/')
def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        last_name = request.POST.get('user_type')
        print(firstname,username,password,last_name)
        user_type = last_name
        if User.objects.filter(username = username).exists():
            messages.error(request,'User Name is Taken')
        else:
            user_obj = User.objects.create(first_name = firstname,username = username,last_name = last_name)
            user_obj.set_password(password)
            user_obj.save()
            print(last_name)
            if user_type == 'principal':
                group = Group.objects.get(name='Principal Group')
            elif user_type == 'teacher':
                group = Group.objects.get(name='Teacher Group')
            elif user_type == 'student':
                group = Group.objects.get(name='Student Group')
            else:
                group = None 
                return redirect('/fighter')

            if group:
                user_obj.groups.add(group)



            messages.success(request,'User Name is Created Successfully')
            return redirect('/login/')
    return render(request,'register.html')
