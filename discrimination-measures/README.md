The discrimination metrics outlined in the paper are entirely implemented within the Dataset class within ./discrimination/analyze.py. Any program that interfaces with this class should be in the same directory as the discrimination directory. To load the module, simply begin your program with: 

from discrimination import analyze

One constructs a new Dataset instance by calling

    analyzer = analyze.Dataset(file_name, benefit_values)
    
where benefit_values is a list of the possible values of the decision variable in the dataset. For example, for the Adult data set, benefit_values would be given as benefit_values = ["<=50k", ">50k"]

To calculate the group discrimination metrics with respect to a specified protected group, one calls

    analyzer.init_protected(protected_group)
    
where protected_group is a dictionary with protected attributes (eg. race) as keys and coorespondin gattribute values (e.g. "Black").

To calculate the consistency over the whole data set, call

    analyzer.get_consistency(k)
    
where k is the number of nearest neighbors to consider. 

To calculate the consistency over a randomly sampled subset of the data, call

    analyzer.get_consistency_subset(k, percentage, random_seed)
    
 Finally, to average the consistencies over a proscribed number of randomly sampled subsets, call
 
    analyzer.get_avg_consistency(num_samples, k, percentage)
    
For an example program interfacing with the class, see test.py

