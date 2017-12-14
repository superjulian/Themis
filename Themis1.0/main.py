import math
import random
import sys
import xml.etree.ElementTree as ET
import Themis

def load_soft_from_settings():
    names={}
    types={}
    values={}
    num_values={}

    tree = ET.parse('new_settings.xml')
#     tree = ET.parse('settings.xml')
    root = tree.getroot()

    #software_name = root.find("name").text
    command = root.find("command").text
    maxSamples = root.find("max_samples").text
    minSamples = root.find("min_samples").text

    print minSamples

    inputs = root.find("inputs")
    random.seed(int(root.find("seed").text))

    for uid, obj in enumerate(inputs.findall("input")):
        names[uid] = obj.find("name").text
        types[uid] = obj.find("type").text
        if types[uid] == "categorical":
            values[uid] = [elt.text for elt in obj.find("values").findall("value")]
        elif types[uid] == "continuousInt":
            values[uid] = range(int(obj.find("bounds").find("lowerbound").text),
                                int(obj.find("bounds").find("upperbound").text))
        else:
            assert false
        num_values[uid] = len(values[uid])

    #print names
    #print values
    #print num_values
    #print command
    #print types

    soft = Themis.soft(names, values, num_values, command, types)
    soft.set_min_max(int(minSamples), int(maxSamples))

    return soft


if __name__ == '__main__':
    soft = load_soft_from_settings()
    soft.printSoftwareDetails()
    print soft.getComand()
    print soft.attr_names

    D = soft.discriminationSearch(0.2,0.80,0.1,"groupandcausal")

    print  "\n\n\nThemis has completed \n"
    print "Software discriminates against ", D
    # X=[7]
    X = [3]
    print soft.groupDiscrimination(X,.99,0.1)
    print soft.causalDiscrimination(X,.99,0.1)
    #print soft.getTestSuite()
