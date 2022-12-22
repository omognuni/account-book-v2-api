from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from core.models import Record

from record.serializers import RecordSerializer, RecordDetailSerializer
from record import shortener


@api_view(['GET'])
def redirect_url(request, new_url):
    '''단축 url 리디렉션'''
    url = cache.get(new_url)

    if url:
        return HttpResponseRedirect(redirect_to=url)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RecordViewSet(viewsets.ModelViewSet):
    '''Record View'''
    serializer_class = RecordDetailSerializer
    queryset = Record.objects.all()

    def get_queryset(self):
        '''요청한 유저의 삭제되지 않은 내역만 필터'''
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

    @action(methods=['POST'], detail=True, url_path='share-url')
    def share_url(self, request, pk=None):
        '''세부 내역 공유'''
        url = reverse('record:record-detail', args=[pk])
        short_url = shortener.encode(int(pk))
        new_url = settings.SITE_URL + '/' + str(short_url)
        if not cache.has_key(short_url):
            cache.set(short_url, url, 3600)

        return Response(data=new_url, status=status.HTTP_201_CREATED)
