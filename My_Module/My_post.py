from My_Module import My_chart
import math
import collections

def get_Post_Clus_Dict(clusters_dict, connections_dict):
    b_nodes_data = __build_Graph(clusters_dict, connections_dict)
    frequency = __GetFrequency(partition)
    cluster_info = __GetInfo(partition, frequency)
    post_dict = {'nodes':b_nodes_data, 'cluster_info':cluster_info, 'global_frequency':frequency['global_frequency']}
    return post_dict

def __build_Graph(clusters_dict, connections_dict):
    #  b = Bubble from the bubble chart
    b_nodes_dict = {}
    print('Creating relatedness dictionary')
    relatedness_dict = __get_Relatednes_Dict(clusters_dict, connections_dict)
    for cluster in clusters_dict:
        b_node = {}
        b_node['id'] = cluster
        b_node['edges'] = relatedness_dict[cluster]
        b_node['radius'] = math.sqrt(len(clusters_dict[cluster]) / math.pi)
        b_node['lenght'] = len(clusters_dict[cluster])
        b_nodes_dict[cluster] = b_node
    print('Geting coordinates')
    b_nodes_data = My_chart.build_Best_Graph(b_nodes_dict, connections_dict)
    return b_nodes_data

def __get_Relatednes_Dict(clu_d, con_d):
    rel_d = {}
    for c1 in con_d:
        rel_d[c1] = {}
        rel_d[c1][c1] = 1
        for c2 in con_d[c1]:
            rel_d[c1][c2] = __relatedness_Score(con_d[c1][c2], len(clu_d[c1]), len(clu_d[c2]))
    return rel_d

def __relatedness_Score(n_connections, lenght_1, lenght_2):
    score = n_connections / (lenght_1*lenght_2)
    return score

def __GetFrequency(partition):
    global_word_list = []
    local_frequency = {}
    for i in range(len(partition)):
        local_word_list = []
        for j in partition[i]:
            node_word_list = partition.graph.vs[j]['noun_phrase']
            local_word_list += node_word_list
            global_word_list += node_word_list
        local_frequency[i] = dict(collections.Counter(local_word_list))
    global_frequency = dict(collections.Counter(global_word_list))
    frequency = {'global_frequency':global_frequency, 'local_frequency':local_frequency}
    return frequency

def __GetInfo(partition, frequency):
    cluster_info = {}
    for i in range(len(partition)):
        info = {}
        info['id'] = i + 1
        info['members'] = partition[i]
        info['size'] = len(partition[i])
        info['local_frequency'] = frequency['local_frequency'][i]
        cluster_info[info['id']] = info
    return cluster_info