This folder contains the code for a neural network classifier that can interface with Themis. Two programs 
are used for this. The first, nn.py, trains the a simple, fully connected network with a single hidden layer on 
a specified data set. The data set is assumed to be a csv file, with the class variable as the first entry. 
The program builds a model and pickles it for later use. The training program should be called as

    python3 nn.py data_file.csv neuron_number iterations percentage seed

where iterations denotes the number of executions of backpropogation, percentage is the decimal fraction
indicating how much of the data set to use for training, and seed is any integer. 

The second program, neural.py, uses this model to predict the class of an inputted instance. It pickle loads
the model created in nn.py. The name of this model should be the first command line argument. The program is written
to interface with Themis. That is, it is meant to handle any command line call of the form

   python3 neuron.py pickle_file.pickle THEMIS INPUT

where THEMIS INPUT is as specified in the read me file in the Themis1.0 directory and in our paper. 