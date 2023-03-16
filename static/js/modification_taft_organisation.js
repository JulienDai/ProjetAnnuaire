

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

