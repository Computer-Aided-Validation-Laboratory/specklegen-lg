# specklegen-lg
Speckle pattern generator python package

## Brief description of usage
### Speckle pattern generation
Talk about the speckle pattern generation method here. 
<img width="885" height="883" alt="image" src="https://github.com/user-attachments/assets/56648e71-4b85-437d-b376-1e3d21dd546e" />

### Speckle pattern saving
Talk about how the code allows for the generated speckle pattern to be saved as a .tiff or .bmp file to prevent losses. Note that the .bmp case can be a bit weird sometimes so its best to diagnose it. 

Talk about how the speckle pattern is saved both for printing and for display. Printing dpi can be specified by the user.

### Diagnostics for the speckle pattern
Code can compute a FFT to look at the average speckle sizes. 
<img width="1000" height="1000" alt="run1_FFTDiagnostic" src="https://github.com/user-attachments/assets/8abf620e-abdf-4978-9f29-ded6c0e8d6ef" />


## Notes for Installation
First clone the repositiory.
_Add some code here to show how to clone the repository_

Then create a virtual environment for this project.
``python -m venv speckle``
Then activate the virtual environment.
``.\speckle\Scripts\Activate.ps1``

Then install the dependencies
``pip install -e.``

For this code to work the matplotlib version shouldn't be the latest one otherwise the saving mechanism will break.

## Using the code
You can run the code using: 
``python main.py input.json``
If no input file is entered then ``input.json`` is selected as the default. 
The code uses commentjson to make the input deck as instructive as possible.

## Testing for development
This code is compatible with pytest. 
To run a test script, just type into the terminal:
``python -m pytest tests/loaderTest.py``
from the main directory.
