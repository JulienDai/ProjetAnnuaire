let new_organisation=0;
let new_taf=0;

function set_every_input_on_read_only(){
    let tafs=document.querySelectorAll(".taf");
    let organisations=document.querySelectorAll(".organisation");

    console.log(tafs)
    for (const taf of tafs){
        let name=taf.querySelector("#name");
        let responsable=taf.querySelector("#responsable");
        let description=taf.querySelector("#description")
        name.readOnly=true;
        responsable.readOnly=true;
        description.readOnly=true;
    }
    for (const organisation of organisations){
        let name=organisation.querySelector("#entreprise");
        name.readOnly=true

    }
}
set_every_input_on_read_only()


function edit_one_taf_or_organisation(element){
    console.log(element.className)
    if(element.className=='taf')
    {
     let name=element.querySelector("#name");
     let responsable=element.querySelector("#responsable");
     let description=element.querySelector("#description");

     name.readOnly=false;
     responsable.readOnly=false;
     description.readOnly=false;}
        else{
        let entreprise=element.querySelector("#entreprise");
        entreprise.readOnly=false;
    }


}

function supprimer_taf_ou_organisation(element){
    let message="";
        if(element.className=='taf')
    {
     let name=element.querySelector("#name").value;
     message="Êtes-vous sûr de vouloir supprimer? "+name +" des tafs ?"
    }else{
          let entreprise=element.querySelector("#entreprise").value
          message=  "Êtes-vous sûr de vouloir supprimer? "+entreprise +" des organisations ?"

        }

     var res = confirm(message);
    if(res) {

        element.remove()
    }

}

function ajout_taf(){
    new_taf++;
   let tbody_tafs= document.getElementById("tbody_taf");

    let tr=document.createElement("tr")
    tr.className="taf"

    let td_name=document.createElement("td")
    let td_responsable=document.createElement("td")
    let td_description=document.createElement("td")
    let td_supprimer_modifier=document.createElement("td")

    let button_modifier=document.createElement("button")
    let button_supprimer=document.createElement("button")

    button_supprimer.type="button"
    button_modifier.type="button"

    button_modifier.className="modifier"
    button_supprimer.className="supprimer"

    button_supprimer.innerHTML="Supprimer"
    button_modifier.innerHTML="Modifier"



    button_modifier.setAttribute("onclick","edit_one_taf_or_organisation(event.target.parentElement.parentElement)")
    button_supprimer.setAttribute("onclick","supprimer_taf_ou_organisation(event.target.parentElement.parentElement)")




    let input_name=document.createElement("input")
    let input_responsable=document.createElement("input")
    let input_description=document.createElement("input")

    input_name.type="text"
    input_responsable.type="text"
    input_description.type="description"

    input_name.name="taf_new_"+new_taf
    input_responsable.name="taf_new_"+new_taf+"_responsable"
    input_description.name="taf_new_"+new_taf+"_description"

    input_name.readOnly=true
    input_responsable.readOnly=true
    input_description.readOnly=true

    input_name.id="name"
    input_responsable.id="responsable"
    input_description.id="description"


    td_name.appendChild(input_name)
    td_responsable.appendChild(input_responsable)
    td_description.appendChild(input_description)
    td_supprimer_modifier.appendChild(button_modifier)
    td_supprimer_modifier.appendChild(button_supprimer)

    tr.appendChild(td_name)
    tr.appendChild(td_responsable)
    tr.appendChild(td_description)
    tr.appendChild(td_supprimer_modifier)

    tbody_tafs.appendChild(tr)

}


function ajout_organisation(){
    new_organisation++;
   let tbody_organisations= document.getElementById("tbody_organisation");

    let tr=document.createElement("tr")
    tr.className="organisation"

    let td_entreprise=document.createElement("td")
    let td_supprimer_modifier=document.createElement("td")

    let button_modifier=document.createElement("button")
    let button_supprimer=document.createElement("button")

    button_supprimer.type="button"
    button_modifier.type="button"

    button_modifier.className="modifier"
    button_supprimer.className="supprimer"

    button_supprimer.innerHTML="Supprimer"
    button_modifier.innerHTML="Modifier"

    button_modifier.setAttribute("onclick","edit_one_taf_or_organisation(event.target.parentElement.parentElement)")
    button_supprimer.setAttribute("onclick","supprimer_taf_ou_organisation(event.target.parentElement.parentElement)")


    let input_entreprise=document.createElement("input")

    input_entreprise.type="text"


    input_entreprise.name="organisation_new_"+new_organisation

    input_entreprise.readOnly=true


    input_entreprise.id="entreprise"



    td_entreprise.appendChild(input_entreprise)

    td_supprimer_modifier.appendChild(button_modifier)
    td_supprimer_modifier.appendChild(button_supprimer)

    tr.appendChild(td_entreprise)
    tr.appendChild(td_supprimer_modifier)

    tbody_organisations.appendChild(tr)

}

