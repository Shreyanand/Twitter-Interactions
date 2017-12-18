from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
import operator
from scipy.stats import ttest_ind

def switch(label):
    if label == 0:
        return 1
    else:
        return 0

csvfile = open('/home/shrey/Desktop/Social Computing assignment 1/train.csv')
remove_head = csvfile.next().rstrip().split(',')

###################### GLOBAL VARIABLES #################################
Y_dic = {}
X_dic = {}

indexnumber = 1
G=nx.Graph()
loopcount = 0
repeatscount = 0
number_wrong = 0
correctjudge = 0
wrongjudge = 0
H_label = -1
data1 = []
data2 = []
H2data1 = []
H2data2 = []

#################### CONSTRUCTING GRAPH ###################################

for line in csvfile:
    s = line.rstrip().split(',')
    label = int(s[0])
    A_features = tuple([float(x) for x in s[1:12]])
    B_features = tuple([float(x) for x in s[12:]])
    
    if A_features not in X_dic:
        A_index = indexnumber
        G.add_node(A_index, Attributes = A_features)
        indexnumber = indexnumber + 1
        X_dic[A_features] = A_index
    else:
        A_index = X_dic[A_features]
    if B_features not in X_dic:
        B_index = indexnumber
        G.add_node(B_index, Attributes = B_features)
        indexnumber = indexnumber + 1
        X_dic[B_features]  = B_index
    else:
        B_index = X_dic[B_features]
        
    G.add_edge(A_index, B_index)

 ###################### HYPOTHESIS 1#######################################################    
    follower_A = G.node[A_index]['Attributes'][0]
    followee_A = G.node[A_index]['Attributes'][1]
    follower_B = G.node[B_index]['Attributes'][0]
    followee_B = G.node[B_index]['Attributes'][1]
    
    if followee_A != 0:
        ratio_A = follower_A / followee_A
    else:
        ratio_A = follower_A / (followee_A + 0.00001)
    if followee_B != 0:
        ratio_B = follower_B / followee_B
    else:
        ratio_B = follower_B / (followee_B + 0.00001)
    #print str(ratio_A) + " " + str(ratio_B)
    
    if ratio_B > ratio_A:
        H_label = 0
    else: 
        H_label = 1
    #print str(label) + " " + str(H_label)
    data1.append(H_label)
    data2.append(label)
    if H_label != label:
        wrongjudge = wrongjudge + 1
    if H_label == label:
        correctjudge = correctjudge + 1
        
######################### HYPOTHESIS 2 ############################################### 
    if B_index < A_index:
        temp = B_index
        B_index = A_index
        A_index = temp
        label = switch(label)
    if (A_index,B_index) not in Y_dic:
        Y_dic[(A_index,B_index)] = label
    else:
        repeatscount = repeatscount + 1
        H2data1.append(Y_dic[(A_index,B_index)])
        H2data2.append(label)
        if Y_dic[(A_index,B_index)] != label:
            number_wrong = number_wrong + 1
            if G.node[A_index]['Attributes'][0] == 209: #An example case
                print "a: " + str(G.node[A_index]['Attributes'])
                print "b: " + str(G.node[B_index]['Attributes'])
csvfile.close()    

lay = nx.spring_layout(G)
nx.draw_networkx_nodes(G,lay,node_color='b',alpha=0.2,node_size=5)
nx.draw_networkx_edges(G,lay,alpha=0.5)
plt.show()



a = nx.degree(G)
Cumdegree = 0
for key in a:
    Cumdegree = Cumdegree + a[key]
Average_degree = Cumdegree / G.number_of_nodes()

t, p = ttest_ind(data1, data2)  
t2, p2 =  ttest_ind(H2data1, H2data2)
    
print "Number of nodes: " + str(G.number_of_nodes())
print "Number of edges: " + str(G.number_of_edges())
print "Clustering Coefficient: " + str(nx.average_clustering(G))
print "Transitivity : " + str(nx.transitivity(G))
print "Density: " + str(nx.density(G))
print "Average Degree: " + str(Average_degree)
print "Most influential node betweeness: " + str(max(nx.betweenness_centrality(G).iteritems(), key=operator.itemgetter(1))[0]) + ": " + str(nx.betweenness_centrality(G)[329])  
print "Most influential node degree: " + str(max(nx.degree_centrality(G).iteritems(), key=operator.itemgetter(1))[0]) + ": " + str(nx.degree_centrality(G)[106])
print "Most degree: " + str(max(a.iteritems(), key=operator.itemgetter(1))[0]) + ": " + str(nx.degree(G)[106])
print "Percentage correct for H1: " + str(correctjudge / (wrongjudge + correctjudge))
print "Error Percentage for H2: " + str(number_wrong * 100 / repeatscount )
print "p value for H1: " + str(p)
print "p value for H2: " + str(p2)