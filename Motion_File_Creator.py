import sys
import math
import random
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom


def motion_function(index):
    percentage = 100.0/2.0 * (1.0*(index-50)/(6.0 * math.sqrt(1 + math.pow(1.0*(index - 50.0)/6.0, 2)))) + 50.0
    return percentage/100.0


def create_steps(difference, start_value):
    steps = list(map(lambda x: x * difference + start_value, percentages))
    return steps


def create_time_steps(time_elapsed, intervals):
    stepsize = time_elapsed/intervals
    steps = [x * stepsize for x in range(0, intervals)]
    return steps


def create_mot_file(start_vector, end_vector, time_elapsed):
    # Get the joint differences
    differences = [(end - start) for (start, end) in zip(start_vector.joints, end_vector.joints)]
    # Get the position for each joint at the time steps
    steps = list(map(create_steps, differences, start_vector.joints))
    # Create timesteps
    timesteps = create_time_steps(time_elapsed, 100)
    # Begin writing.
    if not os.path.exists('Motion Files'):
        os.makedirs('Motion Files')
    # Set up
    number_of_files = len([name for name in os.listdir('./Motion Files')])
    motion_file = open('Motion Files\File_' + str(number_of_files+1) + '.mot', 'w')
    motion_file.write('Coordinates\n')
    motion_file.write('version=1\n')
    motion_file.write('nRows=100\n')
    motion_file.write('nColumns=12\n')
    motion_file.write('inDegrees=yes\n\n')
    motion_file.write('Units are S.I. units (second, meters, Newtons, ...)\n')
    motion_file.write('Angles are in degrees\n\n')
    motion_file.write('endheader\n')
    motion_file.write('time\tSC_y\tSC_z\tSC_x\tAC_y\tAC_z\tAC_x\tGH_y\tGH_z\tGH_yy\tEL_x\tPS_y\n')

    col_width = 15

    for index in range(0, 100):
        toWrite = "{:10.4}".format(timesteps[index]).ljust(col_width)
        for step in steps:
            toWrite += "".join("{:10.4}".format(step[index]).rjust(col_width))
        motion_file.write(toWrite + '\n')
    motion_file.close()
    create_XML_file(motion_file, 0, timesteps[-1])


def create_XML_file(mot_file, time_start, time_finish):
    if not os.path.exists('XML Files'):
        os.makedirs('XML Files')
    xml_file_name = 'XML Files\\' + os.path.basename(mot_file.name).split('.')[0] + ".xml"
    open_sim_document = ET.Element('OpenSimDocument', {"Version": str(20302)})
    inverse_dynamics_tool = ET.SubElement(open_sim_document, "InverseDynamicsTool", {"name": os.path.basename(mot_file.name).split('.')[0]})
    results_directory = ET.SubElement(inverse_dynamics_tool, "results_directory")
    results_directory.text = "../Inverse Dynamics Output"
    input_directory = ET.SubElement(inverse_dynamics_tool, "input_directory")
    model_file = ET.SubElement(inverse_dynamics_tool, "model_file")
    model_file.text = "../../das3.osim"
    time_range = ET.SubElement(inverse_dynamics_tool, "time_range")
    time_range.text = str(time_start) + "\t" + str(time_finish)
    forces_to_exclude = ET.SubElement(inverse_dynamics_tool, "forces_to_exclude")
    forces_to_exclude.text = "Muscles"
    external_loads_file = ET.SubElement(inverse_dynamics_tool, "external_loads_file")
    coordinates_file = ET.SubElement(inverse_dynamics_tool, "coordinates_file")
    coordinates_file.text = os.path.relpath(mot_file.name, "XML Files")
    output_gen_force_file = ET.SubElement(inverse_dynamics_tool, "output_gen_force_file")
    output_gen_force_file.text = os.path.basename(mot_file.name).split('.')[0] + ".sto"

    tree = ET.ElementTree(open_sim_document)
    tree.write(xml_file_name, xml_declaration=True, encoding='utf-8', method="xml")

    x = xml.dom.minidom.parse(xml_file_name)
    pretty_xml = x.toprettyxml()
    xml_file = open(xml_file_name, "w")
    xml_file.write(pretty_xml)

percentages = list(map(motion_function, range(0, 100)))


class MotionVector:
    def __init__(self, joints):
        self.joints = joints
        self.SC_y = joints[0]
        self.SC_z = joints[1]
        self.SC_x = joints[2]
        self.AC_y = joints[3]
        self.AC_z = joints[4]
        self.AC_x = joints[5]
        self.GH_y = joints[6]
        self.GH_z = joints[7]
        self.GH_yy = joints[8]
        self.EL_x = joints[9]
        self.PS_y = joints[10]

if __name__ == "__main__":
    # Get the command line arguments
    # Format: Motion_File_Creator.py SC_y, SC_z, SC_x, AC_y, AC_z, AC_x, GH_y, GH_z, GH_yy, EL_x, PS_y, SC_y, SC_z, SC_x, AC_y, AC_z, AC_x, GH_y, GH_z, GH_yy, EL_x, PS_y time_elapsed
    for i in range(1, 10000):
        arguments = [random.uniform(-60, -11), random.uniform(-5, 40), random.uniform(0, 85), random.uniform(30, 70), random.uniform(-20, 10), random.uniform(-20, 20), random.uniform(-180, 180), random.uniform(-20, 90), random.uniform(-180, 180), random.uniform(5, 140), random.uniform(5, 160),
                     random.uniform(-60, -11), random.uniform(-5, 40), random.uniform(0, 85), random.uniform(30, 70), random.uniform(-20, 10), random.uniform(-20, 20), random.uniform(-180, 180), random.uniform(-20, 90), random.uniform(-180, 180), random.uniform(5, 140), random.uniform(5, 160),
                     random.uniform(0, 5)]
        # Make sure that the number of arguments matches what is needed
        if len(arguments) != 23:
            print('Insufficient arguments')
        start_vector = MotionVector(arguments[0:11])
        end_vector = MotionVector(arguments[11:22])
        create_mot_file(start_vector, end_vector, arguments[22])
