from flask_restful import reqparse

CANNOT_BE_BLANK='This field cannot be blank'

tutor_info_parser = reqparse.RequestParser()
tutor_info_parser.add_argument('username', help=CANNOT_BE_BLANK, required=True)
tutor_info_parser.add_argument('password', help=CANNOT_BE_BLANK, required=True)
tutor_info_parser.add_argument('firstname', help=CANNOT_BE_BLANK, required=True)
tutor_info_parser.add_argument('lastname', help=CANNOT_BE_BLANK, required=True)
tutor_info_parser.add_argument('patronymic', help=CANNOT_BE_BLANK, required=True)
tutor_info_parser.add_argument('rank', help=CANNOT_BE_BLANK, required=True)
tutor_info_parser.add_argument('degree', default=None, store_missing=True, nullable=True)

student_info_parser = reqparse.RequestParser()
student_info_parser.add_argument('username', help=CANNOT_BE_BLANK, required=True)
student_info_parser.add_argument('password', help=CANNOT_BE_BLANK, required=True)
student_info_parser.add_argument('firstname', help=CANNOT_BE_BLANK, required=True)
student_info_parser.add_argument('lastname', help=CANNOT_BE_BLANK, required=True)
student_info_parser.add_argument('patronymic', help=CANNOT_BE_BLANK, required=True)
student_info_parser.add_argument('rank', help=CANNOT_BE_BLANK, required=True)
student_info_parser.add_argument('admission_year', type=int, required=True)
student_info_parser.add_argument('group_id', type=int, required=True)

user_login_parser = reqparse.RequestParser()
user_login_parser.add_argument('username', help=CANNOT_BE_BLANK, required=True)
user_login_parser.add_argument('password', help=CANNOT_BE_BLANK, required=True)

association_parser = reqparse.RequestParser()
association_parser.add_argument('subject_name', help=CANNOT_BE_BLANK, required=True)
association_parser.add_argument('group_id', type=int, required=True)
