from django.shortcuts import redirect, render
from smzdm.models import case_info, his, item, filter
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required

error_login_message = '密码或用户名错误'
error_add_user_repeatuser = '用户名重复！'
error_add_user_notvaild = '请准确填写'



@login_required
def view_case_set(request):

    user = request.user.username

    e_mail_full = user + '@qq.com'

    try:
        caselists_ = case_info.objects.filter(e_mail=e_mail_full)

    except Exception as e:
        error = "您还没有推送呢！赶紧添加一条吧。"
        return render(request, 'case_set.html', {'error': str(error)})

    return render(request, 'case_set.html',
                  {'caselists': caselists_, 'e_mail': user})


@login_required
def view_his(request, case_id, cur=0):

    try:
        limit = int(request.GET['limit']) if request.GET['limit'] else 50
    except:
        limit = 50

    try:
        cur = int(cur)
    except:
        cur = 0

    user = request.user.username
    item_ = []
    e_mail_full = user + '@qq.com'
    no_next = 0
    no_prev = 0
    next_cur = cur
    prev_cur = cur
    try:
        count = his.objects.filter(case_id=case_id, user_email=e_mail_full).count()
        his_ = his.objects.filter(case_id=case_id, user_email=e_mail_full).order_by('-timesort')
        for each in his_:
            item_.append(item.objects.get(article_id=each.article_id))

        if cur + limit > count:
            next_cur = cur
            no_next = 1
        else:
            next_cur = cur + limit
            no_next = 0

        if cur - limit < 0:
            prev_cur = cur
            no_prev = 1
        else:
            prev_cur = cur - limit
            no_prev = 0
    except Exception as e:
        pass

    return render(request, 'his.html',
                  {'item': item_, 'e_mail': user,'case_id':case_id, 'next_cur': next_cur, 'prev_cur': prev_cur, 'no_next': no_next,
                   'no_prev': no_prev})


from django.http import HttpResponsePermanentRedirect


@login_required
def add_case(request, e_mail):
    has_session = bool(getattr(request, 'session', False))

    if not has_session:
        return redirect('login')

    if request.method == 'POST':
        case = case_info()
        case.user_name = request.user.username
        case.count = 0
        case.type = request.POST.get('case_type', '1')
        case.keyword = request.POST.get('case_keyword', '0')
        case.fromwhere = request.POST.get('case_from_where', '0')
        case.e_mail = e_mail + '@qq.com'
        case.save()

        filter_type_bef_list = []
        filter_kw_bef_list = []
        filter_type_bef = 'filter_type_'
        filter_kw_bef = 'filter_keyword_'

        for i in range(1, 4):
            filter_type_bef_list.append(filter_type_bef + str(i))
            filter_kw_bef_list.append(filter_kw_bef + str(i))

        i_ = 0
        for each in filter_type_bef_list:
            i_ += 1

            request_temp_ = request.POST.get(each, '0')
            if request_temp_ == '0':
                break

            filter_ = filter()
            filter_.type = request_temp_
            filter_.keyword = request.POST.get('filter_keyword_' + str(i_), '0')
            filter_.filter = case
            filter_.save()
            del filter_

        return redirect('view_case_set')

    return render(request, 'add_case.html', {'e_mail': e_mail})


@login_required
def home_page(request, cur=0):
    has_ip='REMOTE_ADDR' in request.META.keys()
    if has_ip:
        ip=request.META['REMOTE_ADDR']

    try:
        limit = int(request.GET['limit']) if 'limit' in request.GET else 50
    except:
        limit = 50

    try:
        cur = int(cur)
    except:
        cur = 0

    user = request.user.username

    e_mali_full = user + '@qq.com'
    item_ = []
    no_next = 0
    no_prev = 0
    next_cur = cur
    prev_cur = cur
    try:

        count = his.objects.filter(user_email=e_mali_full).count()
        his_ = his.objects.filter(user_email=e_mali_full).order_by('-inserted_timesort')[cur:cur + limit]
        for each in his_:
            item_.append(item.objects.get(article_id=each.article_id))

        if cur + limit > count:
            next_cur = cur
            no_next = 1
        else:
            next_cur = cur + limit
            no_next = 0

        if cur - limit < 0:
            prev_cur = cur
            no_prev = 1
        else:
            prev_cur = cur - limit
            no_prev = 0

    except Exception as e:
        pass

    return render(request, 'home.html',
                  {'item': item_, 'e_mail': user, 'next_cur': next_cur, 'prev_cur': prev_cur,
                   'no_next': no_next, 'no_prev': no_prev,'debug':ip})


@login_required
def delete_case(request, case_id):

    user = request.user.username

    response_data = {}
    try:
        case_ = case_info.objects.get(case_id=case_id)
        case_.delete()
        response_data['result'] = '1'
    except:
        response_data['result'] = '0'

    return HttpResponse(json.dumps(response_data), content_type="application/json")


from .forms import LoginForm, UserForm
from django.contrib import auth
from django.contrib.auth.models import User


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form,})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('home_page')
            else:
                error = error_login_message
                return render(request, 'login.html', {'form': form, 'error': error})
        else:
            error = error_login_message
            return render(request, 'login.html', {'form': form, 'error': error})


@login_required
def logout(request):
    auth.logout(request)
    form = LoginForm()
    return render(request, 'login.html', {'form': form,})


@login_required
def view_user_info(request):
    return render(request, 'user_info.html')


def add_user(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'add_user.html', {'form': form})
    else:
        form = UserForm(request.POST)
        err = form.is_valid()
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                User.objects.get(username=form_data['username'])
                error = error_add_user_repeatuser
                return render(request, 'add_user.html', {'form': form, 'error': error})
            except:
                pass

            User.objects.create_user(username=form_data['username'], password=form_data['password'])
            user = auth.authenticate(username=form_data['username'], password=form_data['password'])
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('home_page')
        else:
            error = error_add_user_notvaild
            return render(request, 'add_user.html', {'form': form, 'error': error})
