function delete_element(sender){
    sender.remove();


}


function get_input() {
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

        add_element(name="TAF",input_taf)
    }

    if (input_stage!=""){
        add_element(name="Stage",input_stage)
    }
    if(input_entreprise!=""){
        add_element(name="Entreprise",input_entreprise)
    }
    if(input_promotion!=""){
        add_element(name="Promotion",input_promotion)
    }
}


function add_element(name,input){

         let ajout = document.getElementById('ajout');
        let ui = document.createElement('ui');
        ui.className = "filtre_element"


        let span = document.createElement("span");
        span.className = "filtres";
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








