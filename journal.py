from app import app, db
from app.models import User, Tutor, Group, Subject, Student

@app.shell_context_processor
def make_shell_contex():
	return {
			'db': db, 
			'User': User, 
			'Tutor': Tutor, 
			'Group': Group,
			'Subject': Subject,
			'Student': Student,
		}