import pandas, keras
import seaborn as sns
import matplotlib.pyplot as plt


def norm_split(dataset):
    #do normalization of x
    
    #one hot encoding of y

    #split it to y and x
    return dataset

#load table
df = pandas.read_csv("modSel2.csv")
#split to train a nd test
train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset = dataset.drop(train_dataset.index)



