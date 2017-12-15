import sys
import pandas as pd

def convert_file(file, num_columns, middle_vals):
    read_file = open(file, 'r')
    out_file = open('discretized-output', 'w+')
    out_file.write(read_file.readline())

    for line in read_file:
        line = line.strip().split(' ')
        instance = line[:-1]

        for num in num_columns:
            split = middle_vals[num]
            if int(instance[num]) <= split:
                val = "<=" + str(split)
            else:
                val = '>' + str(split)
            instance[num] = val

        for item in instance:
            out_file.write(item + ',')

        out_file.write(line[-1] + '\n')



def main():
    file = sys.argv[1]

    #df = pd.read_csv(file, skiprows=1, header=None)
    df = pd.read_table(file, sep=' ', skiprows=1, header=None)

    middle_vals = {}

    num_columns = [key for key in dict(df.dtypes) if dict(df.dtypes)[key] in ['float64', 'int64']]
    if (len(df.columns) - 1) in num_columns:
        num_columns.remove(len(df.columns) - 1)

    for column in num_columns:
        column_list = sorted(df[column].tolist())
        middle = column_list[int(len(df) / 2)]
        middle_vals[column] = middle

    print(middle_vals)
    convert_file(file, num_columns, middle_vals)

if (__name__ == "__main__"):
    main()