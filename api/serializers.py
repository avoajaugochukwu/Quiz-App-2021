from quiz.models import Choice, Question, Quiz, QuizAnswer
from rest_framework import serializers
from quiz.models import Question, Choice
from rest_framework.validators import UniqueValidator


class QuizSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(
                queryset=Quiz.objects.all(), 
                message="This username has been taken. Please enter another username"
            )
        ]
    )
    class Meta:
        model = Quiz
        fields = ['id', 'username', 'score', 'start', 'total']

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


class QuizAnswerSerializer(serializers.ModelSerializer):
    # username = serializers.SerializerMethodField()
    question = serializers.SerializerMethodField()
    selected_answer = serializers.SerializerMethodField()
    choice = serializers.SerializerMethodField()
    is_correct = serializers.SerializerMethodField()
    

    class Meta:
        model = QuizAnswer
        fields = ('question', 'selected_answer', 'is_correct', 'choice')

    def get_question(self, obj):
        return obj.question.text 
    
    def get_selected_answer(self, obj):
        return obj.choice.text

    def get_is_correct(self, obj):
        choices = Choice.objects.filter(question=obj.question.id)
        for choice in choices:
            if choice.id == obj.choice.id:
                return choice.answer
        return None

    def get_choice(self, obj):
        choices = Choice.objects.filter(question=obj.question.id)
        serializer = ChoiceSerializer(choices, many=True)
        return serializer.data


class QuizDetailSerialize(serializers.ModelSerializer):
    quiz_answer = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        # remove id, if unnecessary
        fields = ['id', 'username', 'score', 'total', 'quiz_answer']

    def get_quiz_answer(self, obj):
        quiz_answers = QuizAnswer.objects.filter(quiz_id=obj.id)
        serializer = QuizAnswerSerializer(quiz_answers, many=True)
        return serializer.data