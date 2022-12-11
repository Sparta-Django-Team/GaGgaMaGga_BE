from rest_framework import serializers

from .models import Review, Comment, Recomment, Report
from places.models import Place
from places.serializers import PlaceSerializer

# 후기 전체 serializer
class ReviewListSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    place_name = serializers.SerializerMethodField()
    review_like_count = serializers.SerializerMethodField()
    place = PlaceSerializer()

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
        fields = ('content', 'review_image_one', 'created_at', 'updated_at', 'rating_cnt', 'review_like_count', 'review_like','author_id' , 'nickname', 'profile_image', 'place_name', 'id','author_id','place_id','place')

# 후기 생성, 수정 serializer
class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('content', 'rating_cnt', 'review_image_one', 'review_image_two', 'review_image_three', )
        extra_kwargs = {'content':{
                        'error_messages': {
                        'required':'내용을 입력해주세요.',
                        'blank':'내용을 입력해주세요.',}},
                        
                        'rating_cnt':{
                        'error_messages':{
                        'required':'평점을 입력해주세요',
                        'blank':'평점을 입력해주세요',}},}

    def validate(self, data):
        http_method = self.context.get("request").method
        new_review_rating = data.get('rating_cnt')
        place = Place.objects.get(id=self.context.get("place_id"))
        review_cnt = place.place_review.count()

        # 리뷰 생성시(별점 계산)
        if http_method == "POST":
            place.rating = (place.rating * review_cnt + new_review_rating) / (review_cnt + 1)
            
            place.save()

        # 리뷰 수정시(별점 계산)
        if http_method == "PUT":
            current_review_rating = Review.objects.get(id=self.context.get("review_id")).rating_cnt # 원래 별점

            place.rating = (place.rating * review_cnt - current_review_rating + new_review_rating) / review_cnt

            place.save()

        return data

# 대댓글 serializer
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

# 대댓글 생성, 수정 serializer
class RecommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recomment
        fields = ('content',)
        extra_kwargs = {'content':{
                        'error_messages': {
                        'required':'내용을 입력해주세요.',
                        'blank':'내용을 입력해주세요.',}},}

# 댓글 serializer
class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    comment_recomments = RecommentSerializer(many=True)
    comment_like_count = serializers.SerializerMethodField()
    review_content = serializers.SerializerMethodField()

    def get_nickname(self, obj):
        return obj.author.user_profile.nickname

    def get_profile_image(self, obj):
        return obj.author.user_profile.profile_image.url

    def get_comment_like_count(self, obj):
        return obj.comment_like.count()

    def get_review_content(self, obj):
        return obj.review.content

    class Meta:
        model = Comment
        fields = ('content','id', 'created_at', 'updated_at', 'comment_like', 'review_content', 'nickname', 'profile_image', 'comment_like_count','comment_recomments',)

# 댓글 생성 serializer
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)
        extra_kwargs = {'content':{
                        'error_messages': {
                        'required':'내용을 입력해주세요.',
                        'blank':'내용을 입력해주세요.',}},}

# 후기 상세페이지 serializer
class ReviewDetailSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    place_name = serializers.SerializerMethodField()
    review_like_count = serializers.SerializerMethodField()
    review_comments = CommentSerializer(many=True)

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
        fields = ('content','author_id', 'review_image_one', 'review_image_two', 'review_image_three', 'created_at', 'updated_at', 'rating_cnt', 'review_like', 'review_like_count', 'nickname', 'profile_image', 'place_name','review_comments' )

# 신고 생성serializer
class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ('content', 'category', )
        extra_kwargs = {'content':{
                        'error_messages': {
                        'required':'내용을 입력해주세요.',
                        'blank':'내용을 입력해주세요.',}},
                        
                        'category':{
                        'error_messages':{
                        'required':'카테고리를 선택해주세요.',
                        'blank':'카테고리를 선택해주세요.',}}}