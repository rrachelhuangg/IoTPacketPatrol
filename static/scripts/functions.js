const analyzeButtonOne = document.getElementById("analyze-button-one");
const modal = document.getElementById("analysis-result-modal");
const modalText = document.getElementById("classification-result-text");
const catModalText = document.getElementById("category-result-text");
const subCatModalText = document.getElementById("subcategory-result-text");
const closeButton = document.getElementById("close-button");
const sampleButton = document.getElementById("sample-datasets");
const sampleModal = document.getElementById("sample-datasets-modal");
const sampleListText = document.getElementById("sample-datasets-list");
const closeSampleButton = document.getElementById("close-sample-button");
const loadDataset1 = document.getElementById("load-dataset-one");
const loadDataset2 = document.getElementById("load-dataset-two");
const loadDataset3 = document.getElementById("load-dataset-three");
const loadDataset4 = document.getElementById("load-dataset-four");
const loadDataset5 = document.getElementById("load-dataset-five");

if(loadDataset1){
    loadDataset1.addEventListener("click", async function(){
        try{
            const response = await fetch("/static/assets/datasets/generated_dataset_1.csv");
            const csvText = await response.text();
            const rows = csvText.trim().split("\n");
            const headers = rows[0].split(",");
            console.log("HEADERS: ", headers);
            const dataRow = rows[1].split(",");
            for(let i=0; i < headers.length; i++){
                const header = headers[i];
                const inputElement = document.getElementById(header);
                console.log("HERE: ", inputElement, headers[0]);
                if(inputElement){
                    inputElement.value = dataRow[i];
                }
            }
        }catch(error){
            console.log("ERROR");
        }
    });
}

if(loadDataset2){
    loadDataset2.addEventListener("click", async function(){
        console.log("CLICKED:");
        try{
            const response = await fetch("/static/assets/datasets/generated_dataset_2.csv");
            const csvText = await response.text();
            const rows = csvText.trim().split("\n");
            const headers = rows[0].split(",");
            console.log("HEADERS: ", headers);
            const dataRow = rows[1].split(",");
            for(let i=0; i < headers.length; i++){
                const header = headers[i];
                const inputElement = document.getElementById(header);
                console.log("HERE: ", inputElement, headers[0]);
                if(inputElement){
                    inputElement.value = dataRow[i];
                }
            }
        }catch(error){
            console.log("ERROR");
        }
    });
}

if(loadDataset3){
    loadDataset3.addEventListener("click", async function(){
        console.log("CLICKED:");
        try{
            const response = await fetch("/static/assets/datasets/generated_dataset_3.csv");
            const csvText = await response.text();
            const rows = csvText.trim().split("\n");
            const headers = rows[0].split(",");
            console.log("HEADERS: ", headers);
            const dataRow = rows[1].split(",");
            for(let i=0; i < headers.length; i++){
                const header = headers[i].replace(/\r$/, '');
                const inputElement = document.getElementById(header);
                console.log("HERE: ", inputElement, headers[0]);
                if(inputElement){
                    inputElement.value = dataRow[i];
                }
            }
        }catch(error){
            console.log("ERROR");
        }
    });
}

if(loadDataset4){
    loadDataset4.addEventListener("click", async function(){
        console.log("CLICKED:");
        try{
            const response = await fetch("/static/assets/datasets/generated_dataset_4.csv");
            const csvText = await response.text();
            const rows = csvText.trim().split("\n");
            const headers = rows[0].split(",");
            console.log("HEADERS: ", headers);
            const dataRow = rows[1].split(",");
            for(let i=0; i < headers.length; i++){
                const header = headers[i];
                const inputElement = document.getElementById(header);
                console.log("HERE: ", inputElement, headers[0]);
                if(inputElement){
                    inputElement.value = dataRow[i];
                }
            }
        }catch(error){
            console.log("ERROR");
        }
    });
}

if(loadDataset5){
    loadDataset5.addEventListener("click", async function(){
        console.log("CLICKED:");
        try{
            const response = await fetch("/static/assets/datasets/generated_dataset_5.csv");
            const csvText = await response.text();
            const rows = csvText.trim().split("\n");
            const headers = rows[0].split(",");
            console.log("HEADERS: ", headers);
            const dataRow = rows[1].split(",");
            for(let i=0; i < headers.length; i++){
                const header = headers[i];
                const inputElement = document.getElementById(header);
                console.log("HERE: ", inputElement, headers[0]);
                if(inputElement){
                    inputElement.value = dataRow[i];
                }
            }
        }catch(error){
            console.log("ERROR");
        }
    });
}

if(sampleButton){
    sampleButton.addEventListener("click", function(){
        sampleModal.style.display = "block";
    });
}

if(closeSampleButton){
    closeSampleButton.addEventListener("click", function(){
        sampleModal.style.display = "none";
    });
}

if(analyzeButtonOne){
    analyzeButtonOne.addEventListener("click", async function(){
        //let url = 'http://localhost:8000/infer_multi';
        //let url = 'http://localhost:8000/infer';
        //let url = 'https://iotpacketpatrol.onrender.com/infer';

        let url = 'https://iotpacketpatrol.onrender.com/infer_multi';

        const fieldIds = [
            "pkSeqID", "proto", "saddr", "sport", "daddr", "dport", "seq",
            "stddev", "N_IN_Conn_P_SrcIP", "min", "state_number", "mean", "N_IN_Conn_P_DstIP", 
            "drate", "srate", "max"
        ];

        const inputData = {};
        for(const id of fieldIds){
            const input = document.getElementById(id);
            if(input){
                inputData[id] = input.value;
            }
        }

        try{
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(inputData)
            });
            const result = await response.json();
            console.log("RESULT: ", result);
            if(result.attack==0){
                modalText.textContent = "Network Activity Classification: Benign";
                catModalText.textContent = "";
                subCatModalText.textContent = "";
            }
            else if(result.attack==1){
                modalText.textContent = "Network Activity Classification: Malicious";
                catModalText.textContent = "Category of Attack: " + result.category;
                subCatModalText.textContent = "Subcategory of Attack: " + result.subcategory;
            }
            modal.style.display = "block";
            catModalText.style.display="block";
            subCatModalText.style.display="block";
        }
        catch(error){
            console.log("ERROR: ", error);
            modalText.textContent = "Error analyzing input flow(s).";
            modal.style.display = "block";
        }
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
    else if(event.target==sampleModal){
        sampleModal.style.display="none";
    }
});