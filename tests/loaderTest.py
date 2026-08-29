"""
Code to test input file loader. 

Written by: Lavya
"""

import pytest
import src.configReader as reader

def testDefaults():

    """
    testDefaults

    Tests if an input file loads all the default values if no value is specified for that parameter. 
    Failing this could be quite problematic for the rest of the code so ensure it passes.
    """

    config = "tests/inputs/testDefaults.json"
    
    config_dict, visualize, save, filetype, subdivisions, mode, ppi, vis_diagnostics, save_diagnostics, edge = reader.configReader(config)

    assert visualize is True, "Default visualize should be True"
    assert save is True, "Default save should be True"
    assert filetype == ".tiff", f"Expected filetype '.tiff', got '{filetype}'"
    assert subdivisions == 1, f"Expected subdivisions 1, got {subdivisions}"
    assert mode == 0, f"Expected mode 0, got {mode}"
    assert ppi == 50, f"Expected ppi 50, got {ppi}"
    assert vis_diagnostics is True, "Default visualize_diagnostics should be True"
    assert save_diagnostics is True, "Default save_diagnostics should be True"
    assert edge is False, "Default edgeclipping should be False"

def testFullLoader():

    """
    testFullLoader

    Tests the read values against those in a known input deck to validate the loader.
    """

    config = "tests/inputs/testFullLoader.json"

    config_dict, visualize, save, filetype, subdivisions, mode, ppi, vis_diagnostics, save_diagnostics, edge = reader.configReader(config)

    assert visualize is False, f"Default visualize should be False, got {visualize}"
    assert save is False, f"Expected save should be False, got {save}"
    assert filetype == ".tiff", f"Expected filetype '.bmp', got '{filetype}'"
    assert subdivisions == 10, f"Expected subdivisions 10, got {subdivisions}"
    assert mode == 1, f"Expected mode 1, got {mode}"
    assert ppi == 100, f"Expected ppi 100, got {ppi}"
    assert vis_diagnostics is False, f"Default visualize_diagnostics should be false, got {vis_diagnostics}"
    assert save_diagnostics is False, f"save_diagnostics should be false, got {save_diagnostics}"
    assert edge is True, f"edgeclipping should be true, got {edge}"
    assert config_dict["run_name"] == "run1", f"Expected run name: run_1, got: {config_dict["run_name"]}"
    assert config_dict["case"] == 0, f"Expected case 0, got {config_dict["case"]}"
    assert config_dict["width"] == 500, f"Expected width 500px, got {config_dict["width"]}px"
    assert config_dict["height"] == 500, f"Expected height 500px, got {config_dict["height"]}px"
    assert config_dict["blackwhite"] == 0.10, f"Expected blackwhite 0.10, got {config_dict["blackwhite"]}"
    assert config_dict["speckle_size"] == 30, f"Expected speckle size of 30px, got {config_dict["speckle_size"]}px"
    assert config_dict["diagnostics"] is True, f"diagnostics should be true, got {config_dict["diagnostics"]}"

#Main block to call tests.
if __name__ == "__main__":
    print("Running tests for loader")
    testDefaults()
    testFullLoader()