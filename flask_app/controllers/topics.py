from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models import topic
from flask_app.models import user

@app.route('/topics')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    data = {
        'user_id': session['user_id']
    }

    logged_in_user = user.User.get_by_id(user_data)
    topics = topic.Topic.get_all_topics()
    topic_adds = topic.Topic.get_all_topic_adds(data)

    return render_template('allTopics.html', logged_in_user = logged_in_user, topics = topics, topic_adds = topic_adds)

@app.route('/topics/new')
def new_topic():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }

    logged_in_user = user.User.get_by_id(data)
    return render_template('newTopic.html', logged_in_user = logged_in_user)

@app.route('/topics/create', methods = ['POST'])
def create_topic():
    if 'user_id' not in session:
        return redirect('/logout')
    if not topic.Topic.validate_topic(request.form):
        return redirect('/topics/new')
    data = {
        "topic": request.form["topic"],
        "subtopic": request.form["subtopic"],
        "description": request.form["description"],
        "user_id": request.form["creator"]
    }

    topic.Topic.create_topic(data)
    return redirect('/topics')

@app.route('/topics/<int:id>')
def show_topic(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    topic_data = {
        "user_id": session['user_id']
    }
    data = {
        "id": id
    }

    logged_in_user = user.User.get_by_id(user_data)
    current_topic = topic.Topic.show_topic(data)
    topic_adds = topic.Topic.get_all_topic_adds(topic_data)
    return render_template("showTopic.html", logged_in_user = logged_in_user, current_topic = current_topic, topic_adds = topic_adds)

@app.route('/topics/<int:id>/edit')
def edit_topic(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id'],
    }
    data = {
        "id": id
    }

    logged_in_user = user.User.get_by_id(user_data)
    current_topic = topic.Topic.show_topic(data)
    return render_template("editTopic.html", logged_in_user = logged_in_user, current_topic = current_topic)

@app.route('/topics/<int:id>/update', methods=['POST'])
def update_topic(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not topic.Topic.validate_topic(request.form):
        return redirect(f'/topics/{id}/edit')
    data = {
        "id": id,
        "topic": request.form["topic"],
        "subtopic": request.form["subtopic"],
        "description": request.form["description"]
    }

    topic.Topic.update_topic(data)
    return redirect('/topics')

@app.route('/topics/<int:id>/delete', methods=['POST'])
def delete_topic(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    
    topic.Topic.destroy_topic(data)
    return redirect('/topics')

@app.route('/topics/<int:id>/add')
def add_topic(id):
    data = {
        "user_id": session['user_id'],
        "topic_id": id
    }
    
    topic.Topic.add_topic(data)
    return redirect('/topics')

@app.route('/topics/<int:id>/remove')
def remove_topic(id):
    data = {
        "user_id": session['user_id'],
        "topic_id": id
    }

    topic.Topic.remove_topic(data)
    return redirect('/topics')

