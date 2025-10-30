import networkx as nx
import pandas as pd
import os

def sample_network():
    # Create a simple directed network with Purdue levels as 'level' attribute
    G = nx.DiGraph()
    # nodes: name, level, role
    nodes = [
        ('Enterprise-1', 4, 'Domain Controller'),
        ('DMZ-1', 3, 'Jump Host'),
        ('IT-Switch', 3, 'Switch'),
        ('Engineering-HMI', 2, 'HMI'),
        ('PLC-1', 1, 'PLC'),
        ('PLC-2', 1, 'PLC'),
        ('Historian', 2, 'Historian'),
    ]
    for n,level,role in nodes:
        G.add_node(n, level=level, role=role)
    # edges
    edges = [
        ('Enterprise-1','DMZ-1'),
        ('DMZ-1','Engineering-HMI'),
        ('Engineering-HMI','PLC-1'),
        ('Engineering-HMI','PLC-2'),
        ('IT-Switch','Enterprise-1'),
        ('PLC-1','Historian'), # intent: maybe questionable
        ('Enterprise-1','PLC-2'), # violation L4->L1
    ]
    for u,v in edges:
        G.add_edge(u,v)
    return G

def score_segmentation(G, annotations):
    # naive scoring: compute number of true violations (edges that jump levels more than 1)
    violations = []
    for u,v in G.edges():
        lu = G.nodes[u].get('level',2)
        lv = G.nodes[v].get('level',1)
        if abs(lu - lv) > 1:
            violations.append(f"{u}->{v}")
    user_violations = [a['edge'] for a in annotations if a.get('verdict')=='Yes']
    # compute precision-like metric
    true_set = set(violations)
    user_set = set(user_violations)
    tp = len(true_set & user_set)
    fp = len(user_set - true_set)
    fn = len(true_set - user_set)
    precision = tp / (tp+fp) if (tp+fp)>0 else 0.0
    recall = tp / (tp+fn) if (tp+fn)>0 else 0.0
    f1 = 2*precision*recall/(precision+recall) if (precision+recall)>0 else 0.0
    score_pct = f1*100
    return score_pct, {'true_violations':list(true_set), 'detected':list(user_set), 'tp':tp,'fp':fp,'fn':fn}

def sample_asset_csv(path='data/sample_assets.csv'):
    import pandas as pd
    rows = [
        {'name':'PLC-1','ip':'10.0.1.10','vendor':'VendorA','protocol':'Modbus','expected':'PLC'},
        {'name':'HMI-1','ip':'10.0.2.5','vendor':'VendorB','protocol':'OPC','expected':'HMI'},
        {'name':'Historian-1','ip':'10.0.3.20','vendor':'VendorC','protocol':'MQTT','expected':'Historian'},
        {'name':'TempSensor-1','ip':'10.0.4.8','vendor':'VendorD','protocol':'Proprietary','expected':'Sensor'},
    ]
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return path
