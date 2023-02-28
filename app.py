from flask import Flask
import flask
from database.models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "sqlite:///C:\\Users\\julie\\OneDrive\\Documents\\DCL\\web\\flaskProject4\\database\\database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_key1234"

db.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello Julien!'


# @app.route("/clean")
def clean():
    db.drop_all()
    db.create_all()
    return "Cleaned!"


@app.route('/base')
def test_base():
    clean()

    # Creation Eleve

    alexis = Student(id=1, first_name='Alexis', last_name='Grandjacquot', promotion=2022,
                     email='alexis', taf_2A='DCL', taf_2A_year='2020',
                     taf_3A='Login', taf_3A_year='2021', company='google', company_entry_year='2024',
                     company_position='CEO', company_description='trop bon les cartes graphiques')
    julien = Student(id=2, first_name='Julien', last_name='Dai', promotion=2023,
                     email='julien', taf_2A='DCL', taf_2A_year='2020',
                     taf_3A='Cyber', taf_3A_year='2021', company='orange', company_entry_year='2025',
                     company_position='fullstack', company_description='Java')
    johnny = Student(id=3, first_name='Johnny', last_name='Hallyday', promotion=1980,
                     email='johnny', taf_2A='Feu', taf_2A_year='1978',
                     taf_3A='bois', taf_3A_year='1979', company='firefox', company_entry_year='1990',
                     company_position='chauffeur de salle', company_description='il fait chaud ici')

    db.session.add(alexis)
    db.session.add(julien)
    db.session.add(johnny)
    db.session.commit()

    # Creation stage

    expert = Internship(id=1, supervisor_name='momo', supervisor_email='momo', year=2018, duration=4,
                        description='developpement android')
    ingenieur = Internship(id=2, supervisor_name='toto', supervisor_email='toto', year=2019, duration=6,
                           description='python')
    decouverte = Internship(id=3, supervisor_name='nono', supervisor_email='nono', year=1978, duration=2,
                            description='feuuuu')
    db.session.add(expert)
    db.session.add(ingenieur)
    db.session.add(decouverte)
    db.session.commit()

    # ajout stage

    alexis.internship_id.append(expert)
    julien.internship_id.append(ingenieur)
    johnny.internship_id.append(decouverte)

    db.session.commit()

    students = Student.query.all()
    internships = Internship.query.all()

    return flask.render_template("index.jinja2", students=students, internships=internships)


if __name__ == '__main__':
    app.run()
