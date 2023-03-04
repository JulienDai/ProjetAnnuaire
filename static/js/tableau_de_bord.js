let filtre_entreprise=[]
let filtre_stage=[]
let filtre_promotion=[]
let filtre_taf=[]


function delete_element(sender){

    if(sender.id=="TAF"){
        filtre_taf=filtre_taf.filter(element => element !== sender.getElementsByClassName("filtres")[0].id)

    }
    if(sender.id=="Stage"){
        filtre_stage=filtre_stage.filter(element => element !== sender.getElementsByClassName("filtres")[0].id)
    }
    if(sender.id=="Entreprise"){
         filtre_entreprise=filtre_entreprise.filter(element => element !== sender.getElementsByClassName("filtres")[0].id)
    }
    else{
        filtre_promotion=filtre_promotion.filter(element => element !== sender.getElementsByClassName("filtres")[0].id)
    }


    sender.remove();
}


function get_input() {
    filter_Alumni()
    let taf=document.getElementById("input_taf")
    let input_taf = taf.value;
    taf.value=""

    let stage=document.getElementById("input_stage")
    let input_stage = stage.value;
    stage.value="";

    promotion=document.getElementById("input_promotion")
    let input_promotion = promotion.value;
    promotion.value="";

    let entreprise=document.getElementById("input_entreprise")
    let input_entreprise = entreprise.value;
    entreprise.value="";


    if (input_taf != "") {
        filtre_taf.push(input_taf);

        add_element(name="TAF",input_taf);
    }

    if (input_stage!=""){
        filtre_stage.push(input_stage);
        add_element(name="Stage",input_stage);
    }
    if(input_entreprise!=""){
        filtre_entreprise.push(input_entreprise);
        add_element(name="Entreprise",input_entreprise);
    }
    if(input_promotion!=""){
        filtre_promotion.push(input_promotion);
        add_element(name="Promotion",input_promotion);
    }
}

//fonction juste pour l'affichage
function add_element(name,input){

         let ajout = document.getElementById('ajout');
        let ui = document.createElement('ui');
        ui.className = "filtre_element"
        ui.id=name;



        let span = document.createElement("span");
        span.className = "filtres";
        span.id=input;
        span.appendChild(document.createTextNode(name+": " + input));
        let button = document.createElement("button");
        button.className = "button_supprimer";



        let img = document.createElement("img");
        img.src = "/static/img/croix.png"
        img.className = "supprimer"

        button.appendChild(img)
        span.appendChild(button)



        button.onclick=function(){delete_element(ui)};
        ui.appendChild(span);
        ajout.appendChild(ui);
}

function filter_Alumni(){
   let alumnis= document.getElementsByClassName("someone_li")

   for (let i = 0; i < alumnis.length; i++){

        let almuni=alumnis[i];
        console.log(almuni);

       if(filtre_taf!==[] && !(filtre_taf.includes(almuni.querySelector("#taf_2A").innerHTML) || filtre_taf.includes(almuni.querySelector("#taf_3A").innerHTML ))){
          console.log("ouiii")
           almuni.style.display="none";
       }

       if(filtre_promotion!==[] && (filtre_promotion.includes(almuni.querySelector("#promotion").value))){
           almuni.style.display="none";
       }
       if(filtre_stage!==[] && (filtre_stage.includes(almuni.querySelector("#stage").value))){
           almuni.style.display="none";
       }

       if(filtre_entreprise!==[] && (filtre_entreprise.includes(almuni.querySelector("#entreprise").value))){
           almuni.style.display="none";
       }





   }

}








