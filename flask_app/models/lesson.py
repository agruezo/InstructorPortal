from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Lesson:

    db_name = "solo_project"

    def __init__(self,data):
        self.id = data['id']
        self.lesson = data['lesson']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.topic_id=data['topic_id']

    @classmethod
    def get_all_lessons(cls):
        query = "SELECT * FROM lessons"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        return results

    @classmethod
    def get_all_topic_lessons(cls, data):
        query = "SELECT *, users.first_name AS instructor FROM lessons "\
        "LEFT JOIN users on users.id = lessons.user_id "\
        "WHERE topic_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def create_lesson(cls, data):
        query = "INSERT into lessons (lesson, user_id, topic_id) VALUES (%(lesson)s, %(user_id)s, %(topic_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    
    @classmethod
    def update_lesson(cls, data):
        query = "UPDATE lessons SET lesson = %(lesson)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    
    @classmethod
    def remove_lesson(cls, data):
        query = "DELETE FROM lessons WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @staticmethod
    def validate_lesson(lesson):
        is_valid = True
        if len(lesson['lesson']) < 1:
            is_valid = False
            flash("Lesson field can not be left blank","lesson")
        return is_valid