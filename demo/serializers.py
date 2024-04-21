from rest_framework import serializers
from .models import WeiboNote
from .models import WeiboNoteComment
import re

class WeiboNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeiboNote
        fields = '__all__'

class WeiboNoteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeiboNoteComment
        fields = '__all__'

class CommentFilterSerializer(serializers.ModelSerializer):
    processed_data = serializers.SerializerMethodField()

    def get_processed_data(self, obj):
        # 在这里编写对特殊列进行处理的逻辑
        # 例如，去除英文和特殊字符
        # 这里使用正则表达式去除英文和特殊字符
        processed_text = re.sub(r'<[^>]+>', '', obj.content)
        return processed_text

    class Meta:
        model = WeiboNoteComment
        fields = ('id', 'content', 'processed_data')

from .models import KeyWordCrawl,BlogCrawl


class KeyWordCrawlSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWordCrawl
        fields = ['keyword', 'count', 'isCrawlComment', 'status']

    def validate_keyword(self, value):
        # 检查关键词是否为空
        if not value:
            raise serializers.ValidationError("关键词不能为空")
        return value

class BlogCrawlSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCrawl
        fields = ['note_id', 'status']

    def validate_note_id(self, value):
        # 检查关键词是否为空
        if not value:
            raise serializers.ValidationError("note_id不能为空")
        return value
