from app import db
from app.models import User, Tutor, Student, Group, Subject, AssociationTGS, Checkpoint, Progress
from .user_service import UserService
from app.exceptions import UserNotExist, AssociationExist, AssociationNotExist, CheckpointNotExist, CheckpointExist, CheckpointFieldNotExist

user_service = UserService()

class TutorService:
    def create_tutor(self, data):
        user = user_service.create_user(data['username'], data['password'])
        tutor = Tutor(lastname=data['lastname'],
                        firstname=data['firstname'],
                        patronymic=data['patronymic'],
                        rank=data['rank'], 
                        degree=data['degree'])
        tutor.account = user
        tutor.add_to_db()
        db.session.commit()
        return tutor
    
    def find_tutor_by_username(self, username):
        user = user_service.find_by_username(username)
        if user is None:
            raise UserNotExist(username)
        return user.tutor
    
    def find_tgs(self, tutor, subject_name, group_id):
        tgs = tutor.tgs.filter_by(subject_name=subject_name, group_id=group_id).first()
        if tgs is None:
            raise AssociationNotExist(subject_name=subject_name, group_id=group_id)
        return tgs

    def find_checkpoint_by_name(self, tgs, name):
        checkpoint = tgs.checkpoints.filter_by(name=name).first()
        if Checkpoint is None:
            raise CheckpointNotExist(name)
        return checkpoint 

    def get_associations(self, username):
        tutor = self.find_tutor_by_username(username)
        associations = tutor.tgs.all()
        return AssociationTGS.json_list(associations, ['id', 'tutor_id'])

    def add_association(self, username, subject_name, group_id):
        tutor = self.find_tutor_by_username(username)
        if tutor.tgs.filter_by(subject_name=subject_name, group_id=group_id).first():
            raise AssociationExist(subject_name=subject_name, group_id=group_id)
        subject = Subject.find_by_name(subject_name)
        if subject is None:
            subject = Subject(name=subject_name)
            subject.add_to_db()
        group = Group.find_by_id(group_id)
        if group is None: 
            group = Group(id=group_id)
            group.add_to_db()
        association = AssociationTGS()
        association.subject = subject
        association.group = group
        tutor.tgs.append(association)
        db.session.commit()

    def get_checkpoints(self, username, subject_name, group_id):
        tutor = self.find_tutor_by_username(username)
        tgs = self.find_tgs(tutor, subject_name, group_id)
        print(tgs)
        res = {}
        checkpoints = tgs.checkpoints.all()
        res['checkpoints'] = Checkpoint.json_list(checkpoints, ['id', 'tgs_id'])
        return res

    def add_checkpoints(self, username, subject_name, group_id, data):
        tutor = self.find_tutor_by_username(username)
        tgs = self.find_tgs(tutor, subject_name, group_id)
        group = tgs.group
        checkpoints = data['checkpoints']
        for cp_json in checkpoints:
            cp_name = cp_json['name']
            if tgs.checkpoints.filter_by(name=cp_name).first():
                raise CheckpointExist(cp_name)
            checkpoint = Checkpoint(tgs_id=tgs.id, **cp_json)
            db.session.add(checkpoint)
            for student in group.students:
                progress = Progress(checkpoint_id=checkpoint.id,
                                        student_id=student.user_id)
                student.progress.append(progress)
        db.session.commit()

    def update_group_progress(self, username, subject_name, group_id, data):
        tutor = self.find_tutor_by_username(username)
        tgs = self.find_tgs(tutor, subject_name, group_id)
        for cp_name in data:
            checkpoint = self.find_checkpoint_by_name(tgs, cp_name)
            for user_info in data[cp_name]:
                student = tgs.group.students.filter_by(user_id=user_info['user_id']).first()
                if student is None:
                    raise UserNotExist(user_info['user_id'])
                Progress.query.filter_by(checkpoint_id=checkpoint.id, student_id=student.user_id).update(user_info['progress'])
        """
        for user_info in data:
            for cp_name in user_info["progress"]:
                checkpoint = self.find_checkpoint_by_name(tgs, cp_name)
                student = tgs.group.students.filter_by(user_id=user_info['user_id']).first()
                if student is None:
                    raise UserNotExist(user_info['user_id'])
                Progress.query.filter_by(checkpoint_id=checkpoint.id, student_id=student.user_id).update(user_info['progress'][cp_name])
        """
        db.session.commit()

    def get_group_progress(self, username, subject_name, group_id):
        tutor = self.find_tutor_by_username(username)
        tgs = self.find_tgs(tutor, subject_name, group_id)
        group = tgs.group
        students = group.students.all()
        progress = Student.json_list(students)
        for i, student in enumerate(students):
            cp_progress = (db.session.query(Checkpoint.name,
                                Progress.mark, Progress.attempts,
                                Progress.checkpoint_date, Progress.deadline, Progress.plagiarism,)
                            .join(Progress)
                            .filter(Progress.student_id == student.user_id)
                            ).all()
            temp = { x[0]: {
                "mark": x[1],
                "attempts": x[2],
                "checkpoint_date": x[3].strftime("%Y-%m-%d") if x[3] is not None else x[3],
                "deadline": x[4].strftime("%Y-%m-%d") if x[4] is not None else x[4],
                "plagiarism": x[5]
            } for x in cp_progress}
            if progress[i].get('progress') is None:
                progress[i]['progress'] = temp
            else:
                progress[i]['progress'].update(temp)
        return progress
    
    def get_group_cp_progress(self, username, subject_name, group_id, cp_name):
        tutor = self.find_tutor_by_username(username)
        tgs = self.find_tgs(tutor, subject_name, group_id)
        group = tgs.group
        checkpoint = self.find_checkpoint_by_name(tgs, cp_name)
        students = group.students.all()
        progress = Student.json_list(students)
        for i, student in enumerate(students):
            cp_progress = (db.session.query(Checkpoint.name,
                                Progress.mark, Progress.attempts,
                                Progress.checkpoint_date, Progress.deadline, Progress.plagiarism,)
                            .join(Progress)
                            .filter(Checkpoint.id == checkpoint.id)
                            .filter(Progress.student_id == student.user_id)
                            ).first()
            print("progress", cp_progress)
            if cp_progress is not None:
                progress[i]['progress'] = {
                "mark": cp_progress[1],
                "attempts": cp_progress[2],
                "checkpoint_date": cp_progress[3].strftime("%Y-%m-%d") if cp_progress[3] is not None else cp_progress[3],
                "deadline": cp_progress[4].strftime("%Y-%m-%d") if cp_progress[4] is not None else cp_progress[4],
                "plagiarism": cp_progress[5]
                }
        return progress