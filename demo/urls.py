from django.urls import path
from demo.views import WeiboNoteListCreate,\
    WeiboNoteCommentRetrieveUpdateDestroy,\
    WeiboNoteCommentListCreate,\
    WeiboNoteRetrieveUpdateDestroy,\
    WeiboNoteCommentFilterView,\
    WeiboNoteFilterView,\
    CommentFilterView,\
    CommentWordFrequencyView,\
    IpStaticsView,\
    CommentAnalysisView,\
    keyword_crawl_view,\
    blog_crawl_view,\
    CrawlSearchView

urlpatterns = [
    path('blog/', WeiboNoteListCreate.as_view(), name='blog-list-create'),
    path('blog/<int:pk>/', WeiboNoteRetrieveUpdateDestroy.as_view(), name='blog-detail'),
    path('comment/', WeiboNoteCommentListCreate.as_view(), name='comment-list-create'),
    path('comment/<int:pk>/', WeiboNoteCommentRetrieveUpdateDestroy.as_view(), name='comment-detail'),
    path('comment-filter/', WeiboNoteCommentFilterView.as_view(), name='comment-list'),
    path('blog-filter/', WeiboNoteFilterView.as_view(), name='blog-list'),
    path('comment-clean/', CommentFilterView.as_view(), name='comment-clean'),
    path('word-frequency/', CommentWordFrequencyView.as_view(), name='word_frequency'),
    path('ip-statics/', IpStaticsView.as_view(), name='ip-statics'),
    path('analysis/', CommentAnalysisView.as_view(), name='analysis'),
    path('keyword_crawl/', keyword_crawl_view, name='keyword_crawl'),
    path('blog_crawl/', blog_crawl_view, name='blog_crawl'),
    path('async_task/', CrawlSearchView.as_view()),
]