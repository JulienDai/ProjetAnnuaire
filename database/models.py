from database.database import db


junction_table = db.Table('internships',
                          db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                          db.Column('internship_id', db.Integer, db.ForeignKey('internship.id')),
                          )


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    promotion = db.Column(db.Integer)
    email=db.Column(db.String(50))
    taf_2A_year = db.Column(db.Integer)
    taf_2A = db.Column(db.String(50))
    taf_3A = db.Column(db.String(50))
    taf_3A_year = db.Column(db.Integer)
    company=db.Column(db.String(50))
    company_entry_year=db.Column(db.Integer)
    company_position=db.Column(db.String(50))
    company_description=db.Column(db.String(50))
    internship_id=db.relationship('Internship', backref='students', secondary=junction_table)



class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supervisor_name = db.Column(db.String(50))
    supervisor_email = db.Column(db.String(50))
    year=db.Column(db.Integer)
    duration=db.Column(db.Integer)
    description=db.Column(db.String(50))




