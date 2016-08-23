from django.conf.urls import url

from smzdm import views

urlpatterns = [
    url(r'^case_set/$', views.view_case_set, name='view_case_set'),
    url(r'^case_set/(?P<case_id>[0-9]+)/$',views.view_his,name='view_his'),
    url(r'^(?P<e_mail>[0-9]+)/add_case/$',views.add_case,name='add_case'),
    url(r'^$',views.home_page,name='home_page'),
    url(r'^pages/(?P<cur>[0-9]+)/$',views.home_page,name='home_page_with_pages'),
    url(r'^case_set/case_delete/(?P<case_id>[0-9]+)/$',views.delete_case,name='delete_case'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^add_user/$',views.add_user,name='add_user'),
    url(r'^user_info/$',views.view_user_info,name='view_user_info'),
]