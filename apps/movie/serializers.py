
from rest_framework import serializers
from movie import models
from users.serializers import UserProfileModelSerializer


# 标签的序列化
class MovieTagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['name']


# 电影的序列化
class MovieModelSerializer(serializers.ModelSerializer):
    # 标签tag是电影的外键
    tag = MovieTagModelSerializer()  # 如果不写，在序列化的时候只是显示tag所绑定的id，many=True表示需要多个字段

    class Meta:
        model = models.Movie
        # fields = ['id', 'title', 'logo', 'star', 'tag', 'movie_file', 'release_time', 'play_nums', 'comment_nums','length']
        fields = '__all__'


# 用户评论的序列化
class CommentModelSerializer(serializers.ModelSerializer):
    # 电影和用户是评论的外键
    movie = MovieModelSerializer()
    user = UserProfileModelSerializer()

    class Meta:
        model = models.Comment
        fields = ['id', 'content', 'add_time', 'movie', 'user']


# 上映预告序列化
class Preview(serializers.ModelSerializer):
    class Meta:
        model = models.Preview
        fields = ['title', 'logo']


# 用户收藏序列化
class Moviecol(serializers.ModelSerializer):
    # 电影和用户是评论的外键
    movie = MovieModelSerializer()
    user = UserProfileModelSerializer()

    class Meta:
        model = models.Moviecol
        fields = ['id', 'movie', 'user']
