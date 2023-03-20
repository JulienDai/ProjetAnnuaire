from datetime import datetime
from flask import Flask, render_template, request
from sqlalchemy import create_engine, select, func

from flask import Flask
import flask
from database.models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] =   "sqlite:///C:\\Users\\julie\\OneDrive\\Documents\\DCL\\web\\flaskProject4\\database\\database.db"
    ##"sqlite:///C:\\Users\\alexi\\PycharmProjects\\projet_avec_git\\ProjetAnnuaire\\database\\database.db"



app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_key1234"

db.init_app(app)

@app.route("/clean")
def clean():
    db.drop_all()
    db.create_all()
    return('cleared')
@app.route('/informations_personnelles',methods=['GET'])
def informations_personnelles():


    id_connecte = request.args.get('id')
    admin=request.args.get('admin')


    person_connect=get_person_by_id(id_connecte)
    people, pfes, all_tafs, organisations, positions = action_base_donnee()

    print(type(person_connect.etat_civil))

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
    def add_person(etat_civil, email, promotion, role, taf1, taf2, nom, prenom):

        new_person = Person(first_name=prenom, last_name=nom, etat_civil=etat_civil,
                            promotion=promotion, role=role, email=email)

        db.session.add(new_person)
        if taf1 != "":
            new_person.tafs.append(get_taf_by_name(taf1))
        if taf2 != "":
            new_person.tafs.append(get_taf_by_name(taf2))

        db.session.commit()

    result = request.form
    promotion=result['promotion']
    etat_civil = result['etat_civil']
    email = result['email']
    role= result['role']
    taf1=result['taf1']
    taf2=result['taf2']
    nom=result['nom']
    prenom=result['prenom']

    add_person(etat_civil, email, promotion, role, taf1, taf2, nom, prenom)

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
    try :
        add_position=result['add_position']
        nom_entreprise = result['nom_entreprise']
        date_debut_position = result['date_debut_position']
        titre_position = result['titre_position']
    except :
        add_position='no'
        nom_entreprise=""
        date_debut_position=""
        titre_position=""


    id_connecte = request.args.get('id')
    modify_all(id_connecte, etat_civil, email, promotion, role, taf1, taf2, titre_sujet, organisation, date_stage,
               duree_stage, email_tuteur, description_projet, nom_tuteur, prenom_tuteur, nom_entreprise,
               date_debut_position, titre_position, add_position)
    admin=request.args.get('admin')

    people = Person.query.all()

    return flask.render_template("resultat_informations_personnelles.html.jinja2", admin=admin,id=id_connecte,people=people)



def modify_all(person_id, etat_civil, email, promotion, role, taf1, taf2, titre_sujet, organisation, date_stage,
               duree_stage, email_tuteur, description_projet, nom_tuteur, prenom_tuteur, nom_entreprise,
               date_debut_position, titre_position, add_position):

    person = get_person_by_id(person_id)
    first_name = person.first_name
    last_name = person.last_name
    pfe= get_pfe_by_student_id(person_id)
    if pfe!=None:
        pfe_id=pfe.id


    remove_object_from_db(person)
    new_person = Person(id=person_id, first_name=first_name, last_name=last_name, etat_civil=etat_civil,
                        promotion=promotion, role=role, email=email)

    db.session.add(new_person)

    if taf1!="":
        new_person.tafs.append(get_taf_by_name(taf1))
    if taf2!="":
        new_person.tafs.append(get_taf_by_name(taf2))

    db.session.commit()

    tuteur = get_person_by_email(email_tuteur, nom_tuteur, prenom_tuteur)
    if pfe!=None:
        remove_object_from_db(pfe)


        new_pfe = PFE(id=pfe_id, student_id=person_id, supervisor_id=tuteur.id,
                  organisation_id=get_organisation_by_name(organisation).id, year=date_stage, duration=duree_stage,
                  description=description_projet, title=titre_sujet)

    else:
        new_pfe = PFE(student_id=person_id, supervisor_id=tuteur.id,
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
            return pfe



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
    organisations=Organisation.query.all()
    count=int(0)
    tafs_existantes=[]
    organisations_existantes=[]

    for taf in tafs:
        for value in dictionnaire:
            if taf.name==dictionnaire[value]:
                tafs_existantes.append(taf)
    for taf in tafs:
        if taf not in tafs_existantes:
            remove_object_from_db(taf)
    for organisation in organisations:
        for value in dictionnaire:
            if organisation.entreprise==dictionnaire[value]:
                organisations_existantes.append(organisation)
    for organisation in organisations:
        if organisation not in organisations_existantes:
            remove_object_from_db(organisation)



    while dictionnaire != {} :

        value=list(dictionnaire.keys())[0]


        if (value[0]=='<' or value[:12] == 'organisation'):
            print(value[:12])
            for organisation in organisations:
                if organisation.entreprise==dictionnaire[value]:
                    count=1

            if count==0:

                new_organisation=Organisation(entreprise=dictionnaire[value])
                count=1

                db.session.add(new_organisation)
                db.session.commit()
            dictionnaire.pop(value)


        if value[0]!='<' and value[:12] != 'organisation':
            for taf in tafs:
                if dictionnaire[value]==taf.name:
                    responsable_email=dictionnaire[value+'_responsable']
                    respo=get_id_by_only_email(responsable_email)
                    taf.respo_id=respo
                    taf.description=dictionnaire[value+'_description']
                    count=1


            if count==0:
                responsable_email = dictionnaire[value + '_responsable']
                respo = get_id_by_only_email(responsable_email)
                new_taf = TAF(name = dictionnaire[value], respo_id=respo, description = dictionnaire[value+'_description'])
                db.session.add(new_taf)
                db.session.commit()


            dictionnaire.pop(value)
            dictionnaire.pop(value + '_responsable')
            dictionnaire.pop(value + '_description')
        count=0





    tafs = TAF.query.all()
    for taf in tafs:
        print(taf.name)

    organisations = Organisation.query.all()
    for organisation in organisations:
        print(organisation.entreprise)

    admin = 'admin'
    return flask.render_template("resultat_informations_personnelles.html.jinja2", admin=admin)



@app.route('/supprimer_personne', methods=['GET', 'POST'])

def remove_person():
    id_connecte = request.args.get('id')
    print(id_connecte)
    print(get_person_by_id(id_connecte))

    remove_object_from_db(get_person_by_id(id_connecte))

    admin = 'admin'
    return flask.render_template("resultat_informations_personnelles.html.jinja2", admin=admin)


if __name__ == '__main__':
    app.run()
