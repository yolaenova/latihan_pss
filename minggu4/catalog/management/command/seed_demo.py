from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from catalog.models import Assignment, Course, Enrollment, Lesson, Submission
from users.models import User


class Command(BaseCommand):
    help = "Membuat sample data Course, Lesson, Assignment, dan Submission secara idempotent"

    def handle(self, *args, **options):
        # 1. User: Dosen dan Mahasiswa
        lecturer, _ = User.objects.get_or_create(
            username="suprayogi",
            defaults={
                "email": "suprayogi@gmail.com",
                "role": User.Role.LECTURER,
            },
        )
        if _:
            lecturer.set_password("12345")
            lecturer.save()

        student, _ = User.objects.get_or_create(
            username="fauzan",
            defaults={
                "email": "fauzan@gmail.com",
                "role": User.Role.STUDENT,
            },
        )
        if _:
            student.set_password("12345")
            student.save()

        # 2. Course
        course, _ = Course.objects.get_or_create(
            code="PSS01",
            defaults={
                "title": "Pemrograman Sisi Server",
                "description": "Belajar backend development dengan Django dan Docker.",
                "lecturer": lecturer,
            },
        )

        # 3. Lesson
        lessons = [
            "Pengenalan Backend",
            "Pola Arsitektur Backend",
            "Containerisasi dengan Docker",
        ]
        for order, title in enumerate(lessons, start=1):
            Lesson.objects.get_or_create(
                course=course,
                order=order,
                defaults={"title": title, "content": f"Materi {title}"},
            )

        # 4. Enrollment
        Enrollment.objects.get_or_create(
            student=student,
            course=course,
        )

        # 5. Assignment
        assignment1, _ = Assignment.objects.get_or_create(
            course=course,
            title="Tugas Django ORM",
            defaults={
                "description": "Implementasikan model dan relationship menggunakan Django ORM.",
                "deadline": timezone.now() + timedelta(days=7),
            },
        )
        assignment2, _ = Assignment.objects.get_or_create(
            course=course,
            title="Tugas REST API",
            defaults={
                "description": "Buat REST API sederhana menggunakan Django.",
                "deadline": timezone.now() + timedelta(days=14),
            },
        )

        # 6. Submission
        Submission.objects.get_or_create(
            assignment=assignment1,
            student=student,
            defaults={
                "content": "Saya telah menyelesaikan implementasi Django ORM.",
                "grade": 87.50,
            },
        )
        Submission.objects.get_or_create(
            assignment=assignment2,
            student=student,
            defaults={
                "content": "Saya telah menyelesaikan REST API menggunakan Django.",
                "grade": 90.00,
            },
        )

        self.stdout.write(self.style.SUCCESS("Sample data berhasil dibuat/diperbarui tanpa duplikasi."))