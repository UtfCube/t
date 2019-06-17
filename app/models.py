from app import db
import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.event import listens_for

def to_json(inst, cls, ignore=[]):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        if c.name in ignore:
            continue
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def json(self, ignore=[]):
        return to_json(self, self.__class__, ignore)

    @staticmethod
    def json_list(lst, ignore=[]):
        return [i.json(ignore) for i in lst]

    def add_to_db(self):
        db.session.add(self)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class RevokedTokenModel(BaseModel):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)

class User(BaseModel):
    """Model for the users table"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    tutor = db.relationship('Tutor', backref='account', uselist=False, lazy=True)
    student = db.relationship('Student', backref='account', uselist=False, lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
"""
    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        if not username or not password:
            return None

        user = cls.find_by_username(username)
        if not user or not check_password_hash(user.password_hash, password):
            return None

        return user
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
"""

class Person(BaseModel):
    """Model for the persons"""
    __abstract__ = True

    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    patronymic = db.Column(db.String(40), nullable=False)
    rank = db.Column(db.String(20), nullable=False) 

class AssociationTGS(BaseModel):
    """Model for the tgs table"""
    __tablename__ = "tgs"

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.user_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    subject_name = db.Column(db.String(128), db.ForeignKey('subjects.name'), nullable=False)
    checkpoints = db.relationship('Checkpoint', lazy='dynamic',
        backref=db.backref('tgs', lazy=True), cascade='all,delete-orphan') 

class Tutor(Person):
    """Model for the tutors table"""
    __tablename__ = "tutors"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=False, nullable=False)
    degree = db.Column(db.String(10))
    tgs = db.relationship('AssociationTGS', lazy='dynamic',
        backref=db.backref('tutor', lazy=True), cascade='all,delete-orphan')
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()

class Group(BaseModel):
    """Model for the groups table"""
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    students = db.relationship('Student', backref='group', lazy='dynamic')
    tgs = db.relationship('AssociationTGS', lazy='dynamic',
        backref=db.backref('group', lazy=True), cascade='all,delete-orphan')

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class Subject(BaseModel):
    """Model for the subjects table"""
    __tablename__ = "subjects"

    name = db.Column(db.String(128), primary_key=True)
    tgs = db.relationship('AssociationTGS', lazy='dynamic',
        backref=db.backref('subject', lazy=True), cascade='all,delete-orphan') 
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

class Student(Person):
    """Model for the students table"""
    __tablename__ = "students"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, autoincrement=False, nullable=False)
    admission_year = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    progress = db.relationship('Progress', backref=db.backref('student', lazy=True), lazy='dynamic', cascade='all,delete-orphan')

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()

@listens_for(Student, 'after_insert')
def add_group_checkpoints(mapper, connect, self):
    """trigger for the student model, that adds progress on existing checkpoints to a newly registered student"""
    student_id = (db.session.query(Student.user_id)
                    .filter(Student.group_id==self.group_id)).first()[0]
    cp_info = (db.session.query(Progress.checkpoint_id, Progress.deadline)
                .filter(Progress.student_id==student_id)).all()
    for info in cp_info:
        progress = Progress(checkpoint_id=info[0],
                            student_id=self.user_id,
                            deadline=info[1])
        self.progress.append(progress)


class Checkpoint(BaseModel):
    """Model for checkpoints table"""
    __tablename__ = "checkpoints"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    tgs_id = db.Column(db.Integer, db.ForeignKey('tgs.id'), nullable=False)
    progress = db.relationship('Progress', lazy='dynamic',
        backref=db.backref('checkpoint', lazy=True), cascade='all,delete-orphan')

class Progress(BaseModel):
    """Model for the progress table"""
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.user_id'), nullable=False)
    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoints.id'), nullable=False)
    mark = db.Column(db.Integer)
    deadline = db.Column(db.Date)
    attempts = db.Column(db.Integer, default=0)
    plagiarism = db.Column(db.String(1000))
    checkpoint_date = db.Column(db.Date)