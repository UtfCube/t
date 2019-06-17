from app import db
from app.models import User, Tutor, Group, Subject, Student, Progress
import datetime
"""
u = User(username='qwe', password_hash='1234')
db.session.add(u)
db.session.commit()
g = Group(id=7343)
db.session.add(g)
db.session.commit()
t = Tutor(user_id=1, firstname='t', lastname='t', patronymic='t', rank='p')
db.session.add(t)
db.session.commit()
s = Subject(name='algebra')
db.session.add(s)
db.session.commit()
u2 = User(username='rty', password_hash='3456')
db.session.add(u2)
db.session.commit()
st = Student(user_id=2, firstname='s', lastname='s', patronymic='s', rank='s', record_book='1234', admission_year=datetime.date(2017, 12, 10))
st.group_id=g.id
p = Progress(date=datetime.date(2017, 12, 10), mark=4)
p.subject = s
st.progress.append(p)
db.session.add(st)
db.session.commit()

from app.models import AssociationTGS
t = Tutor.query.get(1)
g = Group.query.get(7343)
s = Subject.query.get('физика')
a = AssociationTGS()
a.group = g
a.subject = s
t.tgs.append(a)
db.session.commit()
a.tutor = t
"""
st1 = Student.query.get(6)
st2 = Student.query.get(7)
st3 = Student.query.get(8)
s = Subject.query.get('физика')
p = Progress(checkpoint_name='лаб1', posting_date=datetime.date(2017, 12, 10), critical_date=datetime.date(2017, 12, 10))
p.subject = s
p.student = st1
st1.progress.append(p)
db.session.commit()