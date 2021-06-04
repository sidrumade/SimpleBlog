from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView, FormMixin
from .form import EmailForm, CommentForm, SearchForm
from django.urls import reverse
from django.shortcuts import render,redirect

from django.http import Http404


# Create your views here.

class PostListView(ListView, FormView):
    model = Post
    context_object_name = 'posts'
    template_name = 'list.html'
    paginate_by = 2  # pagination each page shows 2 posts

    form_class = SearchForm


    def post(self, request, *args, **kwargs):

        blog_post=self.model.objects.get(title__contains=request.POST.get('search'))
        if blog_post is not None:
            return redirect(blog_post.get_absolute_url()) #reditect joing host+given url
        else:
            raise Http404('Post not found')



class PostDetailView(DetailView, FormMixin):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'post_detail'

    form_class = CommentForm  # this is for FormMixin

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs=self.kwargs)

    def get_object(self):

        post = self.kwargs['post']
        status = 'published'
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        obj = get_object_or_404(Post, slug=post,
                                status=status,
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
        return obj

    def post(self, request, *args, **kwargs):

        self.object = self.get_object() #always requird here
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        comments = self.get_object().comments.filter(active=True)
        context['comments'] = comments

        return context

    def form_valid(self, form):
        self.get_context_data().update({'data': 'hello'})


        new_comment = form.save(commit=False)
        new_comment.post = self.get_object()
        new_comment.name = form.cleaned_data['name']
        new_comment.email = form.cleaned_data['email']
        new_comment.body = form.cleaned_data['body']
        new_comment.save()
        return super().form_valid(form)


class EmailFormView(FormView):
    form_class = EmailForm
    template_name = 'form.html'
    success_url = 'thanks'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books

        context["post"] = Post.objects.get(pk=self.kwargs['post_id'])

        return context

    def form_valid(self, form):
        form.send_email(self.get_context_data())
        return super().form_valid(form)
