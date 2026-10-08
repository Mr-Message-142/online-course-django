from django.shortcuts import render, get_object_or_404

from .models import Course, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        "course_details_bootstrap.html",
        {
            "course": course
        }
    )


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    questions = course.questions.all()

    score = 0
    total_questions = questions.count()

    if request.method == "POST":

        for question in questions:

            selected_choice = request.POST.get(
                f"question_{question.id}"
            )

            if selected_choice:

                try:
                    choice_id = int(selected_choice)

                    correct = question.choices.filter(
                        id=choice_id,
                        is_correct=True
                    ).exists()

                    if correct:
                        score += 1

                except ValueError:
                    pass

        submission = Submission.objects.create(
            course=course,
            score=score,
            total_questions=total_questions
        )

        return render(
            request,
            "exam_result.html",
            {
                "course": course,
                "score": score,
                "total_questions": total_questions,
                "submission": submission
            }
        )

    return render(
        request,
        "mock_exam.html",
        {
            "course": course,
            "questions": questions
        }
    )


def show_exam_result(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    submission = Submission.objects.filter(
        course=course
    ).order_by("-submitted_at").first()

    return render(
        request,
        "exam_result.html",
        {
            "course": course,
            "submission": submission,
            "score": submission.score if submission else 0,
            "total_questions": (
                submission.total_questions
                if submission
                else course.questions.count()
            )
        }
    )