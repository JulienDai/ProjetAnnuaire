# ProjetAnnuaire
Il y a deux manière de se connecter au site:

Il est possible de se connecter en tant qu'administrateur en rentrant cet url :
http://127.0.0.1:5000/tableau_de_bord?admin=admin

Il est aussi possible de se connecter en tant qu'utilisateur en rentrant cet url :
http://127.0.0.1:5000/tableau_de_bord?id=1 , (Il est possible le chiffre 1, en fonction 
de l'identifiant de l'utilisateur avec qui l'on se connecte).



Notre architecture comprend plus dossiers. Le dossier static, templates ainsi que le fichier app.py.  

-Le dossier templates les différents fichiers html : identification.html.jinja2, tableau_de_bord.html.jinja2,
informations_personnelles.html.jinja2, ainsi que modification_taf_organisation.html.jinja2 ainsi que resultat.html
et resultat_informations_personnelles.html.jinja2.

-Le dossier static contient les code css, javascript et les images nécessaire au différents templates .

