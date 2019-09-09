# Author:  Sanchita Rastogi
# ID: 10439951
# Subject: Online Social Networks

# Read the file from the terminal,  python3   triads.py   --filename   epinions69.csv
# Install tabulate library: Type command, pip install tabulate
# Library to import: networkx, tabulate, combinations

# For this assignment, we will study data from epinions.com 
# which represents pairs of reviewers (the nodes) and whether they trust each other or not, 
#represented by a 1 or -1 value for their connecting edge.

# Read the file using below commad on your terminal
#       python3   triads.py   --filename   epinions_small.csv

# Calculating: 
#   1.Number of edgesin the network
#   2.Number of self-loops 
#   3.Number of edgesused to identify triads(referred to as TotEdges)[ this should be a. –b. ]
#   4.Number of positive (trust) edges(ignore self-loops)
#   5.Number of negative (distrust) edges(ignore self-loops)
#   6.Probability  p that an edge will be positive:  (number of positive edges) / TotEdges
#   7.Probability that an edge will be negative:  1 –p
#   8.Expected distribution of triad types (based on  pand  1 –papplied to the number of triangles in the graph).  Show number and percent.
#       a.Trust-Trust-Trust
#       b.Trust-Trust-Distrust
#       c.Trust-Distrust -Distrust
#       d.Distrust-Distrust-Distrust
#       e.Total
#   9.Actual distribution of triad types. Show number and percent.
#       a.Trust-Trust-Trust
#       b.Trust-Trust-Distrust
#       c.Trust-Distrust -Distrust
#       d.Distrust-Distrust-Distrust
#       e.Total

# Reference Link: https://www.cl.cam.ac.uk/~cm542/teaching/2010/stna-pdfs/stna-lecture8.pdf

# Importing tool to study networks
import networkx as nx
# Import table format library
# To install this use command: pip install tabulate
from tabulate import tabulate
# import combinations for recursive solution
from itertools import combinations as comb
# Creating a function with for loop to count 
#   1.Number of edgesin the network
#   2.Number of self-loops 
#   3.Number of edgesused to identify triads(referred to as TotEdges)[ this should be a. –b. ]
#   4.Number of positive (trust) edges(ignore self-loops)
#   5.Number of negative (distrust) edges(ignore self-loops)

def graph_analysis(epinions):
    # Graph class
    g = nx.Graph() 
    total_edges = 0
    self_loops = 0 
    trust_edges = 0 
    distrust_edges = 0 
    # Reading the file
    with open(epinions, 'r') as e:
        for line in e:
            reviewer, reviewee, w = tuple(map(int, line.split(",")))
            # Edges in the Network
            total_edges += 1 if w == 1 or w == -1 else 0 
            # Self- loops in the network
            self_loops += 1 if reviewer == reviewee else 0
            # Number of trust edges
            trust_edges += 1 if reviewer != reviewee and w == 1 else 0
            # Number of Distrust Edges
            distrust_edges +=1 if reviewer != reviewee and w == -1 else 0
            # add the edges to form a graph
            g.add_edge(reviewer, reviewee, w=w)
    return total_edges, self_loops, trust_edges, distrust_edges, g
total_edges, self_loops, trust_edges, distrust_edges, g = graph_analysis("epinions69.csv")
edges_used = trust_edges + distrust_edges - self_loops

# printing all the values calculated above
print("Edges in network: ", total_edges) 
print("Self-loops: ", self_loops)
print("Edges Used: ", edges_used) 
print("Trust Edges: ", trust_edges) 
print("Distrust Edges: ", distrust_edges)  

# Probability  p that an edge will be positive:
p = trust_edges/ edges_used

# Probability that an edge will be negative:  1 –p
q = 1 - p

print("Probability  p that an edge will be positive: ", p)  
print("Probability  p that an edge will be negative: ", q)  
  
# Checking for number of triangles in  Network
triangles = nx.triangles(g) # list of how many triangles each node is part of
tri = sum(triangles.values())/3 # total number of triangles
print("Triangles: ", tri)

# Expected Distribution
prob_trust_trust_trust = p * p * p 
prob_trust_trust_distrust = 3 * (p * p * q)
prob_trust_distrust_distrust = 3 * (p * q * q)
prob_distrust_distrust_distrust = q * q * q

# For Numbers
No_TTT = prob_trust_trust_trust * tri
No_TTD = prob_trust_trust_distrust * tri
No_TDD = prob_trust_distrust_distrust * tri
No_DDD = prob_distrust_distrust_distrust * tri

# Total Percent calculated
Total_per = prob_trust_trust_trust + prob_trust_trust_distrust+ prob_trust_distrust_distrust + prob_distrust_distrust_distrust

# Total number calculated
Total_number = No_TTT + No_TTD + No_TDD + No_DDD

# Showing in tabular form
print((tabulate([["TTT", "{:.1%}".format(prob_trust_trust_trust), No_TTT], ["TTD", "{:.1%}".format(prob_trust_trust_distrust), No_TTD],
                 ["TDD", "{:.1%}".format(prob_trust_distrust_distrust), No_TDD], ["DDD", "{:.1%}".format(prob_distrust_distrust_distrust), No_DDD], 
                 ["Total", "{:.1%}".format(Total_per), Total_number ]],
    headers=["Type", "Percent", "Number"], tablefmt='orgtbl')))

# Actual Distribution
# Adding weight to an edge
weight = nx.get_edge_attributes(g, 'w')
# Calculating triads 
Triads = [edge for edge in nx.enumerate_all_cliques(g)if len(edge) == 3]
#Creating triads llist along with the weight
triads_list = list(map(lambda edge: list(map(lambda edge: (edge, weight[edge]), comb(edge, 2))), Triads))
# INTIALizing the values
T_T_T = 0
T_T_D = 0
T_D_D = 0
D_D_D = 0
# Iterating through each triangles
for triad in triads_list:
    edge_1 = triad[0][1]
    edge_2 = triad[1][1]
    edge_3 = triad[2][1]
    # Based on trust and distrust values calculate the triad types
    if(edge_1 ==1 and edge_2 ==1 and edge_3 ==1):
            triad_type="TTT"
            T_T_T = T_T_T +1
    # Based on trust and distrust values calculate the triad types
    if(edge_1==1 and edge_2==1 and edge_3==-1) or (edge_1==-1 and edge_2==1 and edge_3==1) or (edge_1==1 and edge_2==-1 and edge_3==1):
            triad_type="TTD"
            T_T_D=T_T_D+1
    #Based on trust and distrust values calculate the triad types
    if(edge_1==-1 and edge_2==-1 and edge_3==1) or (edge_1==1 and edge_2==-1 and edge_3==-1) or (edge_1==-1 and edge_2==1 and edge_3==-1):
            triad_type="TDD"
            T_D_D =T_D_D + 1
    #Based on trust and distrust values calculate the triad types
    if(edge_1==-1 and edge_2==-1 and edge_3==-1):
            triad_type="DDD"
            D_D_D=D_D_D+1
# Adding the above calculated value
Total_no =   T_T_T + T_T_D + T_D_D + D_D_D
# Calculting percentage by dividing total count by total number of triangles
per_TTT = T_T_T/tri
per_TTD = T_T_D/tri
per_TDD = T_D_D/tri
per_DDD = D_D_D/tri
Total_per_Actual = per_TTT + per_TTD + per_TDD + per_DDD

print()
print()
# Tabular Form
print((tabulate([["TTT", "{:.1%}".format(per_TTT), T_T_T], ["TTD", "{:.1%}".format(per_TTD), T_T_D],
                 ["TDD", "{:.1%}".format(per_TDD), T_D_D], ["DDD", "{:.1%}".format(per_DDD), D_D_D], 
                 ["Total", "{:.1%}".format(Total_per), Total_no ]],
    headers=["Type", "Percent", "Number"], tablefmt='orgtbl')))


    

    

