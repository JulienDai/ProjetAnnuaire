from datetime import datetime
from flask import Flask, render_template, request
from sqlalchemy import create_engine, select, func

from flask import Flask
import flask
from database.models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\Users\\julie\\OneDrive\\Documents\\DCL\\web\\project\\database\\database.db"
##    "sqlite:///C:\\Users\\alexi\\PycharmProjects\\ProjetAnnuaire\\database\\database.db"



app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_key1234"

db.init_app(app)


@app.route('/')
def form():
    return render_template('form.html')

@app.route('/resultat', methods=['POST', 'GET'])
def hello():
    clean()
    result = request.form
    new_person = Person(first_name=result['first_name'], last_name=result['last_name'])
    print(result['first_name'])
    save_object_to_db(new_person)

    people = Person.query.all()

    return render_template("resultat.html", people=people)


# @app.route("/clean")
def clean():
    db.drop_all()
    db.create_all()
    return "Cleaned!"


@app.route('/informations_personnelles')
def informations_personnelles():
   # id_connecte = request.args.get('id')
   # people, pfes, all_tafs, organisations, positions = action_base_donnee()


  ## db.session.query(Person.query(id=id_connecte).all())

    return flask.render_template("informations_personnelles.html.jinja2")


@app.route('/resultat_informations_personnelles', methods=['POST'])
def test():
    return('oui')

def save_object_to_db(db_object):
    db.session.add(db_object)
    db.session.commit()


def get_person_by_email(email_personne, nom_personne, prenom_personne):
    people=Person.query.all()
    for person in people:
        if person.email == email_personne:
            return(person)
    new_person=Person(email=email_personne, first_name=prenom_personne, last_name=nom_personne)

    db.session.add(new_person)
    db.session.commit()

def remove_object_from_db(db_object):
    db.session.delete(db_object)
    db.session.commit()

def add_pfe_link_people_and_organisation(nom_tuteur, prenom_tuteur, email_tuteur, organisation, titre_sujet, date_stage,
                                         description, id_eleve):
    tuteur=get_person_by_email(email_tuteur, nom_tuteur, prenom_tuteur)
    new_pfe=PFE(supervisor=tuteur, organisation=organisation, student=id_eleve,
                year=date_stage, duration=duree_stage, description=description, title=titre_sujet)
    db.session.add(new_pfe)
    db.session.commit()


def creer_organisation(entreprise_name):
    new_organisation = Organisation(entreprise_name)
    db.session.add(new_organisation)
    db.commit()
def get_organisation_by_name(entreprise_name):
    organisations=Organisation.query.all()
    for organisation in organisations:
        if organisation.entreprise==entreprise_name:
            return(organisation)
    creer_organisation(entreprise_name)


def add_organisation_to_position(date_debut_position, nom_entreprise, add_position, titre_position, id_eleve):
    if add_position:
        organisation=get_organisation_by_name(nom_entreprise)
        new_position=position(employee=id_eleve, entry_date=date_debut_position, title=titre_position)
        db.session.add(new_position)
        position.organisation.append(organisation)
        db.commit()


def add_taf_to_person(id_eleve, taf):
    person=get_person_by_id(id_eleve)
    person.tafs.append(taf)
    db.add(person)
    db.commit()

def get_person_by_id(person_id):
    people = Person.query.all()
    for person in people:
        if person.id==person_id:
            return(person)

def modify_person(person_id, etat_civil, email, promotion, role, taf1, taf2):
    person=get_person_by_id(person_id)
    first_name=person.first_name
    last_name=person.last_name

    remove_object_from_db(person)
    new_person=Person(id=person_id, first_name=first_name, last_name=last_name, etat_civil=etat_civil,
                      promotion=promotion, role=role, email=email)

    db.session.add(new_person)
    new_person.tafs.append(taf1)
    new_person.tafs.append(taf2)

    db.commit


def action_base_donnee():
    clean()

    # Creation Eleve

    alexis = Person(id=1,first_name='Alexis', last_name='Grandjacquot', promotion=2022,
                    email='alexis', role='student')
    julien = Person(id=2,first_name='Julien', last_name='Dai', promotion=2023,
                    email='julien', role='student')
    johnny = Person(id=3,first_name='Johnny', last_name='Hallyday', promotion=1980,
                    email='johnny', role='teacher')
    momo = Person(id=5)
    toto = Person(id=6)
    nono = Person(id=7)
    roro = Person(id=8)

    db.session.add(alexis)
    db.session.add(julien)
    db.session.add(johnny)
    db.session.add(momo)
    db.session.add(toto)
    db.session.add(nono)
    db.session.add(roro)
    db.session.commit()

    # ajout organisations

    google = Organisation(entreprise='google')
    firefox = Organisation(entreprise='firefox')
    amazon = Organisation(entreprise='amazon')

    db.session.add(google)
    db.session.add(firefox)
    db.session.add(amazon)

    db.session.commit()

    # Creation PFE

    expert = PFE(supervisor=momo, student=alexis, organisation=firefox,
                 year=2018, duration=4,
                 description='developpement android', title='yoyo')
    ingenieur = PFE(supervisor=toto, student=julien, organisation=google,
                    year=2019, duration=6,
                    description='python', title='popo')
    decouverte = PFE(supervisor=nono, student=johnny, organisation=amazon,
                     year=1978, duration=2,
                     description='feuuuu', title='gogo')
    ouvrier = PFE(supervisor=roro, student=alexis, year=2025, organisation=google,
                  duration=1, description='usine',
                  title='koko')

    db.session.add(expert)
    db.session.add(ingenieur)
    db.session.add(decouverte)
    db.session.add(ouvrier)

    db.session.commit()

    # ajout positions

    ceo = Position(entry_date=datetime(2022, 2, 22), title='CEO', employee=alexis)
    stagiaire = Position(entry_date=datetime(2021, 5, 12), title='stagiaire', employee=julien)
    developpeur = Position(entry_date=datetime(1998, 11, 25), title='fullstack', employee=johnny)

    db.session.add(ceo)
    db.session.add(stagiaire)
    db.session.add(developpeur)

    ceo.organisation.append(google)
    stagiaire.organisation.append(amazon)
    developpeur.organisation.append(google)
    developpeur.organisation.append(firefox)

    db.session.commit()

    # ajout tafs

    dcl = TAF(name='dcl')
    tee = TAF(name='tee')
    demin = TAF(name='demin')
    login = TAF(name='login')

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
    return people, pfes, all_tafs, organisations, positions


@app.route('/tableau_de_bord',methods=['GET','POST'])
def tableau_de_bord():
    id_connecte = request.args.get('id')


    people,pfes,all_tafs,organisations, positions=action_base_donnee()


    return flask.render_template("tableau_de_bord.html.jinja2", people=people, pfes=pfes, tafs=all_tafs,
                                 organisations=organisations, positions=positions,current_year=datetime.now().year,nombre_organisations=len(organisations),nombre_personnes=len(people),id_connecte=str(id_connecte))




@app.route('/base')
def test_base():
    clean()

    # Creation Eleve

    alexis = Person(first_name='Alexis', last_name='Grandjacquot', promotion=2022,
                     email='alexis', role='student')
    julien = Person(first_name='Julien', last_name='Dai', promotion=2023,
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

    # ajout organisations

    google = Organisation(entreprise='google')
    firefox = Organisation(entreprise='firefox')
    amazon = Organisation(entreprise='amazon')

    db.session.add(google)
    db.session.add(firefox)
    db.session.add(amazon)

    db.session.commit()

    # Creation stage

    expert = PFE(supervisor=momo, student=alexis, organisation=firefox,
                 year=2018, duration=4,
                 description='developpement android', title='yoyo')
    ingenieur = PFE(supervisor=toto, student=julien, organisation=google,
                    year=2019, duration=6,
                    description='python', title='popo')
    decouverte = PFE(supervisor=nono, student=johnny, organisation=amazon,
                     year=1978, duration=2,
                     description='feuuuu', title='gogo')
    ouvrier = PFE(supervisor=roro, student=alexis, year=2025, organisation=google,
                  duration=1, description='usine',
                  title='koko')

    db.session.add(expert)
    db.session.add(ingenieur)
    db.session.add(decouverte)
    db.session.add(ouvrier)

    db.session.commit()

    # ajout positions

    ceo = Position(entry_date=datetime(2022, 2, 22), title ='CEO', employee=alexis)
    stagiaire = Position(entry_date=datetime(2021, 5, 12), title ='stagiaire', employee=julien)
    developpeur = Position(entry_date=datetime(1998, 11, 25), title='fullstack', employee=johnny)

    db.session.add(ceo)
    db.session.add(stagiaire)
    db.session.add(developpeur)
    ceo.organisation.append(google)
    stagiaire.organisation.append(amazon)
    stagiaire.organisation.append(firefox)

    db.session.commit()


    #ajout tafs

    dcl = TAF(name='dcl')
    tee = TAF(name='tee')
    demin = TAF(name='demin')
    login = TAF(name='login')

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
