from datetime import datetime
from flask import Flask, render_template, request
from sqlalchemy import create_engine, select, func

from flask import Flask
import flask
from database.models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\Users\\alexi\\PycharmProjects\\projet_avec_git\\ProjetAnnuaire\\database\\database.db"
                                     ##  "sqlite:///C:\\Users\\julie\\OneDrive\\Documents\\DCL\\web\\flaskProject4\\database\\database.db"


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_key1234"

db.init_app(app)



@app.route("/clean")
def clean():
    db.drop_all()
    db.create_all()
    return "Cleaned!"


@app.route('/informations_personnelles',methods=['GET'])
def informations_personnelles():


    id_connecte = request.args.get('id')
    admin=request.args.get('admin')

    person_connect=get_person_by_id(id_connecte)
    people, pfes, all_tafs, organisations, positions = action_base_donnee()


    pfe=None
    for pfe_ in pfes:
        if str(pfe_.student.id)==id_connecte:
            pfe=pfe_
            break






   ## db.session.query(Person.query(id=id_connecte).all())

    return flask.render_template("informations_personnelles.html.jinja2",pfe=pfe,id=id_connecte,person=person_connect,admin=admin,tafs=all_tafs)

@app.route('/creation_personne',methods=['GET'])
def creation_personne():
    people, pfes, all_tafs, organisations, positions = action_base_donnee()



    admin='admin'
    return flask.render_template("creation_personne.html.jinja2", admin=admin, tafs=all_tafs)

@app.route('/resultat_creation_personne',methods=['GET','POST'])
def resultat_creation_personne():

    admin='admin'
    return flask.render_template("resultat_informations_personnelles.html.jinja2",admin=admin)





@app.route('/resultat_informations_personnelles', methods=['POST','GET'])
def store():

    result = request.form
    promotion=result['promotion']
    etat_civil = result['etat_civil']
    email = result['email']
    role= result['role']
    taf1=result['taf1']
    taf2=result['taf2']

    # Récupération des données de stage
    result = request.form

    titre_sujet=result['titre_sujet']
    organisation=result['organisation']
    date_stage=result['date_stage']
    duree_stage=result['duree_stage']
    email_tuteur=result['email_tuteur']
    nom_tuteur=result['nom_tuteur']
    prenom_tuteur=result['prenom_tuteur']
    description_projet=result['description_projet']


    # Récupération de la position

    result=request.form

    add_position=result['add_position']
    nom_entreprise=result['nom_entreprise']
    date_debut_position=result['date_debut_position']
    titre_position=result['titre_position']


    id_connecte = request.args.get('id')
    person_connect = get_person_by_id(id_connecte)
    modify_all(id_connecte, etat_civil, email, promotion, role, taf1, taf2, titre_sujet, organisation, date_stage,
               duree_stage, email_tuteur, description_projet, nom_tuteur, prenom_tuteur, nom_entreprise,
               date_debut_position, titre_position, add_position)
    #modify_person(id_connecte, etat_civil, email, promotion, role, taf1, taf2)
    #modify_pfe(titre_sujet, organisation, date_stage, duree_stage, email_tuteur, description_projet, id_connecte,
    #           nom_tuteur, prenom_tuteur)
    admin=request.args.get('admin')

    people = Person.query.all()

    return flask.render_template("resultat_informations_personnelles.html.jinja2", admin=admin,id=id_connecte,people=people)



def modify_all(person_id, etat_civil, email, promotion, role, taf1, taf2, titre_sujet, organisation, date_stage,
               duree_stage, email_tuteur, description_projet, nom_tuteur, prenom_tuteur, nom_entreprise,
               date_debut_position, titre_position, add_position):

    person = get_person_by_id(person_id)
    first_name = person.first_name
    last_name = person.last_name
    pfe, pfe_id = get_pfe_by_student_id(person_id)


    remove_object_from_db(person)
    new_person = Person(id=person_id, first_name=first_name, last_name=last_name, etat_civil=etat_civil,
                        promotion=promotion, role=role, email=email)

    db.session.add(new_person)
    new_person.tafs.append(get_taf_by_name(taf1))
    new_person.tafs.append(get_taf_by_name(taf2))

    db.session.commit()

    tuteur = get_person_by_email(email_tuteur, nom_tuteur, prenom_tuteur)
    remove_object_from_db(pfe)

    new_pfe = PFE(id=pfe_id, student_id=person_id, supervisor_id=tuteur.id,
                  organisation_id=get_organisation_by_name(organisation).id, year=date_stage, duration=duree_stage,
                  description=description_projet, title=titre_sujet)

    db.session.add(new_pfe)
    db.session.commit()

    if add_position=='on':
        organisation=get_organisation_by_name(nom_entreprise)
        new_position=Position(person_id=person_id, entry_date=date_debut_position, title=titre_position)
        new_position.organisation.append(organisation)
        db.session.add(new_position)
        db.session.commit()

def get_id_by_only_email(email_personne):
    people = Person.query.all()
    for person in people:
        if person.email == email_personne:
            return (person.id)
def get_pfe_by_student_id(student_id):
    people=Person.query.all()
    student=get_person_by_id(student_id)

    pfes = PFE.query.all()
    for pfe in pfes:
        if pfe.student_id==int(student_id):
            return pfe,pfe.id



def save_object_to_db(db_object):
    db.session.add(db_object)
    db.session.commit()

def get_taf_by_name(taf_name):
    tafs = TAF.query.all()
    for taf in tafs:
        if taf.name==taf_name:
            return(taf)
def get_person_by_email(email_personne, nom_personne, prenom_personne):
    people = Person.query.all()
    for person in people:
        if person.email == email_personne:
            return(person)
    new_person=Person(email=email_personne, first_name=prenom_personne, last_name=nom_personne)

    save_object_to_db(new_person)

    return new_person


def remove_object_from_db(db_object):
    db.session.delete(db_object)
    db.session.commit()

def get_organisation_by_name(entreprise_name):
    organisations=Organisation.query.all()
    for organisation in organisations:
        if organisation.entreprise==entreprise_name:
            return(organisation)
    new_organisation = Organisation(entreprise=entreprise_name)
    db.session.add(new_organisation)
    db.session.commit()
    return(new_organisation)

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
        if person.id == int(person_id):
            return person

def get_taf_by_name(taf_name):

    tafs = TAF.query.all()
    for taf in tafs:
        if taf.name==taf_name:
            return(taf)

def modify_person(person_id, etat_civil, email, promotion, role, taf1, taf2):
    person=get_person_by_id(person_id)
    first_name=person.first_name
    last_name=person.last_name

    remove_object_from_db(person)
    new_person=Person(id=person_id, first_name=first_name, last_name=last_name, etat_civil=etat_civil,
                      promotion=promotion, role=role, email=email)

    db.session.add(new_person)
    new_person.tafs.append(get_taf_by_name(taf1))
    new_person.tafs.append(get_taf_by_name(taf2))

    db.session.commit()

def add_person(first_name, last_name, promotion, etat_civil, email, role, taf1, taf2):
    new_person=Person(first_name=first_name, last_name=last_name, promotion=promotion, email=email, role=role,
                      etat_civil=etat_civil)
    db.session.add(new_person)
    new_person.tafs.append(taf1)
    new_person.tafs.append(taf2)
    db.session.add(new_person)
    db.session.commit()


def action_base_donnee():
    db.drop_all()
    db.create_all()

    # Creation Eleve

    alexis = Person(first_name='Alexis', last_name='Grandjacquot', promotion=2022,
                    email='alexis', role='student')
    julien = Person(first_name='Julien', last_name='Dai', promotion=2023,
                    email='julien', role='student')
    johnny = Person(first_name='Johnny', last_name='Hallyday', promotion=1980,
                    email='johnny', role='teacher')
    momo = Person()
    toto = Person()
    nono = Person()
    roro = Person()

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

    expert = PFE(supervisor_id=4, student_id=1, organisation=firefox,
                 year=2018, duration=4,
                 description='developpement android', title='yoyo')
    ingenieur = PFE(supervisor_id=5, student_id=2, organisation=google,
                    year=2019, duration=6,
                    description='python', title='popo')
    decouverte = PFE(supervisor_id=6, student_id=3, organisation=amazon,
                     year=1978, duration=2,
                     description='feuuuu', title='gogo')

    db.session.add(expert)
    db.session.add(ingenieur)
    db.session.add(decouverte)

    db.session.commit()

    # ajout positions

    ceo = Position(entry_date=2022, title='CEO', person_id=1)
    stagiaire = Position(entry_date=2021, title='stagiaire', person_id=2)
    developpeur = Position(entry_date=1998, title='fullstack', person_id=3)

    db.session.add(ceo)
    db.session.add(stagiaire)
    db.session.add(developpeur)

    ceo.organisation.append(google)
    stagiaire.organisation.append(amazon)
    developpeur.organisation.append(google)
    developpeur.organisation.append(firefox)

    # ajout tafs

    dcl = TAF(name='dcl')
    tee = TAF(name='tee')
    demin = TAF(name='demin')
    login = TAF(name='login')

    db.session.add(dcl)
    db.session.add(tee)
    db.session.add(demin)
    db.session.add(login)

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
    admin=request.args.get('admin')



    people,pfes,all_tafs,organisations, positions=action_base_donnee()


    return flask.render_template("tableau_de_bord.html.jinja2", people=people, pfes=pfes, tafs=all_tafs,
                                 organisations=organisations, positions=positions,current_year=datetime.now().year,nombre_organisations=len(organisations),nombre_personnes=len(people),id_connecte=str(id_connecte),admin=admin)


@app.route('/modification_taf_organisation',methods=['GET','POST'])
def modification_taf_organisation():
    people, pfes, all_tafs, organisations, positions = action_base_donnee()

    ##print(request.args.to_dict()) pour récupérer la requette

    return flask.render_template("modification_taft_organisation.html.jinja2",tafs=all_tafs,organisations=organisations)



@app.route('/modification_taf_organisation/resultat', methods=['GET', 'POST'])
def modification_tafs():

    dictionnaire = request.form.to_dict()
    tafs = TAF.query.all()
    count=int(0)
    for value in dictionnaire :
        for taf in tafs:
            if dictionnaire[value]==taf.name:
                responsable_email=dictionnaire[value+'_responsable']
                respo=get_id_by_only_email(responsable_email)
                taf.respo_id=respo
                taf.description=dictionnaire[value+'_description']





    return('fin')


if __name__ == '__main__':
    app.run()
