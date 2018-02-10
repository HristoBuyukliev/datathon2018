import pandas as pd


def read_data():
    """
    Reads the data, drops the Real_event flag 0 events and adds a new numerical column for the strength
    where High = 1, Medium = 0.5, Low = 0.25
    Then it groups by (from,to) and sums.
    :return:
    """
    df = pd.read_csv('/mnt/8C24EDC524EDB1FE/data/sna/Datathon_2018_Dataset_Hashbyte_New.csv',sep=';')
    df = df[df['Real_Event_Flag'] > 0]
    del df['Real_Event_Flag']
    strength_remap = {'High': 1, 'Medium': 0.5, 'Low': 0.25}
    df['strength'] = df['Label'].map(lambda x: strength_remap[x])
    combined = df.groupby(by=['Subscriber_A',"Subsciber_B"]).sum()
    return combined


def read_g5():
    return pd.read_csv('/mnt/8C24EDC524EDB1FE/data/sna/Node_5_Bad_nodes.csv')