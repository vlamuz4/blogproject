from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.cache import cache_page
from datetime import timedelta
from .models import Post, Comment
from .forms import CommentForm


@cache_page(300)
def post_list(request):
    posts = Post.objects.select_related('author')
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.prefetch_related('comments__author'),
        pk=pk
    )
    comments = post.comments.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            now = timezone.now()
            limit = now - timedelta(minutes=5)
            count = Comment.objects.filter(author=request.user, created__gte=limit).count()

            if count >= 3:
                form.add_error(None, "Ліміт 3 коментарі за 5 хв.")
            else:
                c = form.save(commit=False)
                c.post = post
                c.author = request.user
                c.save()
                return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })
