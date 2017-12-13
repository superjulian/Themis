#We need, max_samples, min_samples, command, seed, file
import sys

def get_attributes(filename):
    attr_values = {}

    dataset = open(filename, 'r')
    attr_names = dataset.readline().strip().split(',')[:-1]
    first_line = dataset.readline().strip().split(',')[:-1]

    for i in range(len(attr_names)):
        print first_line[i]
        try:
            value = float(first_line[i])
            attr_values[attr_names[i]] = {'min' : sys.maxint, 'max' : 0}
        except:
            attr_values[attr_names[i]] = []

    dataset.seek(0)
    dataset.readline()

    for line in dataset:
        instance = line.strip().split(',')[:-1]
        for i in range(len(instance)):
            attribute = attr_names[i]
            if type(attr_values[attribute]) == list:
                if instance[i] not in attr_values[attribute]:
                    attr_values[attribute].append(instance[i])
            else:
                value = int(instance[i])
                if value < attr_values[attribute]['min']:
                    attr_values[attribute]['min'] = value
                if value > attr_values[attribute]['max']:
                    attr_values[attribute]['max'] = value

    return attr_names, attr_values

def write_inputs(f, attr_names, attr_values):
    for i in range(len(attr_names)):
        attribute = attr_names[i]
        f.write('\t\t<input>\n')
        f.write('\t\t\t<name>' + attribute + '</name>\n')
        if type(attr_values[attribute]) == list:
            f.write('\t\t\t<type>categorical</type>\n')
            f.write('\t\t\t<values>\n')
            for value in attr_values[attribute]:
                f.write('\t\t\t\t<value>' + value + '</value>\n')
            f.write('\t\t\t</values>\n')
        else:
            f.write('\t\t\t<type>continuousInt</type>\n')
            f.write('\t\t\t<bounds>\n')
            f.write('\t\t\t\t<lowerbound>' + str(attr_values[attribute]['min']) + '</lowerbound>\n')
            f.write('\t\t\t\t<upperbound>' + str(attr_values[attribute]['max']) + '</upperbound>\n')
            f.write('\t\t\t</bounds>\n')
        f.write('\t\t</input>\n')

def main():
    f = open('new_settings.xml', 'w+')
    f.write('<?xml version="1.0"?>\n')
    f.write('<settings>\n')
    f.write('\t<command>' + sys.argv[3] + '</command>\n')
    f.write('\t<seed>' + sys.argv[5] + '</seed>\n')
    f.write('\t<max_samples>' + sys.argv[2] + '</max_samples>\n')
    f.write('\t<min_samples>' + sys.argv[1] + '</min_samples>\n')
    f.write('\t<inputs>\n')

    attr_names, attr_values = get_attributes(sys.argv[4])
    print attr_names, attr_values
    write_inputs(f, attr_names, attr_values)

    f.write('\t</inputs>\n')
    f.write('</settings>')

    f.close()


main()
