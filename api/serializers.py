from quiz.models import TestDetail
from rest_framework import serializers


class TestDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestDetail
        fields = ['id', 'username', 'score', 'start', 'total']
        # fields = '__all__'

    def validate_username(self, username):
        # Check if username is less than 2 characters
        if len(username) < 2:
            raise serializers.ValidationError('Username must be at least 2 characters')
        # Check if username exists
        if TestDetail.objects.filter(username__iexact=username).count():
            raise serializers.ValidationError(f'Username, {username} already taken')

        return username
