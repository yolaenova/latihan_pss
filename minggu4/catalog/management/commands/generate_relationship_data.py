from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from users.models import User
from catalog.models import Course, Enrollment, Lesson, Assignment, Submission


class Command(BaseCommand):
    help = "Membuat dataset relasi LMS untuk pengujian performa"

    def handle(self, *args, **options):
        assignment_fields = {field.name: field for field in Assignment._meta.fields}
        submission_fields = {field.name: field for field in Submission._meta.fields}

        courses = list(Course.objects.filter(code__startswith="PERF").order_by("code")[:100])
        if len(courses) < 100:
            raise CommandError("Diperlukan minimal 100 Course PERF. Jalankan generate_performance_data dahulu.")

        lecturers = []
        students = []
        with transaction.atomic():
            for i in range(1, 6):
                user, created = User.objects.get_or_create(
                    username=f"perf_lecturer_{i:02d}",
                    defaults={"role": "LECTURER", "is_active": True},
                )
                if created:
                    user.set_unusable_password()
                    user.save(update_fields=["password"])
                lecturers.append(user)

            for i in range(1, 51):
                user, created = User.objects.get_or_create(
                    username=f"perf_student_{i:03d}",
                    defaults={"role": "STUDENT", "is_active": True},
                )
                if created:
                    user.set_unusable_password()
                    user.save(update_fields=["password"])
                students.append(user)

            # Enrollment
            existing_enrollments = set(
                Enrollment.objects.filter(course__in=courses).values_list("course_id", "student_id")
            )
            enrollment_rows = []
            for index, course in enumerate(courses):
                for offset in range(10):
                    student = students[(index * 10 + offset) % len(students)]
                    key = (course.id, student.id)
                    if key not in existing_enrollments:
                        enrollment_rows.append(Enrollment(course=course, student=student))
            Enrollment.objects.bulk_create(enrollment_rows, batch_size=500)

            # Lesson
            existing_lessons = set(
                Lesson.objects.filter(course__in=courses).values_list("course_id", "order")
            )
            lesson_rows = []
            for course in courses:
                for order in range(1, 6):
                    key = (course.id, order)
                    if key not in existing_lessons:
                        lesson_rows.append(
                            Lesson(
                                course=course,
                                title=f"Materi {order}",
                                content=f"Materi simulasi {order} untuk {course.code}",
                                order=order,
                            )
                        )
            Lesson.objects.bulk_create(lesson_rows, batch_size=500)

            # Assignment
            existing_assignments = set(
                Assignment.objects.filter(course__in=courses).values_list("course_id", "title")
            )
            assignment_rows = []
            deadline_val = timezone.now() + timedelta(days=14)
            for course in courses:
                for number in range(1, 3):
                    title = f"PERF Tugas {number}"
                    key = (course.id, title)
                    if key in existing_assignments:
                        continue
                    values = {"course": course, "title": title, "deadline": deadline_val}
                    if "description" in assignment_fields:
                        values["description"] = f"Tugas simulasi untuk {course.code}"
                    assignment_rows.append(Assignment(**values))
            Assignment.objects.bulk_create(assignment_rows, batch_size=500)

            # Submission
            assignments = list(
                Assignment.objects.filter(course__in=courses, title__in=["PERF Tugas 1", "PERF Tugas 2"]).select_related("course")
            )
            enrollment_map = {}
            for c_id, s_id in Enrollment.objects.filter(course__in=courses, student__in=students).values_list("course_id", "student_id"):
                enrollment_map.setdefault(c_id, []).append(s_id)

            existing_submissions = set(
                Submission.objects.filter(assignment__in=assignments).values_list("assignment_id", "student_id")
            )
            submission_rows = []
            for assignment in assignments:
                for student_id in sorted(enrollment_map.get(assignment.course_id, []))[:5]:
                    key = (assignment.id, student_id)
                    if key not in existing_submissions:
                        values = {"assignment": assignment, "student_id": student_id}
                        if "content" in submission_fields:
                            values["content"] = "Jawaban simulasi pengujian performa."
                        submission_rows.append(Submission(**values))
            Submission.objects.bulk_create(submission_rows, batch_size=500)

        self.stdout.write(self.style.SUCCESS("Dataset relasi LMS berhasil dibuat!"))