from django.urls import path,re_path
from .views import PostListView,PostDetailView,EmailFormView
from django.views.generic.base import TemplateView


app_name = 'blog'
urlpatterns = [
    path('list/', PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/form/',EmailFormView.as_view(),name='email_form'),
    #path('<int:post_id>/form/thanks/',TemplateView.as_view(template_name='thanks.html'),name='thanks'),
    re_path('^(.*?)/thanks/$',TemplateView.as_view(template_name='thanks.html'),name='thanks'),
]