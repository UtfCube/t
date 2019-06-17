from flask_restful import Resource
from app.parsers import *
from app.services import tutor_service, student_service, user_service, token_service
from app.exceptions import BaseException, InternalError
from app.modules import AuthUser
from flask import request

class TutorRegistration(Resource):
    def post(self):
        data = tutor_info_parser.parse_args()
        try:
            tutor_service.create_tutor(data)
            access_token = token_service.create_access_token(identity=data['username'])
            refresh_token = token_service.create_refresh_token(identity=data['username'])
            return {
                'msg': 'Tutor {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class TutorHome(Resource):
    @AuthUser
    def post(self, current_user):
        data = association_parser.parse_args()
        try:
            tutor_service.add_association(current_user, **data)
            return {
                'msg': 'Association successfully created'
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

    @AuthUser
    def get(self, current_user):
        try:
            associations = tutor_service.get_associations(current_user)
            return associations
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class GroupCpProgress(Resource):
    @AuthUser
    def get(self, current_user, subject, group_id, cp_name):
        try:
            progress = tutor_service.get_group_cp_progress(current_user, subject, group_id, cp_name)
            return progress
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class Progress(Resource):
    @AuthUser
    def get(self, current_user, subject, group_id):
        try:
            progress = tutor_service.get_group_progress(current_user, subject, group_id)
            return progress
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()
    
    @AuthUser
    def post(self, current_user, subject, group_id):
        data = request.get_json()
        try:
            tutor_service.update_group_progress(current_user, subject, group_id, data)
            return {
                'msg': 'Table succesfully updated'
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class Checkpoints(Resource):
    @AuthUser
    def get(self, current_user, subject, group_id):
        try:
            checkpoints = tutor_service.get_checkpoints(current_user, subject, group_id)
            print(checkpoints)
            return checkpoints
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

    @AuthUser
    def post(self, current_user, subject, group_id):
        #TODO допилить парсер
        data = request.get_json()
        try:
            tutor_service.add_checkpoints(current_user, subject, group_id, data)
            return {
                'msg': 'Checkpoints succesfully created'
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class StudentRegistration(Resource):
    def post(self):
        data = student_info_parser.parse_args()
        try:
            student_service.create_student(data)
            access_token = token_service.create_access_token(identity=data['username'])
            refresh_token = token_service.create_refresh_token(identity=data['username'])
            return {
                'msg': 'Student {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class StudentHome(Resource):
    @AuthUser
    def get(self, current_user):
        try:
            subjects = student_service.get_subjects(current_user)
            return subjects
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()

class SubjectProgress(Resource):
    @AuthUser
    def get(self, current_user, subject):
        try:
            progress = student_service.get_subject_progress(current_user, subject)
            return progress
        except BaseException as e:
            return e.to_json()
        except Exception as e:
            print(e)
            return InternalError().to_json()