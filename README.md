# SensoriMotors
Approximate OpenSim's Inverse Dynamics using a Neural Network
Read report final_report.pdf

Tl;dr OpenSim has a tool called Inverse Dynamics. It receives a musculoskeletal model and a motion file and outputs the forces associated with each joint in the model. I use a Neural Network to try to approximate this computation.

## Motion_File_Creator.py
Creates random samples to give to the Inverse Dynamics tool. 
Generates some motion files and puts them in Motion Files directory along with an XML file in the XML Files directory

## Motion Files
Once created, the python script will store some random motion files in here along with an associated XML file in the XML Files directory.

## XML Files
Contains the XML files used for the inverse dynamics command from OpenSim. There is a batch script that will run the inverse dynamics command for every xml file in this directory. It will generate an sto file which is the output from the inverse dynamics tool for each input motion and put it in the Inverse Dynamics Output directory. (I moved some input output file pairs to the Data folder.)

## Inverse Dynamics Output
Contains output data from the inverse dynamics tool.

## Matlab directory
Stores the matlab code used to test train and validate the constructed neural network. Uses the files in the Motion Files and the files in the Inverse Dynamics Output directories for training and validation.

## Data
Stores extra data that can be used for the neural network training and validation if desired.




