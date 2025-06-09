const analyzeButtonOne = document.getElementById("analyze-button-one");
const modal = document.getElementById("analysis-result-modal");
const modalText = document.getElementById("changed-result-text");
const closeButton = document.getElementById("close-button");

if(analyzeButtonOne){
    analyzeButtonOne.addEventListener("click", function(){
        //let url = 'http://localhost:8000/infer';
        let url = 'https://iotpacketpatrol.onrender.com/infer';
        fetch(url).then(response=>{
            return response.json();
        }).then(result=>{
            console.log("RESULT: ", typeof(result[0]));
            if(result[0]==0){
                modalText.textContent = "Your network activity seems to be normal.";
            }
            else if(result[0]==1){
                modalText.textContent = "Your network activity indicates a likely botnet attack.";
            }
            modal.style.display = "block";
        }).catch(error=>{
            console.log("ERROR: ", error);
            modalText.textContent = "Error analyzing input flow(s).";
            modal.style.display = "block";
        });
    });
}

if(closeButton){
    closeButton.addEventListener("click", function(){
        modal.style.display = "none";
    });
}

window.addEventListener("click", function(event){
    if(event.target===modal){
        modal.style.display="none";
    }
});