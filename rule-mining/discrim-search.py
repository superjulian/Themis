import sys
import pickle
import copy

#method to extract association rules from frequent item sets
def extract_cr(k_rules, prot_attr, class_attr):
    PD, PND = {}, {}

    for k in range(2, len(k_rules)):
        poten_rules = []
        for rule in k_rules[k]: #looping through every rule
            for attr in rule: #checking if any of the attribute are the decision attribute
                if attr[0] == class_attr: #if attribute corresponds to class attribute
                    poten_rules.append(rule) #add rule to set of valid rules
                    break

        for rule in poten_rules:
            Y = list(rule)
            X = [x for x in Y if x[0] != class_attr] #left hand side of rule
            suppY = k_rules[k][rule][0] #support of X -> C
            suppX = k_rules[k - 1][tuple(X)][0] #support of X
            conf = suppY / suppX
            A = [x for x in X if x[0] in prot_attr] #largest subset of discriminatory items
            group = len(X) - len(A)
            if len(A) == 0:
                if group in PND: #if no discriminatory items, potentially non-discriminatory rule
                    PND[group][tuple(Y)] = conf
                else:
                    PND[group] = {tuple(Y) : conf}
            else: #otherwise, potentially discriminatory
                if group in PD:
                    PD[group][tuple(Y)] = conf
                else:
                    PD[group] = {tuple(Y) : conf}

    return PD, PND

#Method to output any rules that are alpha discriminatory
def check_alpha_pd(alpha, prot_attr, PD, PND):
    f = open("discrim-rules.txt", "w+")
    count = 0 #count of outputted rules
    for group in PD:
        if group == 0:
            continue
        for rule in PD[group]:
            X = list(rule)
            B = [x for x in X if x[0] not in prot_attr] #non-discrimatory subset of rule
            confX = PD[group][rule]
            confB = PND[group][tuple(B)]
            elift = confX / confB #calculate elift from confidences of each rule
            if confB != 1 and max(elift, ((1 - confX) / (1 - confB))) >= alpha:
                f.write("[" + str(count) + "]  " )
                for i in range(len(X) - 1):
                    f.write(X[i][0] + "=" + X[i][1] + ",")
                f.write("-> " + X[-1][1] + "\n")

                count += 1



def main():
    if len(sys.argv) <= 1:
        print("Expected user input: (1) rules pickle file (2) alpha (3) protected attributes (4) Class variable")
        exit(1)

    pickle_file = open(sys.argv[1], 'rb')
    k_rules = pickle.load(pickle_file)

    alpha = sys.argv[2]

    protected_attr = set(sys.argv[3:-1])

    class_attr = sys.argv[-1]

    PD, PND = extract_cr(k_rules, protected_attr, class_attr)

    check_alpha_pd(3, protected_attr, PD, PND)



if (__name__ == "__main__"):
    main()
