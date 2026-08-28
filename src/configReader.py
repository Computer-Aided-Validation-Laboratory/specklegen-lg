import commentjson

def configReader(config):

    """
    configReader

    Reads config json files and outputs the dictionary.
    Has control flows to resort to example input decks. 
    It also regulates the None values from the input deck for optional inputs.

    Inputs:
    config  --> Configuration file name.

    Outputs:
    config_dict --> All the variables specified by the user. 
    """

    #Load the json file with comment json.
    with open(config, "r") as file:
        config_dict = commentjson.load(file)

    case = config_dict["case"]

    #Control flows for loading different examples, cases.
    if case == 1:
        print(f"Example case {case} found. Overwritting input deck")

        example_file = "examples/test_square.json"

        with open(example_file, "r") as file:
            config_dict = commentjson.load(file)
        print(f"Loaded input deck: {example_file}")
    elif case == 2:
        print(f"Example case {case} found. Overwritting input deck")

        example_file = "examples/test_rectangle.json"

        with open(example_file, "r") as file:
            config_dict = commentjson.load(file)
        print(f"Loaded input deck: {example_file}")
    elif case ==0:
        config_dict = config_dict
    else:
        raise ValueError("Wrong case selected. Review config file!")

    #For important variables, raise errors:
    if config_dict.get("width") is None:
        raise ValueError("Width is missing from input deck.")
    if config_dict.get("height") is None:
        raise ValueError("Height is missing from input deck.")
    if config_dict.get("speckle_size") is None:
        raise ValueError("Speckle size is missing from input deck.")
    if config_dict.get("blackwhite") is None:
        raise ValueError("Black White Ratio is missing from input deck.")
    if config_dict.get("run_name") is None:
        raise ValueError("Run name is missing from input deck.")
    if config_dict.get("diagnostics") is None:
        raise ValueError("Diagnostics is missing from input deck.")

    #Optional variables for plotting
    visualize = config_dict.get("visualize")
    save = config_dict.get("save")
    filetype = config_dict.get("filetype")
    ppi = config_dict.get("ppi")

    #If plotting variables are none then set them to defaults
    if visualize is None:
        visualize = True
    if save is None:
        save = True
    if filetype is None:
        filetype = ".tiff"
    if ppi is None:
        ppi = 50

    #Optional variables for speckle pattern generation
    subdivisions = config_dict.get("subdivisions")

    #Fallback against none values.
    if subdivisions is None:
        subdivisions = 1

    #Get colour mode data
    mode = config_dict.get("mode")

    #Fallback against none values.
    if mode is None:
        mode = 0

    #Get diagnostics flags
    vis_diagnostics = config_dict.get("visualize_diagnostics")
    save_diagnostics = config_dict.get("save_diagnostics")

    #Control flows for default setting.
    if vis_diagnostics is None:
        vis_diagnostics = True
    if save_diagnostics is None:
        save_diagnostics = True

    #Edge-clipping
    edge = config_dict.get("edgeclipping")

    #Default edge clipping is false
    if edge is None:
        edge = False

    return config_dict, visualize, save, filetype, subdivisions, mode, ppi, vis_diagnostics, save_diagnostics, edge
