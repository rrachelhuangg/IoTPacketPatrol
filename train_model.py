#logistic regression for binary classification of flows
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import ipaddress

#call list_flows endpoint and iterate thorugh it for the inner func of the wrapper func
def get_flows(method='get', data=None, headers=None):
    #call the list_flows endpoint. each element in the list is a flow dict
    url = 'http://localhost:8000/flows/'
    response = requests.request(method, url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def parse_flows(flows):
    x, y = [], []
    for f in flows:
        attributes = []
        attributes += [f['pkSeqID']]
        attributes += [f['proto']]
        attributes += [f['saddr']]
        attributes += [f['sport']]
        attributes += [f['daddr']]
        attributes += [f['dport']]
        attributes += [f['seq']]
        attributes += [f['stddev']]
        attributes += [f['N_IN_Conn_P_SrcIP']]
        attributes += [f['min']]
        attributes += [f['state_number']]
        attributes += [f['mean']]
        attributes += [f['N_IN_Conn_P_DstIP']]
        attributes += [f['drate']]
        attributes += [f['srate']]
        attributes += [f['max']]
        attributes += [f['category']]
        attributes += [f['subcategory']]
        x += [attributes]
        y += [f['attack']]
    return x, y

def one_hot_encode(x):
    #one hot encode categorical columns of independent variables and return as a list
    data = {}
    for i in range(18): #attributes
        data['pkSeqID'] = []
        data['proto'] = []
        data['saddr'] = []
        data['sport'] = []
        data['daddr'] = []
        data['dport'] = []
        data['seq'] = []
        data['stddev'] = []
        data['N_IN_Conn_P_SrcIP'] = []
        data['min'] = []
        data['state_number'] = []
        data['mean'] = []
        data['N_IN_Conn_P_DstIP'] = []
        data['drate'] = []
        data['srate'] = []
        data['max'] = []
        data['category'] = []
        data['subcategory'] = []
        for j in x: #row in x_data
            data['pkSeqID'] += [j[0]]
            data['proto'] += [j[1]]
            data['saddr'] += [j[2]]
            data['sport'] += [j[3]]
            data['daddr'] += [j[4]]
            data['dport'] += [j[5]]
            data['seq'] += [j[6]]
            data['stddev'] += [j[7]]
            data['N_IN_Conn_P_SrcIP'] += [j[8]]
            data['min'] += [j[9]]
            data['state_number'] += [j[10]]
            data['mean'] += [j[11]]
            data['N_IN_Conn_P_DstIP'] += [j[12]]
            data['drate'] += [j[13]]
            data['srate'] += [j[14]]
            data['max'] += [j[15]]
            data['category'] += [j[16]]
            data['subcategory'] += [j[17]]
    df = pd.DataFrame(data)
    
    categorical_columns = ['proto', 'category', 'subcategory']
    encoder = OneHotEncoder(sparse_output=False)
    one_hot_encoded =  encoder.fit_transform(df[categorical_columns])
    one_hot_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(categorical_columns))
    df_encoded = pd.concat([df, one_hot_df], axis=1)
    df_encoded = df_encoded.drop(categorical_columns, axis=1)

    dataframe = process_ip_cols(df_encoded)

    x_vals = []
    for index, row in dataframe.iterrows():
        x_vals += [row]

    return x_vals

def process_ip_cols(df):
    ip_vals_one = df['saddr']
    ip_vals_two = df['daddr']
    ip_vals_one_ints, ip_vals_two_ints = [], []
    j = 0
    for i in ip_vals_one:
        ip_vals_one_ints += [int(ipaddress.ip_address(i))]
        ip_vals_two_ints += [int(ipaddress.ip_address(ip_vals_two[j]))]
        j += 1
    df['saddr'] = ip_vals_one_ints
    df['daddr'] = ip_vals_two_ints

    sport_vals = df['sport']
    dport_vals = df['dport']
    sport_vals_ints, dport_vals_ints = [], []
    x = 0
    for i in sport_vals:
        if "x" in str(i):
            sport_vals_ints += [int(i, 16)]
        else:
            sport_vals_ints += [i]
    for b in dport_vals:
        if "x" in str(b):
            dport_vals_ints += [int(i, 16)]
        else:
            dport_vals_ints += [i]
    df['sport'] = sport_vals_ints
    df['dport'] = dport_vals_ints
    return df

def train():
    X_init, y = parse_flows(get_flows())
    X = one_hot_encode(X_init)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.fit_transform(X_test)
    model = LogisticRegression(random_state=42)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print(f"Confusion Matrix: {conf_matrix}")
    print(f"Classification report: {class_report}")

train()