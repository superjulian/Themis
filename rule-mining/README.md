This folder contains programs for use in mining a data set for potential discrimination, in the form of 
discriminatory association rules. The methods we use draw from the sources cited in our paper. 
The process of mining for alpha-discriminatory rules using the programs in this folder involves several steps.

First, the algorithm we use for frequent itemset generation relies on the provided data set being composed of
uniquely categorical variables. This is an issue for our purposes, as both the Adult data set and the German Credit
data set contain numerial attributes. As such, we wrote a simple program, discretize.py, which takes numerical attributes
and converts them to a categorial variable corresponding to a binary split over a given threshold. This threshold is
chosen so half the data set will lie in each of the two "bins". To discretize a dataset, call

    python3 discretize.py file_name

which will output the discretized verion of the dataset to a file called "discretized-output". It is assumed that the 
binary class attribute is non-numerical as well. 

Having discretized the data set, the next step is to produce all frequent itemsets for the dataset in question. 
To do so, we used the implementation of the eclat algorithm within the arules package of R. To install this package, 
open RStudio and type
   
    install.packages("arules")

From here, load the csv file in question (we followed all these steps for the Adult data set) by entering

    Dataset  <- read.csv(file)

where file is either a file object a string representing the path to file. Having done this, mine the 
dataset for frequent items of size one by calling

    itemsets <- eclat(Dataset,
                  parameter = list(supp = x, maxlen = 1))

where x is the minimum desired support. To output these itemsets to file, run: 

    sink(filename)
    inspect(itemsets)
    sink()

This will save the itemsets to the file with path filename. Next mind the Dataset for all other itemsets
by calling

    itemsets <- eclat(Dataset,
                  parameter = list(supp = x, maxlen = total_num_items))


where we set the max length of any itemset to be the number of items in our dataset. Append these transactions
to the output file by calling

    sink(filename, append = TRUE)
    inspect(itemsets)
    sink()

This produces a file with all itemsets of minimum support x, outputted in a rather unhepful way. As such, we wrote
a program called parse_rules.py which takes the name of the file with the generated itemsets and converts them to 
lists of attribute-value tuples stored in a dictionary with their corresponding supports. This dictionary is 
then pickled for use in rule-mining. The rule parser can be called as

    python3 parse_rules.py rule_file


The final program, "discrim-search.py" is what mines the generated itemsets for the presence of alpha-discriminatory rules. It can be
invoked with: 

    python3 discrim-search.py pickle_file prot1 prot2 ... protn class_attr > adult-output

where pickle_file is the file with the pickled rules, class_atr is the name of the class attribute (eg. 'decision' in the
Adult data set), and the arguments in between denote all the protected attributes of interest (eg. 'race', 'sex', etc.).
