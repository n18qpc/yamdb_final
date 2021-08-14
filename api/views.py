from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import ModelFilter
from api.models import Category, CustomUser, Genre, Review, Title
from api.permissions import (AdminPermission, GeneralPermission,
                             ReviewOwnerPermission)
from api.serializers import (CategoriesSerializer, CommentsSerializer,
                             GenreSerializer, ReviewsSerializer,
                             TitleGeneralSerializer, TitleSlugSerializer,
                             UserSerializer)
from api.utils import generate_confirmation_code, send_mail_to_user


class RegisterView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        confirmation_code = generate_confirmation_code()
        user_exists = CustomUser.objects.filter(email=email).exists()
        if not user_exists:
            data = {'email': email, 'confirmation_code': confirmation_code,
                    'username': email}
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            send_mail_to_user(email, confirmation_code)
        else:
            CustomUser.objects.filter(
                email=email).update(
                confirmation_code=confirmation_code)
            get_code = CustomUser.objects.values_list(
                'confirmation_code', flat=True).get(
                email=email)
            send_mail_to_user(email, get_code)
        return Response({'email': email}, status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def get_token(self, user):
        token = AccessToken.for_user(user)
        return str(token)

    def post(self, request):
        user = get_object_or_404(CustomUser, email=request.data.get('email'))
        if user.confirmation_code != request.data.get('confirmation_code'):
            response = {'confirmation_code': 'Неверный код для данного email'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {'token': self.get_token(user)}
        return Response(response, status=status.HTTP_200_OK)


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, AdminPermission,)

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = [GeneralPermission]

    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class CategoriesViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategoriesSerializer
    permission_classes = [GeneralPermission]

    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ModelFilter
    permission_classes = [GeneralPermission]
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSlugSerializer
        return TitleGeneralSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id), pk=review_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id), pk=review_id
        )
        serializer.save(author=self.request.user, review=review)
