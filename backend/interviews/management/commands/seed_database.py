from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from interviews.models import Interviewer, Student, InterviewSession, Question
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seed the database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('🌱 Seeding database with sample data...'))

        # Create or get superuser
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('✅ Created admin user (username: admin, password: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('ℹ️  Admin user already exists'))

        # Create interviewers
        interviewer1, created = Interviewer.objects.get_or_create(
            email='john.interviewer@company.com',
            defaults={
                'name': 'John Smith',
                'user': user,
            }
        )
        self.stdout.write(f"{'✅ Created' if created else 'ℹ️  Found'} interviewer: {interviewer1.name}")

        interviewer2, created = Interviewer.objects.get_or_create(
            email='sarah.hr@company.com',
            defaults={
                'name': 'Sarah Johnson',
            }
        )
        self.stdout.write(f"{'✅ Created' if created else 'ℹ️  Found'} interviewer: {interviewer2.name}")

        # Create students
        students_data = [
            {'name': 'Alice Brown', 'email': 'alice.brown@student.com'},
            {'name': 'Bob Wilson', 'email': 'bob.wilson@student.com'},
            {'name': 'Carol Davis', 'email': 'carol.davis@student.com'},
            {'name': 'David Martinez', 'email': 'david.martinez@student.com'},
        ]

        students = []
        for student_data in students_data:
            student, created = Student.objects.get_or_create(
                email=student_data['email'],
                defaults={'name': student_data['name']}
            )
            students.append(student)
            self.stdout.write(f"{'✅ Created' if created else 'ℹ️  Found'} student: {student.name}")

        # Create interview sessions
        sessions_data = [
            {
                'title': 'Software Engineer - Full Stack',
                'interviewer': interviewer1,
                'student': students[0],
                'duration_minutes': 45,
                'status': 'scheduled',
                'description': 'Technical interview for full stack developer position',
            },
            {
                'title': 'Frontend Developer Interview',
                'interviewer': interviewer1,
                'student': students[1],
                'duration_minutes': 30,
                'status': 'scheduled',
                'description': 'React and TypeScript focused interview',
            },
            {
                'title': 'Python Developer Assessment',
                'interviewer': interviewer2,
                'student': students[2],
                'duration_minutes': 60,
                'status': 'scheduled',
                'description': 'Backend development with Python and Django',
            },
        ]

        sessions = []
        for i, session_data in enumerate(sessions_data):
            scheduled_time = timezone.now() + timedelta(days=i+1)
            session, created = InterviewSession.objects.get_or_create(
                title=session_data['title'],
                student=session_data['student'],
                defaults={
                    **session_data,
                    'scheduled_at': scheduled_time,
                }
            )
            sessions.append(session)
            self.stdout.write(f"{'✅ Created' if created else 'ℹ️  Found'} session: {session.title}")

        # Create questions for each session
        questions_sets = [
            # Full Stack Questions
            [
                {
                    'question_text': 'Tell me about yourself and your experience with full-stack development.',
                    'category': 'Introduction',
                    'difficulty': 'easy',
                    'order': 1,
                },
                {
                    'question_text': 'Explain the difference between SQL and NoSQL databases. When would you use each?',
                    'category': 'Technical',
                    'difficulty': 'medium',
                    'order': 2,
                },
                {
                    'question_text': 'Describe your experience with RESTful API design and implementation.',
                    'category': 'Technical',
                    'difficulty': 'medium',
                    'order': 3,
                },
                {
                    'question_text': 'How do you handle state management in a React application?',
                    'category': 'Technical',
                    'difficulty': 'medium',
                    'order': 4,
                },
                {
                    'question_text': 'Tell me about a challenging technical problem you solved recently.',
                    'category': 'Behavioral',
                    'difficulty': 'hard',
                    'order': 5,
                },
            ],
            # Frontend Questions
            [
                {
                    'question_text': 'What interests you about frontend development?',
                    'category': 'Introduction',
                    'difficulty': 'easy',
                    'order': 1,
                },
                {
                    'question_text': 'Explain the virtual DOM and how React uses it.',
                    'category': 'Technical',
                    'difficulty': 'medium',
                    'order': 2,
                },
                {
                    'question_text': 'How do you ensure your web applications are accessible?',
                    'category': 'Technical',
                    'difficulty': 'medium',
                    'order': 3,
                },
                {
                    'question_text': 'Describe your approach to responsive design.',
                    'category': 'Technical',
                    'difficulty': 'easy',
                    'order': 4,
                },
            ],
            # Python Questions
            [
                {
                    'question_text': 'What drew you to Python development?',
                    'category': 'Introduction',
                    'difficulty': 'easy',
                    'order': 1,
                },
                {
                    'question_text': 'Explain Python decorators and give an example of when you would use them.',
                    'category': 'Technical',
                    'difficulty': 'hard',
                    'order': 2,
                },
                {
                    'question_text': 'How do you handle database migrations in Django?',
                    'category': 'Technical',
                    'difficulty': 'medium',
                    'order': 3,
                },
                {
                    'question_text': 'Describe your experience with asynchronous programming in Python.',
                    'category': 'Technical',
                    'difficulty': 'hard',
                    'order': 4,
                },
                {
                    'question_text': 'How do you approach testing in Python applications?',
                    'category': 'Technical',
                    'difficulty': 'medium',
                    'order': 5,
                },
            ],
        ]

        for session, questions_data in zip(sessions, questions_sets):
            for question_data in questions_data:
                question, created = Question.objects.get_or_create(
                    session=session,
                    order=question_data['order'],
                    defaults={
                        **question_data,
                    }
                )
                if created:
                    self.stdout.write(f"  ✅ Added question {question.order} to {session.title}")

        self.stdout.write(self.style.SUCCESS('\n🎉 Database seeding completed!'))
        self.stdout.write(self.style.SUCCESS('\n📊 Summary:'))
        self.stdout.write(f"  - Interviewers: {Interviewer.objects.count()}")
        self.stdout.write(f"  - Students: {Student.objects.count()}")
        self.stdout.write(f"  - Sessions: {InterviewSession.objects.count()}")
        self.stdout.write(f"  - Questions: {Question.objects.count()}")
        self.stdout.write(self.style.SUCCESS('\n💡 You can now test the API with this sample data!'))
        self.stdout.write('   Admin panel: http://localhost:8000/admin/')
        self.stdout.write('   Username: admin')
        self.stdout.write('   Password: admin123')
