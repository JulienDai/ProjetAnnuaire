let filtre_entreprise=[]
let filtre_stage=[]
let filtre_promotion=[]
let filtre_taf=[]

//alumni doit être l'element html de classe someone_li
function vue_moins(alumni){

      const ul= document.querySelector(".everyone");

      ul.style.removeProperty("display")
        ul.style.removeProperty("justifyContent")
    alumni.style.removeProperty("textAlign")





        const button_moins=alumni.querySelector("#button_moins");
        const button_plus=alumni.querySelector("#button_plus");

        button_moins.style.display='none';
        button_plus.style.display='block';



        reset_affichage();
        const toshow=alumni.querySelector("#to_show");
        console.log(toshow);
        toshow.style.display="none";
        const set_width=alumni.getElementsByClassName("someone")[0];
        set_width.style.width="200px";

}
//alumni doit être l'element html de classe someone_li
function vue_plus(alumni){

    console.log(alumni)

    supress_every_element_affichage()
    const button_moins=alumni.querySelector("#button_moins");
    const button_plus=alumni.querySelector("#button_plus");
    button_moins.style.display='block';
    button_plus.style.display='none';


    const ul= document.querySelector(".everyone");
    ul.style.display="flex";
    ul.style.justifyContent="center"

    alumni.style.textAlign="center";

    alumni.style.display='inline-block'

    const toshow=alumni.querySelector("#to_show");
    toshow.style.display="block";
     const set_width=alumni.getElementsByClassName("someone")[0];
        set_width.style.width="auto";

}



console.log("yeppa");

window.addEventListener('DOMContentLoaded', function() {

    let alumnis = document.getElementsByClassName("someone_li")
    console.log(alumnis)

    for (let i = 0; i < alumnis.length; i++) {
        console.log("vu_moins")
        vue_moins(alumnis[i]);

    }
});




function delete_element(sender){

    //supprime les filtres des fonctions filtre_entreprise, filtre_stage , filtre_promotion et filtre_taf

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

    sender.remove(); // permet de supprimer le bouton

    reset_affichage()




}

function reset_affichage(){
      const ul= document.querySelector(".everyone");

      ul.style.removeProperty("display")
        ul.style.removeProperty("justifyContent")
    let alumnis= document.getElementsByClassName("someone_li")
    for (let i = 0; i < alumnis.length; i++){
        alumnis[i].style.removeProperty("textAlign")

        alumnis[i].style.display="inline-block";

    }
    filter_Alumni()
}

function supress_every_element_affichage(){
    let alumnis= document.getElementsByClassName("someone_li")
    for (let i = 0; i < alumnis.length; i++){

        alumnis[i].style.display="none";
    }


}




function get_input() {

    let taf=document.getElementById("input_taf")
    let input_taf = taf.value;
    console.log(input_taf)
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
    filter_Alumni()
}

//fonction pour créer l'affichage graphique du filtre
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


//permet de ne plus afficher l'alumni si il ne fait plus parti des filtres
function filter_Alumni(){
   let alumnis= document.getElementsByClassName("someone_li")

   for (let i = 0; i < alumnis.length; i++){

        let almuni=alumnis[i];

        almuni.style.display="inline-block"


      let  taf=almuni.querySelectorAll("#taf")

       let taf0;
      let taf1;
       if (taf.length>=2){
         taf0=taf[0].innerHTML;
         taf1=taf[1].innerHTML;
       }
       else if(taf.length==1){
          taf0=taf[0].innerHTML;
         taf1=null;
       }
       else{
           taf0=null;
           taf1=null;
       }


       if((filtre_taf.length!=0) && !(filtre_taf.includes(taf0) || filtre_taf.includes(taf1 ))){

           almuni.style.display="none";


       }



       if((filtre_promotion.length!=0) && !(filtre_promotion.includes(almuni.querySelector("#promotion").innerHTML.toString()))){
           almuni.style.display="none";
       }

      let keep_stage=filtre_stage.length==0;

       let stages = almuni.querySelectorAll("#stage")
       for (const stage of stages){
           if(keep_stage){
               break
           }
           keep_stage=filtre_stage.includes(stage.innerHTML);
       }

       if(!keep_stage){
           almuni.style.display="none";
       }

        let positions =almuni.querySelectorAll("#position");

        let keep_position=filtre_entreprise.length==0; //permet de ne pas filter si il n'y à pas d'entreprise sélectionné
       for (const position of positions){
            if (keep_position){
               break;
           }

           keep_position=filtre_entreprise.includes(position.innerHTML);

       }
       if(!keep_position){
           almuni.style.display="none";
       }


   }

}








