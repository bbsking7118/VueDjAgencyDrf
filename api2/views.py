from collections import OrderedDict

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.utils import obj_to_post, prev_next_post, obj_to_comment
from api2.serializer import CommentSerializer, PostListSerializer, CateTagSerializer, PostSerializerDetail
from blog.models import Post, Comment, Category, Tag


# class CommentCreateAPIView(CreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer


class CateTagAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()
        data = {
            'cateList': cateList,
            'tagList': tagList,
        }

        serializer = CateTagSerializer(instance=data)
        return Response(serializer.data)


class PostPageNumberPagination(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
        ]))


# class PostListAPIView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer
#     pagination_class = PostPageNumberPagination
#
#     def get_serializer_context(self):
#         return {
#             'request': None,
#             'format': self.format_kwarg,
#             'view': self
#         }
#
#
# class PostRetrieveAPIView(RetrieveAPIView):
#
#     def get_queryset(self):
#         return Post.objects.all().select_related('category').prefetch_related('tags', 'comment_set')
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         commentList = instance.comment_set.all()
#
#         postDict = obj_to_post(instance)
#         prevDict, nextDict = prev_next_post(instance)
#         commentDict = [obj_to_comment(c) for c in commentList]
#
#         dataDict = {
#             'post': postDict,
#             'prevPost': prevDict,
#             'nextPost': nextDict,
#             'commentList': commentDict,
#         }
#
#         return Response(dataDict)
#
#
# class PostLikeAPIView(GenericAPIView):
#     queryset = Post.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.like += 1
#         instance.save()
#         return Response(instance.like)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

    def get_serializer_context(self):
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }

    def get_queryset(self):
        return Post.objects.all().select_related('category').prefetch_related('tags', 'comment_set')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        commentList = instance.comment_set.all()

        postDict = obj_to_post(instance)
        prevDict, nextDict = prev_next_post(instance)
        commentDict = [obj_to_comment(c) for c in commentList]

        dataDict = {
            'post': postDict,
            'prevPost': prevDict,
            'nextPost': nextDict,
            'commentList': commentDict,
        }

        return Response(dataDict)

    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()
        return Response(instance.like)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
