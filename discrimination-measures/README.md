The discrimination metrics outlined in the paper are entirely implemented within the Dataset class within ./discrimination/analyze.py. Any program that interfaces with this class should be in the same directory as the discrimination directory. To load the module, simply begin your program with: 

from discrimination import analyze

One constructs a new Dataset instance by calling

    analyze.Dataset(file_name, benefit_values)
    
where benefit_values is a list of the possible values of the decision variable in the dataset. For example, for the Adult data set, benefit_values would be given as benefit_values = ["<=50k", ">50k"]
