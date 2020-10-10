from rest_framework import serializers
from login.models import User, Subject
from quiz.models import Quiz, Question, UserAnswer, Answer, UserQuiz

class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["title", "description", "total_marks", "publish_date","timestamp", "pk", "end_date"]
    

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"



class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = "__all__"

 
class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = "__all__"


class MyQuizListSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        #fields = ["id", "title", "discription","completed","score"]
        fields = "__all__"

    def get_completed(self, obj):
        try:
            print(obj)
            userquiz = UserQuiz.objects.get(user=self.context['request'].user, quiz=obj)
            return userquiz.completed
        except UserQuiz.DoesNotExist:
            print(obj)
            return None

    def get_questions_count(self, obj):
        return obj.question_set.all().count()


    def get_score(self, obj):
        try:
            userquiz = UserQuiz.objects.get(user=self.context['request'].user, quiz=obj)
            if userquiz.completed == True:
                return userquiz.score
                return None
        except UserQuiz.DoesNotExist:
                return None

class UserAnswerQuestionSerializer(serializers.ModelSerializer):
    answer_title = serializers.SerializerMethodField()
    question_title = serializers.SerializerMethodField()
    answer_is_true = serializers.SerializerMethodField()

    class Meta:
        model = UserAnswer
        fields = ("answer_title", "question_title", "answer_is_true")
    
    def get_answer_title(self, obj):
        try:
            print(obj.answer.id)
            answer = Answer.objects.get(id=obj.answer.id)
            return answer.content
        except:
            return None
    
    def get_question_title(self, obj):
        try:
            question = Question.objects.get(id=obj.question.id)
            return question.content
        except:
            return None
    
    def get_answer_is_true(self, obj):
        try:
            print(obj.answer.id)
            answer = Answer.objects.get(id=obj.answer.id)
            return answer.is_correct
        except:
            return None

class UserQuizSerializer(serializers.ModelSerializer):
    useranswer_set = UserAnswerQuestionSerializer(many=True)

    class Meta:
        model = UserQuiz
        fields = "__all__"


class QuizResultSerializer(serializers.ModelSerializer):
	userquiz_set = serializers.SerializerMethodField()

	class Meta:
		model = Quiz
		fields = "__all__"

	def get_userquiz_set(self, obj):
		try:
			userquiz = UserQuiz.objects.get(user=self.context['request'].user, quiz=obj)
			serializer = UserQuizSerializer(userquiz)
			return serializer.data

		except UserQuiz.DoesNotExist:
			return None


class QuizDetailSerializer(serializers.ModelSerializer):
    userquiz_set = serializers.SerializerMethodField()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = "__all__"
    
    def get_userquiz_set(self, obj):
        try:
            userquiz = UserQuiz.objects.filter(user=self.context['request'].user, quiz=obj)
            serializer = UserQuizSerializer(userquiz)
            return serializer.data
        except:
            return False


class UserSubmitAnswerSerializer(serializers.ModelSerializer):
    useranswer_set = UserAnswerQuestionSerializer(many=True) 
    quiz_title = serializers.SerializerMethodField()

    class Meta:
        model = UserQuiz
        #fields = ("quiz_title", "score", "completed", "useranswer_set")
        fields = "__all__"

    def get_quiz_title(self, obj):
        try:
            quiz = Quiz.objects.get(id=obj.quiz.id)
            return quiz.title
        except:
            return None

