from rest_framework import serializers

from .models import Review, Comment, Recomment

class ReviewListSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    place_name = serializers.SerializerMethodField()
    review_like_count = serializers.SerializerMethodField()

    def get_nickname(self, obj):
        return obj.author.user_profile.nickname

    def get_profile_image(self, obj):
        return obj.author.user_profile.profile_image.url

    def get_place_name(self, obj):
        return obj.place.place_name

    def get_review_like_count(self, obj):
        return obj.review_like.count()

    class Meta:
        model = Review
        fields = ('title', 'content', 'review_image_one', 'created_at', 'updated_at', 'rating_cnt', 'review_like_count', 'review_like', 'nickname', 'profile_image', 'place_name', )

class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('title', 'content', 'rating_cnt', 'review_image_one', 'review_image_two', 'review_image_three', )
        extra_kwargs = {
                        'title':{
                        'error_messages':{
                        'required':'제목을 입력해주세요',
                        'blank':'제목을 입력해주세요',}},

                        'content':{
                        'error_messages': {
                        'required':'내용을 입력해주세요.',
                        'blank':'내용을 입력해주세요.',}},
                        
                        'rating_cnt':{
                        'error_messages':{
                        'required':'평점을 입력해주세요',
                        'blank':'평점을 입력해주세요',}},}

class ReviewDetailSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    place_name = serializers.SerializerMethodField()
    review_like_count = serializers.SerializerMethodField()

    def get_nickname(self, obj):
        return obj.author.user_profile.nickname

    def get_profile_image(self, obj):
        return obj.author.user_profile.profile_image.url

    def get_place(self, obj):
        return obj.place.place_name
        
    def get_review_like_count(self, obj):
        return obj.review_like.count()

    class Meta:
        model = Review
        fields = ('title', 'content', 'review_image_one', 'review_image_two', 'review_image_three', 'created_at', 'updated_at', 'rating_cnt', 'review_like', 'review_like_count', 'nickname', 'profile_image', 'place_name', )


class RecommentSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    recomment_like_count = serializers.SerializerMethodField()
    
    def get_nickname(self, obj):
        return obj.author.user_profile.nickname

    def get_profile_image(self, obj):
        return obj.author.user_profile.profile_image.url
    
    def get_recomment_like_count(self, obj):
        return obj.recomment_like.count()
    
    class Meta:
        model = Recomment
        fields = ('content', 'created_at', 'updated_at', 'recomment_like', 'comment', 'nickname', 'profile_image', 'recomment_like_count',)

class RecommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomment
        fields = ("content",)
        extra_kwargs = {'content':{
                        'error_messages': {
                        'required':'내용을 입력해주세요.',
                        'blank':'내용을 입력해주세요.',}},}

class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    comment_recomments = RecommentSerializer(many=True)
    comment_like_count = serializers.SerializerMethodField()
    review_title = serializers.SerializerMethodField()

    def get_nickname(self, obj):
        return obj.author.user_profile.nickname

    def get_profile_image(self, obj):
        return obj.author.user_profile.profile_image.url

    def get_comment_like_count(self, obj):
        return obj.comment_like.count()

    def get_review_title(self, obj):
        return obj.review.title

    class Meta:
        model = Comment
        fields = ('content', 'created_at', 'updated_at', 'comment_like', 'review_title', 'nickname', 'profile_image', 'comment_like_count','comment_recomments',)

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
        extra_kwargs = {'content':{
                        'error_messages': {
                        'required':'내용을 입력해주세요.',
                        'blank':'내용을 입력해주세요.',}},}