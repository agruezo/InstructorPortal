from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models import topic, user, lesson

@app.route('/topics/<int:id>/lessons')
def new_lesson(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    topic_id = {
        'id': id
    }

    logged_in_user = user.User.get_by_id(data)
    current_topic = topic.Topic.show_topic_and_creator(topic_id)
    current_lessons = lesson.Lesson.get_all_topic_lessons(topic_id)

    return render_template('topicLesson.html', logged_in_user=logged_in_user, current_topic=current_topic, current_lessons=current_lessons)

@app.route('/topics/<int:id>/lessons/create', methods = ['POST'])
def create_lesson(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not lesson.Lesson.validate_lesson(request.form):
        return redirect(f'/topics/{id}/lessons')
    data = {
        "lesson": request.form["lesson"],
        "user_id": request.form["author"],
        "topic_id": request.form["topic_lesson"]
    }
    lesson.Lesson.create_lesson(data)
    return redirect(f'/topics/{id}/lessons')

@app.route('/topics/<int:id>/lessons/<int:id2>/delete', methods = ['POST'])
def remove_lesson(id, id2):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id2
    }

    lesson.Lesson.remove_lesson(data)
    return redirect(f'/topics/{id}/lessons')