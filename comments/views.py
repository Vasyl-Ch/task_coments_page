# comments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.cache import cache
from django.views.decorators.http import require_http_methods

from .models import Comment
from .forms import CommentForm
from .sanitizer import sanitize_text

ALLOWED_SORTS = [
    "user_name",
    "-user_name",
    "email",
    "-email",
    "created_at",
    "-created_at",
]
COMMENTS_PER_PAGE = 25
CACHE_TTL = 60


@require_http_methods(["GET", "POST"])
def index(request):
    sort_by = request.GET.get("sort", "-created_at")
    if sort_by not in ALLOWED_SORTS:
        sort_by = "-created_at"

    page_number = request.GET.get("page", 1)

    reply_to = request.GET.get("reply_to", "")
    reply_comment = None
    if reply_to:
        reply_comment = get_object_or_404(Comment, id=reply_to)
    preview_text = None

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        action = request.POST.get("action", "submit")

        if action == "preview":
            raw_text = request.POST.get("text", "")
            preview_text = sanitize_text(raw_text)
        else:
            if form.is_valid():
                comment = form.save(commit=False)

                parent_id = request.POST.get("parent_id")
                if parent_id:
                    comment.parent = get_object_or_404(Comment, id=parent_id)

                comment.save()
                cache.clear()

                return redirect(f"/?sort={sort_by}&page={page_number}")
    else:
        form = CommentForm()
        if reply_to:
            form.initial["parent_id"] = reply_to

    cache_key = f"comments_{sort_by}_page_{page_number}"
    comments_page = cache.get(cache_key)

    if comments_page is None:
        root_qs = Comment.objects.filter(parent=None).order_by(sort_by)
        paginator = Paginator(root_qs, COMMENTS_PER_PAGE)
        comments_page = paginator.get_page(page_number)
        cache.set(cache_key, comments_page, CACHE_TTL)

    return render(
        request,
        "comments/index.html",
        {
            "comments_page": comments_page,
            "form": form,
            "sort_by": sort_by,
            "reply_to": reply_to,
            "reply_comment": reply_comment,
            "preview_text": preview_text,
            "page_number": page_number,
        },
    )
