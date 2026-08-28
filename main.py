import numpy as np
import src.configReader as reader
from src.generateSpeckle import generateSpeckle
from src.diagnostics import speckleDiagnostics
import argparse

#Console output
print(f"#### --- Speckle Generator Code --- ####")
print(f"####  ------ Made by Lavya ------   ####")

#Setup parser
parser = argparse.ArgumentParser(
    description = "Speckle Generator Code",
    epilog = "Created by Lavya"
)

#Add configuration file argument.
parser.add_argument("config", nargs="?", default = "input.json", help = "Configuration file")

#Parse terminal
args = parser.parse_args()

#Get the input deck.
config = args.config
print(f"Initialized code with input deck: {config}")

#Get the config file values from the reader
config_dict, visualize, save, filetype, subdivisions, mode, ppi, vis_diagnostics, save_diagnostics, edge = reader.configReader(config)

#Console outputs
print(f"Solving for run name: {config_dict["run_name"]}")
print(f"Required Speckle Pattern Dimensions:")
print(f"Width = {config_dict["width"]}")
print(f"Height = {config_dict["height"]}")
print(f"Colour grading mode: {mode}")

#Initialize the speckle generator class
speckleGenerator = generateSpeckle(
    width = config_dict["width"],
    height = config_dict["height"],
    blackwhite = config_dict["blackwhite"],
    speckle_size = config_dict["speckle_size"],
    run = config_dict["run_name"], 
    mode = mode, 
    edgeclipping = edge
)

#Generate speckle pattern.
specklePattern = speckleGenerator.generateSpecklePattern(subdivisions = subdivisions)

#Visualization
speckleGenerator.visualizeSpecklePattern(visualize = visualize, save = save, filetype = filetype, ppi = ppi)

#Control flows for diagnostics
if config_dict["diagnostics"]:
    print(f"Computing Speckle Pattern Diagnostics")

    #Initialize diagnostics class
    diagnostics = speckleDiagnostics(
        pattern = specklePattern, 
        width = config_dict["width"],
        height = config_dict["height"],
        run = config_dict["run_name"],
    )

    #Plot out the FFT
    diagnostics.visualizeFFT(visualize = vis_diagnostics, save = save_diagnostics)
    
else:
    print(f"Skipped Diagnostics")

#Final console output
print(f"Code finished running with no errors.")
