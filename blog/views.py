from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, ListView

from .models import Article, Subscribe, Mark


class AllBlogsView(ListView):
    model = User
    template_name = 'blog/allblogs.html'

    def get_queryset(self):
        return User.objects.all()


@method_decorator(login_required, name='dispatch')
class CreateArticleView(CreateView):
    model = Article
    fields = ('title', 'text')
    template_name = 'blog/add_article.html'

    def form_valid(self, form):
        form_data = form.cleaned_data
        Article.objects.create(author=self.request.user, **form_data)
        return HttpResponseRedirect(reverse('blog:user_blog', args=[self.request.user.pk]))


class Blog(ListView):
    model = Article
    template_name = 'blog/blog.html'

    def get_queryset(self):
        return Article.objects.filter(author_id=self.kwargs.get('author_pk'))


@method_decorator(login_required, name='dispatch')
class Feed(ListView):
    template_name = 'blog/feed.html'

    def get_queryset(self):
        subscribes = Subscribe.objects.filter(follower_id=self.request.user.pk).values_list('target_id', flat=True)
        return Article.objects.filter(author_id__in=subscribes)


@method_decorator(login_required, name='dispatch')
class MarkReadView(View):

    def post(self, request, *args, **kwargs):
        mark_data = {'owner_id': request.user.pk, 'article_id': kwargs.get('article_id')}
        mark_status = 'mark'
        try:
            Mark.objects.get(**mark_data).delete()
            mark_status = 'unmark'
        except Mark.DoesNotExist:
            Mark.objects.create(**mark_data)


@method_decorator(login_required, name='dispatch')
class SubscribeView(View):

    def post(self, request, *args, **kwargs):
        subscribe_data = {'follower_id': request.user.pk,
                          'target_id': kwargs.get('target_id')}
        subscribe_status = 'follow'
        try:
            Subscribe.objects.get(**subscribe_data).delete()
            subscribe_status = 'unfollow'
        except Subscribe.DoesNotExist:
            Subscribe.objects.create(**subscribe_data)

        return JsonResponse({'status': subscribe_status})
