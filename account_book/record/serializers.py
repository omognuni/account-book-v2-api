from rest_framework import serializers

from core.models import Record


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record
        fields = ['id', 'category', 'amount']
        read_only_fields = ['id']


class RecordDetailSerializer(RecordSerializer):
    '''내역 상세 보기에서 memo 및 생성 날짜 확인'''
    class Meta(RecordSerializer.Meta):
        fields = RecordSerializer.Meta.fields + \
            ['memo', 'created_at', 'updated_at']
        read_only_fields = RecordSerializer.Meta.read_only_fields + \
            ['created_at', 'updated_at']
