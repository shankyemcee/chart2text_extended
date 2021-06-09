# Pew Model Output UI
- This folder contains the code for a website that displays the model outputs for test dataset in the Pew Research Dataset
- Currently, it contains the model outputs for BART and Chart-to-Text
- You can view the interface [here](https://rtkleong10-pew-model-outputs.herokuapp.com/)

## How to Run Locally
1. Unzip the `dataset.zip` file (if you haven't)
2. Install [Node](https://nodejs.org/en/)
3. Install the NPM package live-server: `npm install -g live-server`
4. `live-server .` (you only need to run this line after installing for the first time)

### Notes
- You can use other alternatives for hosting a local development server, but this is one of the simplest ways I've found
- A local development server is required to load the CSV files
- Alternatively, you can view the interface [here](https://rtkleong10-pew-model-outputs.herokuapp.com/)

## How to Add More Model Outputs
1. Unzip the `dataset.zip` file (if you haven't)
2. Change your directory to the `outputs/` folder: `cd outputs`
3. Generate a model output file
	1. Should contain only the generated captions with 1 caption per line
	2. The order of the generated captions should match the order of the charts in the `mappings/test_index_mapping.csv` file
4. Add your model output file into the `outputs/` folder
5. For the chart2text model only, to reorder the outputs to match the `mappings/test_index_mapping.csv` file
	3. Name the output file as `chart2text_reodered.txt`
	4. `python reorder_chart2text.py`
6. Add your model's name and filename to the `outputs/output_files.csv` file
7. Update the `outputs/combined.csv` file: `python generate_csv.py`
