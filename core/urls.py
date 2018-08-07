from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view


# API Routes
from apps.author.views import AuthorViewSet
from apps.article.views import ArticleViewSet

router = DefaultRouter()

# API Docs
schema_view = get_swagger_view(title='med-news')
router.register(r'author', AuthorViewSet)
router.register(r'article', ArticleViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/docs/$', schema_view),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/', include((router.urls, 'api'), namespace='api')),
]
