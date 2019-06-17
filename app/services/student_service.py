from app.models import User, Tutor, Student, Group, Subject, AssociationTGS, Checkpoint, Progress
from .user_service import UserService
from app import db
from app.exceptions import UserNotExist, AssociationNotExist

user_service = UserService()

class StudentService:
    def create_student(self, data):
        user = user_service.create_user(data['username'], data['password'])
        group = Group.find_by_id(data['group_id'])
        if group is None:
            group = Group(id=data['group_id'])
            group.add_to_db()
        student = Student(lastname=data['lastname'],
                            firstname=data['firstname'],
                            patronymic=data['patronymic'],
                            rank=data['rank'], 
                            admission_year=data['admission_year'], 
                            group_id=group.id)
        student.account = user
        student.add_to_db()
        db.session.commit()
        return student

    def find_student_by_username(self, username):
        user = user_service.find_by_username(username)
        if user is None:
            raise UserNotExist(username)
        return user.student

    def get_subjects(self, username):
        student = self.find_student_by_username(username)
        group = student.group
        tgs = group.tgs.distinct(AssociationTGS.tutor_id).all()
        tmp = { el.tutor_id: [] for el in tgs }
        tutors = [Tutor.json(Tutor.query.get(el.tutor_id), ['user_id']) for el in tgs]
        pairs = group.tgs.with_entities(AssociationTGS.tutor_id, AssociationTGS.subject_name).all()
        for pair in pairs:
            tmp[pair[0]].append(pair[1])
        index = 0
        for key in tmp:
            tutors[index]["subjects"] = tmp[key]
            index += 1
        return tutors

    def get_subject_progress(self, username, subject_name):
        return ""
        """
        student = self.find_student_by_username(username)
        tgs = AssociationTGS.query.filter_by(subject_name=subject_name, group_id=student.group_id).first()
        if tgs is None:
            raise AssociationNotExist(subject_name=subject_name)
        checkpoints = tgs.checkpoints.all()
        progress = Checkpoint.json_list(checkpoints, ['id', 'tgs_id'])
        for i, checkpoint in enumerate(checkpoints):
            cp_progress = (db.session.query(CheckpointField.name,
                                Progress.passed)
                            .join(Progress)
                            .filter(CheckpointField.checkpoint_id == checkpoint.id)
                            .filter(Progress.student_id == student.user_id)
                            ).all()
            progress[i]["progress"] = dict(cp_progress)
        """
        return progress
            