"""
Code to check speckle pattern quality. 
Currently has one diagnostic: FFT to check average speckle size.

Code written by: Lavya
"""

import numpy as np
import scipy.fft as fft
import matplotlib.pyplot as plt
import os

class speckleDiagnostics():

    def __init__(self, pattern, width, height, run):

        """
        speckleDiagnostics

        Class to compute various diagnostics with the speckle pattern. 
        Functions:
        fourierTransformer      --> Computes a FFT for the speckle pattern. 
        visualizeFFT            --> Plots the FFT for visualization

        Inputs:
        pattern                 --> Dictionary containing the speckle pattern. 
        width, height           --> Dimensions specified by user.
        run                     --> Run name.
        """

        #Assigning variables to self.
        self.pattern = pattern
        self.width = width
        self.height = height
        self.run = run

        #Extracting arrays from pattern dictionary
        f = self.pattern["f"]
        nx = self.pattern["nx"]
        ny = self.pattern["ny"]
        dx = self.pattern["dx"]
        dy = self.pattern["dy"]

        #Fourier transform
        self.amplitudes, self.f_x, self.f_y = self.fourierTransformer(f, nx, dx, ny, dy)


    #### Fourier Transformer #####
    def fourierTransformer(self, f, nx, dx, ny, dy):

        """
        fourierTransformer

        Function to compute the FFT for the speckle pattern. 
        Acts as a diagnostic to check average speckle choice although can get a bit inaccurate for tiny speckles. 

        Inputs:
        f       --> Speckle Pattern
        nx      --> Number of x points
        dx      --> Distance b/w x points (uniform)
        ny      --> Number of y points
        dy      --> Distance b/w y points (uniform)

        Outputs:
        amplitudes, frequencies
        """

        #Fourier transforming
        fft_complex = fft.fft2(f)

        #Get frequencies
        freq_x = fft.fftfreq(nx, dx)
        freq_y = fft.fftfreq(ny, dy)

        mask_x = freq_x > 0
        mask_y = freq_y > 0

        f_x, f_y = np.meshgrid(freq_x[mask_x], freq_y[mask_y])

        #Amplitudes
        amplitudes = (1 / (nx * ny)) * np.abs(fft_complex)
        amplitudes = amplitudes[mask_y,:]
        amplitudes = amplitudes[:,mask_x]

        #Sizes
        f_x = (1/f_x) * dx 
        f_y = (1/f_y) * dy

        return amplitudes, f_x, f_y


    #### FFT Visualizer ####
    def visualizeFFT(self, visualize = True, save = True):

        """
        visualizeFFT

        Function to visualize the computed FFT diagnostic. 
        Inputs:
        visualize   --> Flag to visualize the FFT
        save        --> Flag to save the FFT

        Outputs:
        Saved FFT.
        """

        #Generate pretty figure
        plt.figure(figsize=(10,10))
        plt.title("Fast Fourier Transform of the Speckle Pattern")
        plt.pcolormesh(self.f_x, self.f_y, self.amplitudes)
        plt.colorbar()
        plt.xscale("log")
        plt.yscale("log")
        plt.ylabel("y-pixel sizes (height)")
        plt.xlabel("x-pixel sizes (width)")

        #Control flows for saving.
        if save:
            #File names
            directory = "output/"+self.run+"/"
            save_path = directory+self.run+"_FFTDiagnostic.png"
            os.makedirs(directory, exist_ok = True)

            #Save figuer
            plt.savefig(fname = save_path)

            #Console outputs
            print(f"Saved FFT Diagnostic to: {save_path}")

        #Control flows for visualization
        if visualize:
            plt.show()
