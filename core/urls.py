from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


def flat_pages():
    # the url for the pages are determined from the page name
    pages = [
        'about',
        'services',
        'portfolio',
    ]
    for page in pages:
        yield path(page+'/', views.Flat.as_view(page_name=page), name=page)



app_name = "core"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('blog/', views.BlogView.as_view(), name="blog"),
    path('blog/<slug:slug>/', views.BlogDetail.as_view(), name="blog_detail"),
    path('blog/<slug:slug>/comment/', views.BlogComment.as_view(), name="blog_comment"),
    path('synd-feed/', views.SynchFeed.as_view(), name='synd_feed'),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *flat_pages(),
]
