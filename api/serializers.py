from rest_framework import serializers

from .models import Category, Comment, CustomUser, Genre, Review, Title


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSlugSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, slug_field='slug',
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'


class TitleGeneralSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    score = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if self.context['request'].method != 'POST':
            return data
        review_exists = Review.objects.filter(
            title=title_id, author=user).exists()
        if review_exists:
            raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data

    class Meta:
        model = Review

        fields = ('id', 'pub_date', 'author', 'text', 'score', 'title')
        read_only_fields = ('id', 'pub_date', 'author', 'title')


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date', 'author')


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default=CustomUser.UserRole.USER)

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role', 'confirmation_code')
        model = CustomUser
        extra_kwargs = {'confirmation_code': {'write_only': True},
                        'username': {'required': True},
                        'email': {'required': True}}
