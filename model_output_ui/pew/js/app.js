let outputList = ["Gold Standard"];

function updateDisplay(dataObj) {
	let div = document.getElementById('outputs-div');
	$("#chart-img").attr("src", "");
	$("#chart-title").text("");
	$("#chart-id").text("");
	div.innerHTML = "";

	if (dataObj == null) {
		$("#chart-img").attr("src", "imgs/loading.gif");
		div.innerHTML = `<h2 class="ui red header">Error: Invalid chart number.</h2><br>`
		return;
	}

	$("#chart-img").attr("src", dataObj["img"]);
	
	// ID
	$("#chart-id").text(dataObj["File_No"].split(".txt")[0]);

	// Title
	$("#chart-title").text(dataObj["title"]);

	// OCR Text
	$("#ocr-text").html(dataObj["ocr-text"].replaceAll(" | ", "<br />"));

	// Model Outputs
	for (let i = 0; i < outputList.length; i++) {
		let key = outputList[i];

		let header = document.createElement("h2");
		header.innerText = key === "Gold Standard" ? key : key + " Output";

		let caption = document.createElement("div");
		caption.className = `ui ${key === "Gold Standard" ? "yellow" : "blue"} segment`;
		caption.innerText = dataObj[key];

		div.appendChild(header);
		div.appendChild(caption);
	}
};

$(function () {
	d3.csv("pew/outputs/output_files.csv").then(outputFiles => {
		for (let i = 0; i < outputFiles.length; i++) {
			outputList.push(outputFiles[i]["Name"]);
		}

		d3.csv("pew/outputs/combined.csv").then(outputData => {
			$("#chart-num").on("change input", e => {
				let i = $(e.target).val();
				updateDisplay(outputData[i]);
			});
	
			$("#chart-num").attr("max", outputData.length - 1);
			$("#chart-num").trigger("change");
	
			$("#random-button").click(() => {
				$("#chart-num").val(Math.floor(Math.random() * outputData.length));
				$("#chart-num").trigger("change");
			});
		});
	});
});
