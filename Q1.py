import pandas as pd
# import numpy as np


def xlsx_to_csv(file_name):
    data_xlsx = pd.read_excel(file_name, index_col=0)
    data_xlsx.to_csv(file_name[:-4]+"csv", encoding="utf-8")


if __name__ == "__main__":
    # xlsx_to_csv("Test_recommend_calculs.xlsx")
    # data = pd.read_csv("Test_recommend_calculs.csv")
    # df = data.drop(data.columns[[0, 1,-1,-2,-3,-4,-5]], axis=1)
    # df = df.drop([0,1,2,10,11,13])
    # df = df.reset_index(drop=True)
    # df.columns = ['Critics', 'Lady', 'Snakes', 'Luck', 'Superman', 'Dupree', 'Night']
    # df.to_csv("cleaned_data.csv")
    df = pd.read_csv("cleaned_data.csv")
    df = df.transpose()
    df = df.drop(['Unnamed: 0'])
    df = df.rename(columns=df.iloc[0])
    df = df.drop(df.index[0])
    # df.to_csv("rating.csv")
    Critiques = df.to_dict()
    print(Critiques['Lisa'])


