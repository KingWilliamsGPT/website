import random
import urllib.parse

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, RedirectView

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser

from .models import Blog, Comment
from . import forms


def redirect(url):
    return HttpResponseRedirect(url)


class IndexView(TemplateView):
    template_name = "core/index.html"


class Flat(IndexView):
    template_name = "core/index.html"
    page_name = "index"
    
    def get(self, request):
        return render(request, self.add_app(self.page_name), {})
    
    
    def add_app(self, page):
        return 'core/' + page + '.html'


class BaseBlogView:
    model = Blog
    
    def recent_blogs(self):
        return self.model.objects.order_by('-created_when')[:5]
    
    def get_context_data(self, *a, **kw):
        context = super().get_context_data(*a, **kw)
        context.update({
            "recent_blogs": self.recent_blogs()
        })
        return context


class BlogView(BaseBlogView, ListView):
    template_name = "core/blog.html"
    context_object_name = 'blogs'
    paginate_by = 7

    # def get_queryset(self):
    #     objects = self.model.objects.all()
    #     return random.choices(objects, k=15)


class BlogDetail(BaseBlogView, DetailView):
    model = Blog
    template_name = "core/blog_single.html"
    context_object_name = "blog"


class BlogComment(BlogDetail):
    def post(self, request, slug):
        blog = get_object_or_404(self.model, slug=slug)
        user = self.get_user(request)
        
        comment = Comment(username=user.username,
                            comment_text=request.POST.get('comment'),
                            # is_anonymous=user.is_anonymous,
                            )
        
        if not user.is_anonymous:
            comment.user = user
        
        comment.blog = blog
        comment.save()
        return redirect(
            reverse_lazy('core:blog_detail', kwargs={'slug':slug}))
    
    def get_user(self, request):
        post = request.POST
        name, email, comment = post.get('name'), post.get('email'), post.get('comment')
        try:
            user = auth.get_user(request)
        except Exception as ex:
            # print(ex, 'exc'*300)
            user = AnonymousUser()
            user.username = name
        return user


def add_params(more_params, url):
    from_uri = urllib.parse.urlsplit(url)
    uri, p, fragment = from_uri[:-2], from_uri[-2], from_uri[-1]

    # conver the ?query=string+to=a dictionary
    params = {}
    for token in p.split('&'):
        x = token.split('=')
        if len(x) >= 2:
            params[x[0]] = x[1]

    q = urllib.parse.quote
    # do what you were made for add to that dict
    params.update(more_params)
    params = '&'.join(('%s=%s' % (q(k), q(v)) for k,v in params.items()))
    ret = urllib.parse.urlunsplit([*uri, (params), fragment])
    # raise Exception
    return ret

def send_msg(url, msg, **kw):
    return add_params({'msg': msg, **kw}, url)


class SynchFeed(TemplateView):
    url = reverse_lazy('core:index')
    def post(self, request):
        form = forms.SyncFeedForm(request.POST)
        req_uri = request.POST['uri']

        if form.is_valid():
            return HttpResponseRedirect(
                send_msg(req_uri, 'You were added successfuly', code='0')
            )
        return HttpResponseRedirect(
            send_msg(req_uri, 'Invalid email address', email=form['email'].value(), code='1')
        )
        