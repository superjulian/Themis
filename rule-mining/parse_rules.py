import pickle
import sys

def clean_rules(rules, supports):

    new_rules = {}
    for i in range(len(rules)):
        rules[i] = rules[i].strip().replace('.', '-').split(',')
        for j in range(len(rules[i])):
            attr = rules[i][j].split('=')
            if '<' in attr:
                index = attr.index('<')
                attr.pop(index)
                attr[index] = "<=" + attr[index]

            rules[i][j] = (attr[0], attr[1])


        supports[i] = supports[i].strip().split(' ')
        if '' in supports[i]:
            supports[i].remove('')

        for j in range(len(supports[i])):
            if supports[i][j] == '':
                continue
            supports[i][j] = float(supports[i][j])

        new_rules[tuple(rules[i])] = supports[i]

    return new_rules

def split_by_length(rules):
    k_rules = {}

    for rule in rules:
        k = len(rule[0])
        if k in k_rules:
            k_rules[k].append(rule)
        else:
            k_rules[k] = [rule]

    return k_rules

def split_by_legnth_p(rules):
    k_rules = {}

    for rule in rules:
        k = len(rule)
        if k in k_rules:
            k_rules[k][rule] = rules[rule]
        else:
            k_rules[k] = {rule: rules[rule]}

    return k_rules

def main():
    file_name = sys.argv[1]
    file = open(file_name, 'r')
    file.readline()
    count = 0
    string = file.read()

    state = 0
    current_string = ""
    rules = []
    supp_count = []

    for char in string:
        if char == '[':
            state = 0
        elif char == ']':
            state = 1
        if (char == '\n' and state ==1) or (char == ' ' and state != 2) or state == 0:
            continue
        if char == '{':
            current_string = ""
            continue
        if char == '}':
            state = 2
            rules.append(current_string)
            current_string = ""
            continue
        if char == '\n' and state != 1:
            supp_count.append(current_string)
            current_string = ""

        current_string += char

    new_rules = clean_rules(rules, supp_count)

    k_rules = split_by_legnth_p(new_rules)


    picke_name = file_name + ".pickle"
    pickle_file = open(picke_name, 'wb')
    pickle.dump(k_rules, pickle_file)





if (__name__ == "__main__"):
    main()
