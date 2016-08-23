from django.core.urlresolvers import resolve
from django.test import TestCase
from smzdm.views import home_page, login, add_user
from django.test import Client
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from smzdm.forms import LoginForm, UserForm
import re
from django.contrib.auth.models import User
from smzdm.views import error_login_message, error_add_user_notvaild
from django.utils.html import escape
from  unittest import skip
from smzdm.models import item, his


class HomePageTest(TestCase):
    def test_unlogin_to_homepage_redirect_to_login_view(self):
        client = Client()
        response = client.get('/smzdm/', follow=True)
        redirect_chain = response.redirect_chain
        self.assertEqual(redirect_chain[0], ('/smzdm/login/?next=/smzdm/', 302))
        self.assertEqual(response.resolver_match.func, login)

        # 这样也行
        # self.assertRedirects(response, '/smzdm/login/?next=/smzdm/')


class HomePageTest_logined(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='123', password='test')
        # item_ = item(article_id=1000, article_collection=10, article_comment=10, article_content='这是第一个测试的item',
        #              article_data='2015-01-01', article_download_pic='ppp,ppp', article_link='www.test.com',
        #              article_mall='test', article_pic='', article_price=100, article_rating=10,
        #              article_title='这是第一个测试的item',timesort=1000)
        # item_.save()
        # item_ = item(article_id=1000, article_collection=10, article_comment=10, article_content='这是第二个测试的item',
        #      article_data='2015-01-01', article_download_pic='ppp,ppp', article_link='www.test.com',
        #      article_mall='test', article_pic='', article_price=100, article_rating=10,
        #      article_title='这是第二个测试的item',timesort=1001)
        # item_.save()
        cls.client = Client()
        # 这里登录似乎不行
        # cls.client.login(username='123', password='test')

    def test_loginde_to_homepage(self):
        self.client.login(username='123', password='test')
        response = self.client.get('/smzdm/', follow=True)
        self.assertEqual(response.resolver_match.func, home_page)

    def test_homepage_view_renders_home_template(self):
        self.client.login(username='123', password='test')
        response = self.client.get('/smzdm/')
        # 使用辅助方法 assertTemplateUsed 替换之前手动测试模板的代码。
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_view_returns_correct_html(self):
        self.client.login(username='123', password='test')
        response = self.client.get('/smzdm/')
        e_mail = '123'
        e_mail_full = e_mail + '@qq.com'
        item_ = []
        try:

            his_ = his.objects.filter(user_email=e_mail_full).order_by('-timesort')
            for each in his_:
                item_.append(item.objects.get(article_id=each.article_id))

        except Exception as e:
            pass

        expected_html = render_to_string('home.html', {'item': item_, 'e_mail': e_mail})

        patten = re.compile(r"<input type='hidden'.*?/>")
        searchObj = patten.sub('', response.content.decode())
        self.assertEqual(searchObj, expected_html)


class LoginTest(TestCase):
    def test_login_url_resolves_to_login_view(self):
        client = Client()
        response = client.get('/smzdm/login/')
        self.assertEqual(response.resolver_match.func, login)

    def test_login_view_returns_correct_html(self):
        client = Client()
        response = client.get('/smzdm/login/')
        a = response.content.decode()
        expected_html = render_to_string('login.html', {'form': LoginForm()})

        # because of token,not equal
        # self.assertEqual(response.content.decode(), expected_html)
        # 官方文档说，但是实际上csrf依然存在。所以使用正则去除
        # By default, the test client will disable any CSRF checks performed by your site
        patten = re.compile(r"<input type='hidden'.*?/>")
        searchObj = patten.sub('', response.content.decode())
        self.assertEqual(searchObj, expected_html)

    def test_login_view_renders_login_template(self):
        response = self.client.get('/smzdm/login/')
        # 使用辅助方法 assertTemplateUsed 替换之前手动测试模板的代码。
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_uses_LoginForm(self):
        response = self.client.get('/smzdm/login/')
        # 使用 assertIsInstance 确认视图使用的是正确的表单类。
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_login_to_login_user_and_redirect_home_page(self):
        User.objects.create_user(username='test', password='test')
        client = Client()
        response = client.post('/smzdm/login/', {'username': 'test', 'password': 'test'}, follow=True)
        self.assertEqual(response.resolver_match.func, home_page)

    def test_login_to_login_user(self):
        User.objects.create_user(username='test', password='test')
        client = Client()
        response = client.login(username='test', password='test')
        self.assertTrue(response)

    def test_for_invalid_user_login(self):
        User.objects.create_user(username='test', password='test')
        client = Client()
        response = client.post('/smzdm/login/', {'username': 'invalid_test', 'password': 'invalid_test'}, follow=True)
        self.assertEqual(response.resolver_match.func, login)

    def test_for_invalid_login_shows_error_on_page(self):
        User.objects.create_user(username='test', password='test')
        client = Client()
        response = client.post('/smzdm/login/', {'username': 'invalid_test', 'password': 'invalid_test'}, follow=True)

        self.assertContains(response, escape(error_login_message))


class add_userTest(TestCase):
    def test_add_user_url_resolves_to_add_user_view(self):
        client = Client()
        response = client.get('/smzdm/add_user/')
        self.assertEqual(response.resolver_match.func, add_user)

    def test_add_user_view_returns_correct_html(self):
        client = Client()
        response = client.get('/smzdm/add_user/')

        expected_html = render_to_string('add_user.html', {'form': UserForm()})
        patten = re.compile(r"<input type='hidden'.*?/>")
        searchObj = patten.sub('', response.content.decode())
        self.assertEqual(searchObj, expected_html)

    def test_add_user_view_renders_add_user_template(self):
        response = self.client.get('/smzdm/add_user/')
        self.assertTemplateUsed(response, 'add_user.html')

    def test_add_user_view_uses_UserForm(self):
        response = self.client.get('/smzdm/add_user/')
        # 使用 assertIsInstance 确认视图使用的是正确的表单类。
        self.assertIsInstance(response.context['form'], UserForm)

    # text
    @skip
    def test_add_user_to_add_user_and_redirect_home_page(self):
        client = Client()
        response = client.post('/smzdm/add_user/', {'username': 'test', 'password': 'test', 'password_again': 'test'},
                               follow=True)
        self.assertEqual(response.resolver_match.func, home_page)

    # num
    def test_add_user_to_add_user_and_redirect_home_page(self):
        client = Client()
        response = client.post('/smzdm/add_user/', {'username': '123', 'password': 'test', 'password_again': 'test'},
                               follow=True)
        self.assertEqual(response.resolver_match.func, home_page)

    # num
    def test_add_user_to_add_user(self):
        client = Client()
        client.post('/smzdm/add_user/', {'username': '123', 'password': 'test', 'password_again': 'test'}, follow=True)
        response = client.login(username='123', password='test')
        self.assertTrue(response)

    def test_for_invalid_add_user_of_text_username(self):
        client = Client()
        response = client.post('/smzdm/add_user/', {'username': 'text', 'password': 'test', 'password_again': 'test'},
                               follow=True)
        self.assertEqual(response.resolver_match.func, add_user)

    def test_for_invalid_add_user_shows_error_on_page(self):
        client = Client()
        response = client.post('/smzdm/add_user/', {'username': 'text', 'password': 'text', 'password_again': 'test'},
                               follow=True)

        self.assertContains(response, escape(error_add_user_notvaild))

    # num
    # 这个一般不在数据库因此错误，所以就只在前端检查了
    @skip
    def test_for_invalid_of_password_not_euqual_password_again(self):
        client = Client()
        response = client.post('/smzdm/add_user/', {'username': '123', 'password': 'text', 'password_again': 'test1'},
                               follow=True)
        self.assertContains(response, escape(error_add_user_notvaild))
