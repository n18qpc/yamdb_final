from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentViewSet, GenreViewSet,
                    RegisterView, ReviewViewSet, TitleViewSet, TokenView,
                    UsersViewSet)

v1_router = DefaultRouter()
v1_router.register('categories', CategoriesViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='review')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/'
                   r'(?P<review_id>\d+)/comments',
                   CommentViewSet, basename="reviews_comments")
v1_router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(v1_router.urls)),
    path('v1/auth/email/', RegisterView.as_view(),
         name='get_confirmation_code'),
    path('v1/auth/token/', TokenView.as_view(), name='get_token'),
]
