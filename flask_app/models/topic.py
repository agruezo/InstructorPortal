import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Topic:

    db_name ="solo_project"

    def __init__(self,data):
        self.id = data['id']
        self.topic = data['title']
        self.subtopic = data['description']
        self.description = data['due_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.users_who_add = []

    @classmethod
    def get_all_topics(cls):
        query = "SELECT topics.id, topics.topic, users.first_name AS creator, topics.subtopic FROM topics "\
        "JOIN users ON users.id = topics.user_id "\
        "LEFT JOIN adds ON topics.id = adds.topic_id "\
        "GROUP BY topics.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        return results

    @classmethod
    def get_all_topic_adds(cls, data):
        topic_adds = []
        query = "SELECT topic_id FROM adds WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        for result in results:
            topic_adds.append(result['topic_id'])
        return topic_adds
    
    @classmethod
    def create_topic(cls, data):
        query = "INSERT into topics (topic, subtopic, description, user_id) VALUES (%(topic)s, %(subtopic)s, %(description)s, %(user_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def show_topic(cls, data):
        query = "SELECT *, topics.id AS topic_id, users.first_name AS creator FROM topics "\
        "JOIN users ON users.id = topics.user_id "\
        "WHERE topics.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print (results[0])
        
        return (results[0])

    @classmethod
    def show_topic_and_creator(cls, data):
        query = "SELECT *, users.first_name AS creator, topics.id AS topic FROM users "\
        "LEFT JOIN topics ON users.id = topics.user_id "\
        "WHERE topics.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @classmethod
    def update_topic(cls, data):
        query = "UPDATE topics SET topic = %(topic)s, subtopic = %(subtopic)s, description = %(description)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def destroy_topic(cls, data):
        query = "DELETE FROM topics WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def add_topic(cls, data):
        query = "INSERT INTO adds (user_id, topic_id) VALUES (%(user_id)s, %(topic_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def remove_topic(cls, data):
        query = "DELETE from adds WHERE user_id = %(user_id)s AND topic_id = %(topic_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @staticmethod
    def validate_topic(project):
        is_valid = True
        if len(project['topic']) < 1:
            is_valid = False
            flash("Topic field can not be left blank","topic")
        if len(project['subtopic']) < 1:
            is_valid = False
            flash("Subtopic field can not be left blank","topic")
        if len(project['description']) < 1:
            is_valid = False
            flash("Description field can not be left blank","topic")
        return is_valid