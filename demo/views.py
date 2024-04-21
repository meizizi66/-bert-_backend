from asgiref.sync import sync_to_async
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import WeiboNote
from .models import WeiboNoteComment
from .serializers import WeiboNoteSerializer,KeyWordCrawlSerializer,BlogCrawlSerializer
from .serializers import WeiboNoteCommentSerializer
from .serializers import CommentFilterSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
import re
from collections import Counter
import jieba
from .TextAnalyzer import TextAnalyzer
from rest_framework.decorators import api_view
from typing import List

import asyncio
from demo.crawl_def import crawl_search, crawl_specified


class WeiboNoteListCreate(generics.ListCreateAPIView):
    queryset = WeiboNote.objects.all()
    serializer_class = WeiboNoteSerializer

class WeiboNoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = WeiboNote.objects.all()
    serializer_class = WeiboNoteSerializer

class WeiboNoteCommentListCreate(generics.ListCreateAPIView):
    queryset = WeiboNoteComment.objects.all()
    serializer_class = WeiboNoteCommentSerializer

class WeiboNoteCommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = WeiboNoteComment.objects.all()
    serializer_class = WeiboNoteCommentSerializer

class WeiboNoteCommentFilterView(ListAPIView):
    queryset = WeiboNoteComment.objects.all()
    serializer_class = WeiboNoteCommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user_id']  # 指定要搜索的字段

class WeiboNoteFilterView(ListAPIView):
    queryset = WeiboNote.objects.all()
    serializer_class = WeiboNoteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user_id']  # 指定要搜索的字段

class CommentFilterView(generics.ListAPIView):
    queryset = WeiboNoteComment.objects.all()
    serializer_class = CommentFilterSerializer

class CommentWordFrequencyView(APIView):
    def get(self, request):
        # 获取所有文本数据并进行预处理
        all_text = WeiboNoteComment.objects.values_list('content', flat=True)
        cleaned_text = [re.sub(r'<[^>]+>', '', text) for text in all_text]
        print(cleaned_text)
        print(type(cleaned_text))

        # 加载停用词表
        stopwords = set()
        with open("utils/baidu_stopwords.txt", "r", encoding="utf-8") as f:
            for line in f:
                stopwords.add(line.strip())

        # 合并文本数据为一个字符串
        combined_text = ' '.join(cleaned_text)
        # 定义正则表达式模式，匹配空格和中文标点符号
        pattern = re.compile("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-]+")

        # 使用正则表达式去除空格和标点符号
        combined_text = pattern.sub("", combined_text)

        # 使用jieba进行分词
        words = jieba.cut(combined_text, cut_all=False)

        # 将分词结果转换为列表，并去除停用词
        seg_list = [word for word in words if word not in stopwords]

        # 统计词频
        word_counts = Counter(seg_list)

        # 对词频进行排序
        sorted_word_counts = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True))

        return Response(sorted_word_counts)

class IpStaticsView(APIView):
    def get(self, request):
        # 获取所有文本数据并进行预处理
        blog_ip = WeiboNote.objects.values_list('ip_location', flat=True)
        comment_ip = WeiboNoteComment.objects.values_list('ip_location', flat=True)
        ips = blog_ip.union(comment_ip, all=True)
        # 创建一个空集合
        ips_set = list()
        print(type(ips))
        for obj in ips:
            ips_set.append(obj)
        # 使用 Counter 统计重复元素
        counter = Counter(ips_set)

        # 使用列表推导式将统计结果转换为元组列表，并排序
        sorted_count = dict(sorted(counter.items(), key=lambda x: x[1],reverse=True))
        # blog_str = ' '.join(str(obj) for obj in blog_ip)
        # comment_str = ' '.join(str(obj) for obj in comment_ip)
        # ips_str = blog_str+' '+comment_str
        # print(ips_str)

        return Response(sorted_count)

class CommentAnalysisView(APIView):
    def get(self, request):
        # 获取所有文本数据并进行预处理
        all_text = WeiboNoteComment.objects.values_list('content', flat=True)
        cleaned_text = [re.sub(r'<[^>]+>', '', text) for text in all_text]
        analyzer = TextAnalyzer()
        # 初始化结果列表
        predicted_emotions = []
        # 对每条文本进行推理
        for text in cleaned_text:
            predicted_class = analyzer.analyze_text(text)
            emotion_mapping = {'neutral': '平和', 'happy': '开心', 'angry': '生气', 'sad': '悲伤', 'fear': '恐惧', 'surprise': '惊讶'}
            predicted_emotion = emotion_mapping[predicted_class]
            # 添加到结果列表中
            predicted_emotions.append(predicted_emotion)
        # 使用 Counter 统计重复元素
        counter = Counter(predicted_emotions)

        # 使用列表推导式将统计结果转换为元组列表，并排序
        sorted_emotion = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))

        return Response(sorted_emotion)


@api_view(['POST'])
def keyword_crawl_view(request):
    if request.method == 'POST':
        # 序列化表单数据
        serializer = KeyWordCrawlSerializer(data=request.data)
        # 验证数据
        if serializer.is_valid():
            # 如果数据有效，将其保存到数据库
            # 如果提交的数据是 JSON 格式
            if isinstance(serializer.validated_data, dict):
                # 获取指定key的value值
                count = serializer.validated_data.get('count', None)
                keywords = serializer.validated_data.get('keyword', None)
                is_enable_comments = serializer.validated_data.get('isCrawlComment', None)

                if count is not None and keywords is not None and is_enable_comments is not None:
                    # 进行你的操作，例如打印指定key的value值
                    serializer.save()
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(crawl_search1(count,keywords,is_enable_comments))
                    loop.close()
                    return Response({"message": result,"code":1}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "数据不能为空","code":0}, status=status.HTTP_200_OK)
        else:
            # 如果数据无效，返回验证错误信息
            error_data = {'code':400 , 'message':serializer.errors}
            return Response(error_data)

@api_view(['POST'])
def blog_crawl_view(request):
    if request.method == 'POST':
        # 序列化表单数据
        serializer = BlogCrawlSerializer(data=request.data)
        # 验证数据
        if serializer.is_valid():
            # 如果数据有效，将其保存到数据库
            # 如果提交的数据是 JSON 格式
            if isinstance(serializer.validated_data, dict):
                # 获取指定key的value值
                note_list = serializer.validated_data.get('note_id', None)
                print(serializer.validated_data)
                if note_list is not None:
                    # 进行你的操作，例如打印指定key的value值
                    serializer.save()
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(crawl_specify1(note_list))
                    loop.close()
                    return Response({"message": result, "code": 1}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "数据不能为空", "code": 0}, status=status.HTTP_200_OK)
        else:
            # 如果数据无效，返回验证错误信息
            error_data = {'code': 400, 'message': serializer.errors}
            return Response(error_data)

async def crawl_search1(count:int,keywords:str,is_enable_comments:bool):
    try:
        await crawl_search(count, keywords, is_enable_comments)
        return f"{count}, {keywords},{is_enable_comments}!"
    except Exception as e:
        return Response({"message": "爬虫失败，请稍后再试", "code": 0}, status=status.HTTP_200_OK)

async def crawl_specify1(note_id:List[str]):
    try:
        await crawl_specified(note_id, True)
        return f"{note_id}!"
    except Exception as e:
        return Response({"message": "爬虫失败，请稍后再试", "code": 0}, status=status.HTTP_200_OK)

class CrawlSearchView(APIView):
    # async def get(self, request):
    #     # 在异步视图中调用异步任务
    #     result = await crawl_search1()
    #     return Response({"message": result}, status=status.HTTP_200_OK)

    # 使用 run_until_complete 来运行异步任务
    def get(self, request):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(crawl_search1())
        loop.close()
        return Response({"message": result}, status=status.HTTP_200_OK)
