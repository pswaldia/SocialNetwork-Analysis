import networkx as nx

# Reading the gpickle file 
G = nx.read_gpickle("github.p")

# Define get_nodes_from_partition()
def get_nodes_from_partition(G,partition):
    '''
    G: Graph object
    partition: String , name of the partition we want info about.
    '''
    nodes=[n for n,d in G.nodes(data=True) if d['bipartite']==partition]
    return nodes

# Print the number of nodes in the 'projects' partition
print(len(get_nodes_from_partition(G, 'projects')))

# Print the number of nodes in the 'users' partition
print(len(get_nodes_from_partition(G,'users')))




def shared_partition_nodes(G,node1,node2):
    '''
    G: graph object
    node1: String
    node2: String
    '''
    assert G.node[node1]['bipartite'] == G.node[node2]['bipartite']

    nbrs1 = G.neighbors(node1)

    nbrs2 = G.neighbors(node2)

    # Compute the overlap using set intersections
    overlap = set(nbrs1).intersection(nbrs2)
    return overlap

# # Print the number of shared repositories between users 'u7909' and 'u2148'
# print(len(shared_partition_nodes(G,'u7909','u2148')))
# print(shared_partition_nodes(G,'u7909','u2148'))



def similarity_Score(G, user1, user2, proj_nodes):
    '''
    G: graph object
    user1: String
    user2: String
    proj_nodes: integer, no. of nodes in project partition
    '''
    assert G.node[user1]['bipartite'] == 'users'
    assert G.node[user2]['bipartite'] == 'users'

    shared_nodes = shared_partition_nodes(G,user1,user2)

    return len(shared_nodes) / proj_nodes

# Compute the similarity score between users 'u7909' and 'u2148'
project_nodes = get_nodes_from_partition(G,'projects')
similarity_score = similarity_Score(G,'u7909','u2148',len(project_nodes))

print(similarity_score)


from collections import defaultdict

def most_similar_users(G, user, user_nodes, project_nodes):
    '''
    G: graph
    user: String
    user_nodes: nodes in user partition
    project_nodes: nodes in project partition
    '''
    user_nodes = set(user_nodes) 
    user_nodes.remove(user)
    similarities = defaultdict(list)
    for n in user_nodes:
        similarity = similarity_Score(G, user, n, len(project_nodes))
        similarities[similarity].append(n)

    max_similarity = max(similarities.keys())
    return similarities[max_similarity]

user_nodes = get_nodes_from_partition(G, 'users')
project_nodes = get_nodes_from_partition(G, 'projects')

print(most_similar_users(G, 'u4560', user_nodes, project_nodes))


def recommend_repositories(G, from_user, to_user):
    # Get the set of repositories that from_user has contributed to
    from_repos = set(G.neighbors(from_user))
    # Get the set of repositories that to_user has contributed to
    to_repos = set(G.neighbors(to_user))

    # Identify repositories that the from_user is connected to that the to_user is not connected to
    return from_repos.difference(to_repos)

# Print the repositories to be recommended
print('Recommended Repositories: ')
print(recommend_repositories(G, 'u14984', 'u4560'))
