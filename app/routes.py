# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from functools import wraps  
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request, current_app

import jwt

from app.models import User, Tutor, Student, Group, Subject, Progress, AssociationTGS, Checkpoint
from dateutil.parser import parse

def token_required(func):
    @wraps(func)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(username=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return func(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401   
    return _verify


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

def get_user_type(user):
    tutor = Tutor.query.filter_by(user_id=user.id).first()
    if not tutor:
        return 'student'
    else:
        return 'tutor'

@app.route('/api/login', methods=['POST'])
def login():
    print('login')
    if request.method == 'POST':
        data = request.get_json()
        if data:
            user = User.authenticate(**data)
            if not user:
                return jsonify({"message": "invalid credentials", "authenticated": False}), 401
            token = jwt.encode({
                'sub': user.username,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=30)},
                current_app.config['SECRET_KEY'])
            return jsonify({ 'token': token.decode('UTF-8'), 'type': get_user_type(user) })

@app.route('/api/register/tutor', methods=['POST'])
def register_tutor():
    data = request.get_json()
    user = User(data['username'], data['password'])
    db.session.add(user)
    db.session.commit()
    tutor = Tutor(user_id=user.id,
                    lastname=data.get('lastname'),
                    firstname=data.get('firstname'),
                    patronymic=data.get('patronymic'),
                    rank=data.get('rank'), 
                    degree=data.get('degree'))
    db.session.add(tutor)
    db.session.commit()
    return jsonify({"message": "You are now a register user"}), 200


@app.route('/api/register/student', methods=['POST'])
def register_student():
    data = request.get_json()
    user = User(data['username'], data['password'])
    db.session.add(user)
    group = Group.query.filter_by(id=data.get('group_id')).first()
    if group is None:
        group = Group(id=data.get('group_id'))
        db.session.add(group)
    student = Student(user_id=user.id,
                        lastname=data.get('lastname'),
                        firstname=data.get('firstname'),
                        patronymic=data.get('patronymic'),
                        rank=data.get('rank'), 
                        admission_year=data.get('admission_year'), 
                        group_id=group.id)
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "You are now a register user"}), 200

@app.route('/api/tutor/home', methods=['GET', 'POST'])
@token_required
def tutor_home(user):
    tutor = Tutor.query.filter_by(user_id=user.id).first()
    if request.method == 'GET':
        associations = tutor.tgs.all()
        return jsonify(AssociationTGS.serialize_list(associations))
    if request.method == 'POST':
        data = request.get_json()
        subject = Subject.query.get(data.get('subject_name'))
        if subject is None:
            subject = Subject(name=data.get('subject_name'))
            db.session.add(subject)
        group = Group.query.get(data.get('group_id'))
        if group is None: 
            group = Group(id=data.get('group_id'))
            db.session.add(group)
        association = AssociationTGS()
        association.subject = subject
        association.group = group
        tutor.tgs.append(association)
        db.session.commit()
        return jsonify({"message": "success"}), 200

@app.route('/api/student/home')
@token_required
def student_home(user):
    student = Student.query.filter_by(user_id=user.id).first()
    group = Group.query.filter_by(id=student.group_id).first()
    subjects = [x[0] for x in group.tgs.with_entities(AssociationTGS.subject_name)]
    return jsonify({"username": user.username, "subjects": subjects})

def set_progress_names(el):
    return {
        "name": el[0], 
        "posting_date": el[1],
        "critical_date": el[2],
        "pass_date": el[3],
        "approaches_number": el[4]
    }

@app.route('/api/student/<subject>')
@token_required
def get_subject_progress(user, subject):
    student = Student.query.filter_by(user_id=user.id).first()
    info = (db.session.query(Checkpoint.name,
                    Checkpoint.posting_date,
                    Checkpoint.critical_date,
                    Progress.pass_date,
                    Progress.approaches_number)
                .join(Progress)
                .join(AssociationTGS)
                .filter(AssociationTGS.subject_name == subject)
                .filter(Progress.student_id == student.user_id)
                ).all()
    info = [set_progress_names(el) for el in info]
    return jsonify(info)

@app.route('/api/tutor/<subject>/<group_id>', methods=['GET', 'POST'])
@token_required
def checkpoints(user, subject, group_id):
    if request.method == 'GET':
        tutor = Tutor.query.filter_by(user_id=user.id).first()
        checkpoints = tutor.tgs.filter_by(subject_name=subject, group_id=group_id).first().checkpoints.all()
        return jsonify(Checkpoint.json_list(checkpoints))
    if request.method == 'POST':
        data = request.get_json()
        if data:
            tutor = Tutor.query.filter_by(user_id=user.id).first()
            tgs = tutor.tgs.filter_by(subject_name=subject, group_id=group_id).first()
            checkpoint = Checkpoint(name=data.get('name'),
                                    posting_date=parse(data.get('posting_date')),
                                    critical_date=parse(data.get('critical_date')),
                                    tgs_id=tgs.id)
            db.session.add(checkpoint)    
            group = Group.query.get(tgs.group_id)
            for student in group.students:
                progress = Progress(checkpoint_id=checkpoint.id,
                                    student_id=student.user_id)
                student.progress.append(progress)
            db.session.commit()
        return jsonify({"message": "success"})

"""
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
"""