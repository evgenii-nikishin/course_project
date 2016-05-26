import networkx as nx
import pandas as pd

#%% some function definitions

def read_nodeadjlist(filename):
    G = nx.Graph()
    for line in open(filename):
        e1, es = line.split(':')
        es = es.split()
        for e in es:
            if e == e1: continue
            G.add_edge(int(e1),int(e))
    return G

#%% set script params

submissionNumber = 123456

# folder paths
egonetFolderName = './egonets/'
submissionFolderName = ''

#%% make a submission

submission = pd.read_csv(submissionFolderName + 'sample_submission.csv')
for userId in list(submission['UserId']):

    print 'predicting for user ' + str(userId)

    # read graph
    filename = str(userId) + '.egonet'
    G = read_nodeadjlist(egonetFolderName + filename)

    # find the single most popular user
    rankDictionary = nx.pagerank(G)

    ranks = list(rankDictionary.values())
    nodes = list(rankDictionary.keys())

    maximumRankedNode = nodes[ranks.index(max(ranks))]

    # populate prediction string
    predictionString = str(maximumRankedNode)

    submission.ix[submission['UserId'] == userId,'Predicted'] = predictionString

submission.to_csv(submissionFolderName + str(submissionNumber) + '.csv', index=False)
