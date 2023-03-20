from database.database import db


junction_table_etudes=db.Table('etudes',
                        db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
                        db.Column('taf_id', db.Integer, db.ForeignKey('taf.id')))

junction_table_positions=db.Table('position_organisation',
                                  db.Column('position_id', db.Integer, db.ForeignKey('position.id')),
                                  db.Column('organisation_id', db.Integer, db.ForeignKey('organisation.id')))


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    promotion = db.Column(db.Integer)
    role = db.Column(db.String(50))
    email=db.Column(db.String(50))
    etat_civil=db.Column(db.String(10))
    tafs=db.relationship('TAF', backref='people', secondary=junction_table_etudes)



class PFE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    student=db.relationship('Person', backref='pfe_student', foreign_keys=[student_id])
    supervisor_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    supervisor=db.relationship('Person', backref='pfe_supervisor', foreign_keys=[supervisor_id])
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    organisation = db.relationship('Organisation', backref='pfe_organisation')
    year=db.Column(db.Integer)
    duration=db.Column(db.Integer)
    description=db.Column(db.String(50))
    title=db.Column(db.String(50))

class Organisation(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    entreprise=db.Column(db.String(50))



class TAF(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    respo_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    respo = db.relationship('Person', backref='responsable_id')
    description= db.Column(db.String(50))

class Position(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    entry_date=db.Column(db.Integer)
    title=db.Column(db.String(50))
    employee=db.relationship('Person', backref='positions')
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    organisation = db.relationship('Organisation', backref='positions', secondary=junction_table_positions)




