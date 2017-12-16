For instructions regarding how Themis works and how to interface with it, see Themis_README.md

Note however that Themis requires the presence of an xml file that denotes program specifications,
such as the program to execute, min samples, max samples, a random seed, and the name every 
attribute, its type and all possible values for that attribute. We wrote a script, "create_xml.py"
to facilitate the creation of these settings files. It should be invoked as follows: 

    python3 create_xml.py min_samples  max_samples  command  dataset  seed

where dataset is the file used to train the software/decision models in question