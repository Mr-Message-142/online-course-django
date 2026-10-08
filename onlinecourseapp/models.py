from django.db import models


class Instructor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Learner(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    text = models.TextField()

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Submission(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.name} - {self.score}/{self.total_questions}"