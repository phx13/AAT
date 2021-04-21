from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, RadioField


class ReviewForm(FlaskForm):
    # reference https://stackoverflow.com/questions/14591202/how-to-make-a-radiofield-in-flask/14591681#14591681
    options = [
        (1, 'Strongly disagree'),
        (2, 'Disagree'),
        (3, 'Neither agree nor disagree'),
        (4, 'Agree'),
        (5, 'Strongly Agree')
    ]
    comment = TextAreaField('Additional comments (optional):')
    submit = SubmitField('Submit')


class AssessmentReviewForm(ReviewForm):
    # reference https://stackoverflow.com/questions/13404476/inherited-class-variable-modification-in-python/13404537#13404537
    statement1 = RadioField('I feel that I had sufficient knowledge to complete this assessment.',
                            choices=ReviewForm.options)
    statement2 = RadioField('I found this assessment difficult.', choices=ReviewForm.options)


class AATReviewForm(ReviewForm):
    statement1 = RadioField('I find it easy to navigate the AAT to find my tasks that need to be completed.',
                            choices=ReviewForm.options)
    statement2 = RadioField('I am pleased overall with the functionality of the AAT.', choices=ReviewForm.options)


class QuestionReviewForm(ReviewForm):
    statement1 = RadioField('I found this question difficult to answer.', choices=ReviewForm.options)
    statement2 = RadioField('I feel this question is relevant to the topic being assessed.', choices=ReviewForm.options)
