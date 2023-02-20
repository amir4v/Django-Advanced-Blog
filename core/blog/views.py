from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    TemplateView,
    RedirectView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from .models import Post
from .forms import PostForm


def indexView(request):
    """
    a function based view to show index page
    """
    return render(request, "index.html", context={"name": "Amir-fbv"})


class IndexView(TemplateView):
    """
    A class based view to show index page
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Amir-c"
        context["posts"] = Post.objects.all()
        return context


"""
Function based view sample:
from django.shortcuts import redirect
def redirect_to(request):
    return redirect('url')
"""


class RedirectToDjango(RedirectView):
    url = "https://djangoproject.com"

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        print(post)
        return super().get_redirect_url(*args, **kwargs)


class PostListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = "blog.view_post"
    queryset = Post.objects.all()
    context_object_name = "posts"
    # paginate_by = 1
    ordering = "-id"

    # def get_queryset(self):
    #     posts = Post.objects.filter()
    #     return posts


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = '__all__'
    form_class = PostForm
    success_url = "/blog/posts/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/posts/"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/blog/posts/"
