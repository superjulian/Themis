import sys
import pickle
import copy

def extract_cr(k_rules, prot_attr, class_attr):
    PD, PND = {}, {}

    for k in range(2, len(k_rules)):
        for rule in k_rules[k]: #looping through every rule
            poten_rules = []
            for attr in rule: #checking if any of the attribute are the decision attribute
                if attr[0] == class_attr: #if attribute corresponds to class attribute
                    poten_rules.append(rule)
                    break
                    #rule_list = list(rule) #turn tuple into list
                    #pred = [x for x in rule_list if x[0] != class_attr] #take those values which don't correspond
                    #print(pred)
                    #print(rule_list)

                    #print(k_rules[k - 1][tuple(pred)])

            for rule in poten_rules:
                #print(rule)
                Y = list(rule)
                #print(Y)
                X = [x for x in Y if x[0] != class_attr]
                suppY = k_rules[k][rule][0]
                #print(suppY)
                #print(X)
                suppX = k_rules[k - 1][tuple(X)][0]
                conf = suppY / suppX
                #print(suppX)
                #print(conf)
                A = [x for x in X if x[0] in prot_attr]
                #print(A)
                group = len(X) - len(A)
                #print(group)
                if len(A) == 0:
                    if group in PND:
                        PND[group][tuple(Y)] = conf
                    else:
                        PND[group] = {tuple(Y) : conf}
                    #print("We are fucking saints")
                else:
                    #print("We are fucking discriminatory assholes")
                    if group in PD:
                        PD[group][tuple(Y)] = conf
                    else:
                        PD[group] = {tuple(Y) : conf}

                #print()

    return PD, PND

def check_alpha_pd(alpha, prot_attr, PD, PND):
    for group in PD:
        if group == 0:
            continue
        for rule in PD[group]:
            X = list(rule)
            B = [x for x in X if x[0] not in prot_attr]
            confX = PD[group][rule]
            confB = PND[group][tuple(B)]
            elift = confX / confB
            if max(elift, ((1 - confX) / (1 - confB))) >= alpha:
                for i in range(len(X) - 1):
                    print(X[i][0] + "=" + X[i][1] + ",", end = "")
                print("-> " + X[-1][1])



def main():
    if len(sys.argv) <= 1:
        print("Expected user input: (1) rules pickle file (2) protected attributes (3) Class variable")
        exit(1)

    pickle_file = open(sys.argv[1], 'rb')
    k_rules = pickle.load(pickle_file)

    protected_attr = set(sys.argv[2:-1])

    class_attr = sys.argv[-1]

    print(protected_attr)
    print(class_attr, '\n')

    PD, PND = extract_cr(k_rules, protected_attr, class_attr)

    check_alpha_pd(1.5, protected_attr, PD, PND)



if (__name__ == "__main__"):
    main()
