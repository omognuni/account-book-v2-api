from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

from drf_spectacular.utils import extend_schema

from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from core.models import Record

from record.serializers import RecordSerializer, RecordDetailSerializer
from record import shortener


@extend_schema(description='캐시에 있는 공유 url을 가져와서 리디렉션', methods=['GET'])
@api_view(['GET'])
def redirect_url(request, new_url):
    '''단축 url 리디렉션'''
    pk = cache.get(new_url)
    url = reverse('record:record-detail', args=[pk])
    if url:
        return HttpResponseRedirect(redirect_to=url)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Record']
)
class RecordViewSet(viewsets.ModelViewSet):
    '''Record View'''
    serializer_class = RecordDetailSerializer
    queryset = Record.objects.all()

    def get_queryset(self):
        '''요청한 유저의 가 생성한 내역만 필터'''
        queryset = self.queryset.filter(
            user=self.request.user)

        return queryset

    def get_serializer_class(self):
        '''list 일때는 amount만 보여주기'''
        if self.action == 'list':
            return RecordSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        '''가계부 내역 생성 시 user_id 저장'''
        serializer.save(user=self.request.user)

    @extend_schema(description='record 세부 내역 복제', methods=['POST'])
    @action(methods=['POST'], detail=True, url_path='copy-detail')
    def copy_detail(self, request, pk=None):
        '''세부 내역 복제'''
        record = self.queryset.get(id=pk)
        if record:
            record.pk = None
            record.user = self.request.user
            record.save()
            serializer = self.get_serializer(record)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(description='record id로 세부 내역 공유 단축 url 생성', methods=['POST'])
    @action(methods=['POST'], detail=True, url_path='share-url')
    def share_url(self, request, pk=None):
        '''세부 내역 공유'''
        short_url = shortener.encode()
        key = f'record{pk}'
        if cache.get(key):
            new_url = settings.SITE_URL + '/' + str(cache.get(key))
            return Response(data=new_url, status=status.HTTP_200_OK)
        else:
            cache.set(short_url, pk, 600)
            cache.set(key, short_url, 600)
            new_url = settings.SITE_URL + '/' + str(short_url)
            return Response(data=new_url, status=status.HTTP_201_CREATED)
