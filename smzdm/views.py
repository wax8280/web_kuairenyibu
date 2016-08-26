from django.shortcuts import redirect, render
from smzdm.models import case_info, his, item, filter, My_user
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
from tools.my_config import *
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from django.template.response import SimpleTemplateResponse
from tools.settings import SECRET_KEY
from .utils.token import Token
from .utils.functions import *
from .forms import LoginForm, UserForm
from django.contrib import auth
from django.contrib.auth.models import User

error_login_message = '密码或用户名错误.如果您是未激活的用户，请前往您的邮箱激活'
error_register_repeatuser = '用户名重复'
error_register_notvaild = '请准确填写'
error_register_ip_limit = '同一IP注册用户数超过限制，请与管理员联系'

IP_LIMIT = 10
IS_IP_LIMIT = True

token_confirm = Token(SECRET_KEY)


@login_required
def view_case_set(request):
    user = request.user.username
    e_mail_full = user + '@qq.com'

    caselists_ = case_info.objects.filter(e_mail=e_mail_full)
    return render(request, 'case_set.html',
                  {'caselists': caselists_, 'e_mail': user})


@login_required
def view_his(request, case_id, cur=0):
    limit = try_int(request.GET['limit'], 50) if 'limit' in request.GET else 50
    cur = try_int(cur, 0)
    user = request.user.username
    item_ = []
    e_mail_full = user + '@qq.com'

    try:
        count = his.objects.filter(case_id=case_id, user_email=e_mail_full).count()
        his_ = his.objects.filter(case_id=case_id, user_email=e_mail_full).order_by('-timesort')

    except Exception as e:
        count = 0
        his_ = []

    for each in his_:
        try:
            item_.append(item.objects.get(article_id=each.article_id))
        except Exception as e:
            pass

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

    return render(request, 'his.html',
                  {'item': item_, 'e_mail': user, 'case_id': case_id, 'next_cur': next_cur, 'prev_cur': prev_cur,
                   'no_next': no_next,
                   'no_prev': no_prev})


@login_required
def add_case(request, e_mail):
    if request.method == 'POST':
        case = case_info()
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

        # 一共3个filter
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
    limit = try_int(request.GET['limit'], 50) if 'limit' in request.GET else 50
    cur = try_int(cur, 0)
    user = request.user.username
    e_mali_full = user + '@qq.com'
    item_ = []

    try:
        count = his.objects.filter(user_email=e_mali_full).count()
        his_ = his.objects.filter(user_email=e_mali_full).order_by('-inserted_timesort')[cur:cur + limit]
    except:
        count = 0
        his_ = []

    for each in his_:
        try:
            item_.append(item.objects.get(article_id=each.article_id))
        except:
            pass

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

    return render(request, 'home.html',
                  {'item': item_, 'e_mail': user, 'next_cur': next_cur, 'prev_cur': prev_cur,
                   'no_next': no_next, 'no_prev': no_prev,})


@login_required
def delete_case(request, case_id):
    response_data = {}
    try:
        case_ = case_info.objects.get(case_id=case_id)
        case_.delete()
        response_data['result'] = '1'
    except:
        response_data['result'] = '0'

    return HttpResponse(json.dumps(response_data), content_type="application/json")


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
            if user is None or not user.is_active:
                error = error_login_message
                return render(request, 'login.html', {'form': form, 'error': error})

            auth.login(request, user)
            return redirect('home_page')
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


def register(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'register.html', {'form': form})
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            username, password, nick_name = form_data['username'], form_data['password'], form_data['nick_name']

            # IP注册限制
            ip = try_get_from_dict(request.META, 'REMOTE_ADDR', '0.0.0.0')
            if IS_IP_LIMIT:
                ip_count = My_user.objects.filter(register_ip=ip).count() if ip != '0.0.0.0' else 0
                if ip_count >= IP_LIMIT:
                    error = error_register_ip_limit
                    return render(request, 'register.html', {'form': form, 'error': error})

            try:
                User.objects.get(username=username)
                error = error_register_repeatuser
                return render(request, 'register.html', {'form': form, 'error': error})
            except:
                pass

            token = token_confirm.generate_validate_token(username)
            receivers = username + '@qq.com'
            e_mail_template = SimpleTemplateResponse('e_mail.html',
                                                     {'info': '来自“快人一步”的验证邮件', 'token': token, 'DOMAIM': DOMAIM})
            text = e_mail_template.render().content
            message = MIMEText(text, 'html', 'utf-8')
            message['From'] = Header(u"快人一步", 'utf-8')
            message['To'] = Header(nick_name, 'utf-8')
            message['Subject'] = Header('来自“快人一步”的验证邮件', 'utf-8')

            for i in range(10):
                try:
                    smtpObj = smtplib.SMTP(mail_host, 25)
                    smtpObj.login(mail_user, mail_pass)
                    smtpObj.sendmail(sender, receivers, message.as_string())
                    break
                except smtplib.SMTPException:
                    pass

            User.objects.create_user(username=username, password=password, is_active=False)
            return render(request, 'welcome_user_but_not_active.html', {'info': u"请登录到注册邮箱中验证用户，有效期为1个小时。"})

            # My_user.objects.create(user=u,register_ip=ip,nick_name=nick_name,username=username)
            # user = auth.authenticate(username=username, password=password)
            #
            # if user is not None and user.is_active:
            #     auth.login(request, user)
            #     return redirect('home_page')
        else:
            error = error_register_notvaild
            return render(request, 'register.html', {'form': form, 'error': error})


def active_user(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        return render(request, 'welcome_user_but_not_active.html', {'info': u'对不起，验证链接已经过期'})
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'welcome_user_but_not_active.html', {'info': u'对不起，您所验证的用户不存在，请重新注册'})

    user.is_active = True
    user.save()
    return redirect('login')
