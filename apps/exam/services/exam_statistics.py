from django.utils import timezone
from django.db.models.functions import ExtractWeek, ExtractMonth
from apps.exam.models import Exam
from apps.question.models import Question

class ExamStatisticsService:
    @staticmethod
    def get_exam_statistics():
        now = timezone.now()
        current_month = now.month
        current_week = now.isocalendar()[1]

        total_exams = Exam.objects.count()
        last_month = Exam.objects.filter(created_at__month=current_month).count()
        total_weeks = Exam.objects.filter(created_at__week=current_week).count()
        last_week = Exam.objects.filter(created_at__week=current_week - 1).count()
        applied_last_month = Exam.objects.filter(created_at__month=current_month, status="APPLIED").count()
        total_exams_applied = Exam.objects.filter(status="APPLIED").count()
        recent_exams = Exam.objects.filter(created_at__gte=now - timezone.timedelta(days=30)).order_by('-created_at')
        total_questions = Question.objects.count()
        total_questions_last_month = Question.objects.filter(created_at__month=current_month).count()
        total_exams_generated_by_ai = Exam.objects.filter(was_generated_by_ai=True).count()
        total_exams_generated_by_ai_last_month = Exam.objects.filter(created_at__month=current_month, was_generated_by_ai=True).count()

        return {
            "total_exams": total_exams,
            "last_month": last_month,
            "total_weeks": total_weeks,
            "last_week": last_week,
            "applied_last_month": applied_last_month,
            "total_exams_applied": total_exams_applied,
            "recent_exams": recent_exams,
            "total_questions": total_questions,
            "total_questions_last_month": total_questions_last_month,
            "total_exams_generated_by_ai": total_exams_generated_by_ai,
            "total_exams_generated_by_ai_last_month": total_exams_generated_by_ai_last_month
        }
