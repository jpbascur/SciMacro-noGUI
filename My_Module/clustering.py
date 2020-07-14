#clustering functions
import time

def optimal_Clusters_Dict(ig_network, r_list=[0.1, 0.01, 0.001, 0.0001, 0.00001]):
    index_to_name_translation = __get_Index_To_Name_Translation(ig_network)
    done = False
    index = 0
    print('Iteration ' + str(index))
    my_time = time.time()
    partition = __get_Partition_Class(ig_network, r_list[0])
    print(time.time() - my_time)
    while not done:
        index += 1
        if index < len(r_list):
            print('Iteration ' + str(index))
            my_time = time.time()
            new_partition = __get_Partition_Class(ig_network, r_list[index])
            print(time.time() - my_time)
            if __too_Big(new_partition):
                done = True
            else:
                partition = new_partition
        else:
            done = True
    connections_dict = __get_Conn_Dict_From_Partition(partition)        
    clusters_dict = __get_Cluster_Dict_From_Partition(partition, index_to_name_translation)
    out_dict = {'resolution': r_list[index], 'connections_dict': connections_dict, 'clusters_dict': clusters_dict}
    return out_dict

def __get_Index_To_Name_Translation(ig_network):
    translation_dict = {}
    for vertex in ig_network.vs:
        translation_dict[vertex.index] = vertex['name']
    return translation_dict
        
def __get_Partition_Class(ig_network, resolution):
    partition = ig_network.community_leiden(resolution_parameter=resolution)
    return partition

def __too_Big(partition, max_fraction=1/3):
    condition = partition.giant().vcount() > partition.graph.vcount()*max_fraction
    return condition

def __get_Conn_Dict_From_Partition(partition):
    cluster_graph = partition.cluster_graph(combine_edges=sum)
    connections_dict = {vertex.index: {} for vertex in cluster_graph.vs}
    for edge in cluster_graph.es:
        source = edge.source
        target = edge.target
        weight = edge['weight']
        connections_dict[source][target] = weight
        connections_dict[target][source] = weight
    return connections_dict

def __get_Cluster_Dict_From_Partition(partition, tr):
    clusters_dict = {e[0]: set([tr[node_index] for node_index in e[1]]) for e in enumerate(partition)}
    return clusters_dict