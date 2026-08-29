"""
Speckle generator class. 
Uses matplotlib to generate speckle pattern. 

Code written by: Lavya
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import qmc
from PIL import Image as im
import os
import math

class generateSpeckle:

    def __init__(self, width, height, speckle_size, blackwhite, run, mode = 0, edgeclipping = False):

        """
        Class to generate speckle patterns. 

        Functions:
        generateSpecklePositions    --> Seeds the speckles.
        generateSpecklePattern      --> Creates the speckle pattern.
        visualizeSpecklePattern     --> Self explanatory.

        Inputs:
        width, height, speckle_size --> Dimensions specified by user.
        blackwhite                  --> Fraction of one colour to another.
        run                         --> Run number.
        mode                        --> Colour grading. 0 is black on white, 1 is white on black.
        edgeclipping                --> Flag to stop any fractional speckles being generated.
        """

        #Assign variables to self
        self.width = width
        self.height = height
        self.speckle_size = speckle_size
        self.blackwhite = blackwhite
        self.run = run
        self.mode = mode
        self.edgeclipping = edgeclipping

        #Colour information
        if mode == 1:
            self.specklecolor = "white"
            self.backgroundcolor = "black"
        elif mode == 0:
            self.specklecolor = "black"
            self.backgroundcolor = "white"
        else:
            raise ValueError("Mode value chosen is out of bounds. Chose either black on white or white on black!")

        #Generate speckle seeds.
        self.speckles = self.generateSpecklePositions()


    #### Speckle Position Generator ####
    def generateSpecklePositions(self):

        """
        generateSpecklePositions

        function to generate the positions of the speckles. 
        Uses halton sampling to create pointwise speckles, think of it as seed points. 

        Can also clip the upper and lower bounds to stop any fractional speckles from being generated.

        Outputs:
        speckles --> 2D array of X,Y coordinates for speckles.
        """

        #Calculate total area in pixels.
        area = self.width * self.height

        #Calculate area that needs to be spanned by the speckles
        self.speckle_radius = self.speckle_size/2
        self.speckle_area = np.pi * (self.speckle_radius ** 2)

        #Get the number of speckls needed
        n_speckles = (area * self.blackwhite) / self.speckle_area
        n_speckles = int(n_speckles) #Needs to be an integer

        #Create the halton sampler
        sampler = qmc.Halton(d = 2, optimization = "random-cd")
        if self.edgeclipping:
            speckles = sampler.integers(n = n_speckles, 
                                        l_bounds = [math.ceil(0 + 2 * self.speckle_radius), math.ceil(0 + 2 * self.speckle_radius)], 
                                        u_bounds = [int(self.width -  2 * self.speckle_radius), int(self.height -  2 *self.speckle_radius)])
        else:
            speckles = sampler.integers(n = n_speckles, l_bounds = [0,0], u_bounds = [self.width, self.height])

        #Console output
        print(f"Generated {n_speckles} speckle seeds.")

        return speckles #This gives the pointwise locations of the speckles


    #### Speckle Pattern Generator ####
    def generateSpecklePattern(self, subdivisions = 1):

        """
        generateSpecklePattern

        Takes pixel data from matplotlibs scatter to create a function for the speckle pattern. 
        White pixels have the value 255 while black have the value 0. 
        Can go to sub-pixel resolutions compared to the input pixel count.

        Inputs:
        subdivisions    --> How many splits inside a pixel are needed (resolution)

        Outputs:
        pattern         --> Dictionary containing all the information about the speckle pattern function
                            Can be fed into diagnostics.
        """

        #Calculate required DPI
        #For pattern creation: 500 pixels = 10 inches
        x_inches = self.width * (10/500)
        y_inches = self.height * (10/500)

        #For subpixel accuracy we need:
        target_pixels = self.width * subdivisions
        #This gives us a required ppi/dpi of:
        dpi = target_pixels/x_inches

        #Create matplotlib scatter plot
        fig, ax = plt.subplots()
        fig.set_figheight(y_inches)
        fig.set_figwidth(x_inches)
        fig.set_dpi(dpi)
        fig.patch.set_facecolor(self.backgroundcolor)
        ax.set_facecolor(self.backgroundcolor)
        ax.scatter(x = self.speckles[:,0], y = self.speckles[:,1], s = self.speckle_area, c = self.specklecolor)
        ax.set_xlim((0, self.width))
        ax.set_xscale("linear")
        ax.set_ylim((0, self.height))
        ax.set_xscale("linear")

        #Taking the pixel maps from matplotlib
        ax.axis('off')
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        fig.canvas.draw()

        w, h = fig.canvas.get_width_height()
        rgb_buffer = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        pixel_matrix_3d = rgb_buffer.reshape((h, w, 3))

        #Make the grids and the function.
        x = np.linspace(0, self.width, w)
        y = np.linspace(0, self.height, h)
        X,Y = np.meshgrid(x,y)
        dx = self.width/w
        dy = self.height/h

        f = pixel_matrix_3d[:, :, 0]

        #Save the X,Y grids and related information alongside the function f in a dictionary to send out.
        pattern = {"f" : f, "X" : X, "dx" : dx, "nx" : w, "Y" : Y, "dy" : dy, "ny" : h}

        #Console output
        print("Finished creating the speckle pattern.")

        return pattern


    #### Speckle Visualizer ####
    def visualizeSpecklePattern(self, visualize = True, save = True, filetype = ".tiff", ppi = 50):

        """
        visualizeSpecklePattern

        Function to visualize or save the speckle pattern. 
        Inputs:
        visualize   --> Flag for visualization
        save        --> Flag for saving
        filetype    --> Filetype, can be either ".tiff" or ".bmp"
        ppi         --> User specified pixels per inch if needed. Defaults to 50

        Outputs:
        Saved speckle pattern image for both visualization (with axes) and directly for printing.
        """

        #Get inch requirements:
        x_inches = self.width * (10/500)
        y_inches = self.height * (10/500)
        
        #Generate the pretty figure.
        fig, ax = plt.subplots()
        fig.set_dpi(ppi)
        fig.set_figheight(y_inches)
        fig.set_figwidth(x_inches)
        fig.patch.set_facecolor("white")
        ax.set_facecolor(self.backgroundcolor)
        ax.scatter(x = self.speckles[:,0], y = self.speckles[:,1], s = self.speckle_area, c = self.specklecolor)
        ax.set_xlim((0, self.width))
        ax.set_xscale("linear")
        ax.set_ylim((0, self.height))
        ax.set_xscale("linear")

        if save:
            #File names
            directory = "output/"+self.run+"/"
            save_path_axis = directory+self.run+"_SpecklePatternAxis"+filetype
            save_path_print = directory+self.run+"_SpecklePatternPrint"+filetype
            os.makedirs(directory, exist_ok = True)

            #Render image
            fig.canvas.draw()

            #Saving as a .tiff file
            image = im.frombytes("RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
            image.save(save_path_axis)

            #Turn axis off to save the printing
            ax.axis("off")
            fig.canvas.draw()

            image = im.frombytes("RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
            image.save(save_path_print)

            #Turn axis back on afterwards to see the proper pattern.
            ax.axis("on")
            ax.set_title(f"Speckle pattern for run: {self.run}")
            fig.canvas.draw()

            #Console output
            print(f"Speckle pattern saved as: {save_path_axis}")
            print(f"Pattern for printing saved as: {save_path_print}")

        if visualize:
            #Show image
            plt.show()
