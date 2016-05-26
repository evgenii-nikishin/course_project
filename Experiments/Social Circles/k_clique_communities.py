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

# params
cliqueSize = 5
tooLittleFriendsInCircleThreshold = 10
tooManyNodesThreshold = 220
submissionNumber = 1

# folder paths
egonetFolderName = './egonets/'
submissionFolderName = ''

#%% make a submission

submission = pd.read_csv(submissionFolderName + 'sample_submission.csv')
for userId in list(submission['UserId']):

    # read graph
    filename = str(userId) + '.egonet'
    G = read_nodeadjlist(egonetFolderName + filename)

    # do not calculate for large graphs (it takes too long)
    if len(G.nodes()) > tooManyNodesThreshold:
        print 'skipping user ' + str(userId)
        continue
    else:
        print 'predicting for user ' + str(userId)

    # find comunities using k_clique_communities()
    listOfCircles = []
    kCliqueComunities = list(nx.k_clique_communities(G,cliqueSize))
    for community in kCliqueComunities:
        # leave only relativly large communities
        if len(community) >= tooLittleFriendsInCircleThreshold:
            listOfCircles.append(list(community))

    # populate prediction string
    predictionString = ''
    for circle in listOfCircles:
        for node in circle:
            predictionString = predictionString + str(node) + ' '
        predictionString = predictionString[:-1] + ';'
    predictionString = predictionString[:-1]

    # if no prediction was created, use 'all friends in one circle'
    if len(listOfCircles) > 0:
        submission.ix[submission['UserId'] == userId,'Predicted'] = predictionString

submission.to_csv(submissionFolderName + str(submissionNumber) + '.csv', index=False)
