from datetime import datetime

from flask import Flask
import flask
from database.models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\Users\\alexi\\PycharmProjects\\ProjetAnnuaire\\database\\database.db"
  ##  "sqlite:///C:\\Users\\julie\\OneDrive\\Documents\\DCL\\web\\project\\database\\database.db"
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
@app.route('/tableau_de_bord')
def tableau_de_bord():
    clean()

    # Creation Eleve

    alexis = Person(id=1, first_name='Alexis', last_name='Grandjacquot', promotion=2022,
                    email='alexis', role='student')
    julien = Person(id=2, first_name='Julien', last_name='Dai', promotion=2023,
                    email='julien', role='student')
    johnny = Person(id=3, first_name='Johnny', last_name='Hallyday', promotion=1980,
                    email='johnny', role='teacher')
    momo = Person(id=4)
    toto = Person(id=5)
    nono = Person(id=6)
    roro = Person(id=7)

    db.session.add(alexis)
    db.session.add(julien)
    db.session.add(johnny)
    db.session.add(momo)
    db.session.add(toto)
    db.session.add(nono)
    db.session.add(roro)
    db.session.commit()

    # Creation stage

    expert = PFE(id=1, supervisor=momo, student=alexis, supervisor_email='momo', year=2018, duration=4,
                 description='developpement android', title='yoyo')
    ingenieur = PFE(id=2, supervisor=toto, student=julien, supervisor_email='toto', year=2019, duration=6,
                    description='python', title='popo')
    decouverte = PFE(id=3, supervisor=nono, student=johnny, supervisor_email='nono', year=1978, duration=2,
                     description='feuuuu', title='gogo')
    ouvrier = PFE(id=4, supervisor=roro, student=alexis, supervisor_email='roro', year=2025, duration=1,
                  description='usine',
                  title='koko')

    db.session.add(expert)
    db.session.add(ingenieur)
    db.session.add(decouverte)
    db.session.add(ouvrier)

    db.session.commit()

    # ajout organisations

    google = Organisation(id=1, entreprise='google')
    firefox = Organisation(id=2, entreprise='firefox')
    amazon = Organisation(id=3, entreprise='amazon')

    db.session.add(google)
    db.session.add(firefox)
    db.session.add(amazon)

    db.session.commit()

    # ajout positions

    ceo = Position(id=1, entry_date=datetime(2022, 2, 22), title='CEO', employee=alexis, organisation_name=google)
    stagiaire = Position(id=2, entry_date=datetime(2021, 5, 12), title='stagiaire', employee=julien,
                         organisation_name=amazon)
    developpeur = Position(id=3, entry_date=datetime(1998, 11, 25), title='fullstack', employee=johnny,
                           organisation_name=firefox)

    db.session.add(ceo)
    db.session.add(stagiaire)
    db.session.add(developpeur)

    db.session.commit()

    # ajout tafs

    dcl = TAF(id=1, name='dcl')
    tee = TAF(id=2, name='tee')
    demin = TAF(id=3, name='demin')
    login = TAF(id=4, name='login')

    db.session.add(dcl)
    db.session.add(tee)
    db.session.add(demin)
    db.session.add(login)

    db.session.commit()

    # attribution tafs

    alexis.tafs.append(dcl)
    alexis.tafs.append(demin)
    julien.tafs.append(dcl)
    julien.tafs.append(tee)
    johnny.tafs.append(login)



    db.session.commit()

    people = Person.query.all()
    pfes = PFE.query.all()
    all_tafs = TAF.query.all()
    organisations = Organisation.query.all()
    positions = Position.query.all()
    return flask.render_template("tableau_de_bord.html.jinja2", people=people, pfes=pfes, tafs=all_tafs,
                                 organisations=organisations, positions=positions)




@app.route('/base')
def test_base():
    clean()

    # Creation Eleve

    alexis = Person(id=1, first_name='Alexis', last_name='Grandjacquot', promotion=2022,
                     email='alexis', role='student')
    julien = Person(id=2, first_name='Julien', last_name='Dai', promotion=2023,
                     email='julien', role='student')
    johnny = Person(id=3, first_name='Johnny', last_name='Hallyday', promotion=1980,
                     email='johnny', role='teacher')
    momo=Person(id=4)
    toto=Person(id=5)
    nono=Person(id=6)
    roro=Person(id=7)

    db.session.add(alexis)
    db.session.add(julien)
    db.session.add(johnny)
    db.session.add(momo)
    db.session.add(toto)
    db.session.add(nono)
    db.session.add(roro)
    db.session.commit()

    # Creation stage

    expert = PFE(id=1, supervisor=momo, student = alexis, supervisor_email='momo', year=2018, duration=4,
                        description='developpement android', title='yoyo')
    ingenieur = PFE(id=2, supervisor=toto, student= julien, supervisor_email='toto', year=2019, duration=6,
                           description='python', title='popo')
    decouverte = PFE(id=3, supervisor=nono, student=johnny, supervisor_email='nono', year=1978, duration=2,
                            description='feuuuu', title='gogo')
    ouvrier = PFE(id=4, supervisor=roro, student = alexis, supervisor_email='roro', year=2025, duration=1, description='usine',
                  title='koko')

    db.session.add(expert)
    db.session.add(ingenieur)
    db.session.add(decouverte)
    db.session.add(ouvrier)

    db.session.commit()

    # ajout organisations

    google = Organisation(id=1, entreprise='google')
    firefox = Organisation(id=2, entreprise='firefox')
    amazon = Organisation(id=3, entreprise='amazon')

    db.session.add(google)
    db.session.add(firefox)
    db.session.add(amazon)

    db.session.commit()

    # ajout positions

    ceo = Position(id=1, entry_date=datetime(2022, 2, 22), title ='CEO', employee=alexis, organisation_name=google)
    stagiaire = Position(id=2, entry_date=datetime(2021, 5, 12), title ='stagiaire', employee=julien, organisation_name=amazon)
    developpeur = Position(id=3, entry_date=datetime(1998, 11, 25), title='fullstack', employee=johnny, organisation_name=firefox)

    db.session.add(ceo)
    db.session.add(stagiaire)
    db.session.add(developpeur)

    db.session.commit()


    #ajout tafs

    dcl = TAF(id=1, name='dcl')
    tee = TAF(id=2, name='tee')
    demin = TAF(id = 3, name='demin')
    login = TAF(id=4, name='login')

    db.session.add(dcl)
    db.session.add(tee)
    db.session.add(demin)
    db.session.add(login)

    db.session.commit()

    # attribution tafs

    alexis.tafs.append(dcl)
    alexis.tafs.append(demin)
    julien.tafs.append(dcl)
    julien.tafs.append(tee)
    johnny.tafs.append(login)

    db.session.commit()

    people=Person.query.all()
    pfes=PFE.query.all()
    all_tafs=TAF.query.all()
    organisations=Organisation.query.all()
    positions=Position.query.all()

    return flask.render_template("index.jinja2", people=people, pfes=pfes, tafs=all_tafs,
                                 organisations=organisations, positions=positions)


if __name__ == '__main__':
    app.run()
