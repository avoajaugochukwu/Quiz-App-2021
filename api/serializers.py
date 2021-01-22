from quiz.models import Choice, Question, Quiz, QuizAnswer
from rest_framework import serializers


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'username', 'score', 'start', 'total']
        # fields = '__all__'

    # custom serialize methods must start with validate
    def validate_username(self, username):
        # Check if username is less than 2 characters
        if len(username) < 2:
            raise serializers.ValidationError('Username must be at least 2 characters')
        # Check if username exists
        if Quiz.objects.filter(username__iexact=username).count():
            raise serializers.ValidationError(f'Username, {username} already taken')

        return username


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'question', 'text', 'answer')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text')


class QuestionChoiceSerializer(serializers.ModelSerializer):
    choice_question = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'text', 'choice_question']
        # fields = '__all__'


class QuizDictSerializer(serializers.Serializer):
    quiz_dict_response = serializers.DictField()

    class Meta:
        fields = ['quiz_response']


class ResultDetailSerializer(serializers.Serializer):
    # choice = QuestionChoiceSerializer()
    # quiz = QuizSerializer()
    question = QuestionSerializer()

    class Meta:
        fields = ['question']