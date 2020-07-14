# Join functions

def join_Clusters(clusters_dict, connections_dict, n_clusters):
    con_dict = dict(connections_dict)
    clu_dict = dict(clusters_dict)
    rem_clu_dict = {}
    while len(clu_dict) > n_clusters:
        #if (len(clu_dict) % 10000==0):
        #    print(len(clu_dict))
        c_merge = min_Key_By_Lenght(clu_dict)
        n_merge = set(clu_dict[c_merge])
        del(clu_dict[c_merge])
        if c_merge in con_dict:
            score_dict = {}
            for c in con_dict[c_merge]:
                score_dict[c] = __get_Score_Value(con_dict[c_merge][c], len(clu_dict[c]), len(n_merge))
            if sum(score_dict.values()) == 0:
                rem_clu_dict[c_merge] = n_merge
            else:
                best_c = max_Key_By_Value(score_dict)
                clu_dict[best_c].update(n_merge)
                con_dict = __update_Con_Dict(clu_dict, con_dict, best_c, c_merge)
        else:
            rem_clu_dict[c_merge] = n_merge 
    con_dict = __clean_Con_Dict(con_dict, clu_dict)
    merge_dict = {'mer': clu_dict, 'rem_clusters': rem_clu_dict, 'con_dict': con_dict}
    return merge_dict



def __get_Score_Value(n_connections, lenght_1, lenght_2):
    score = n_connections / (lenght_1*lenght_2)
    return score

def __clean_Con_Dict(con_dict, clu_dict):
    clean_con_dict = {}
    for c_1 in list(clu_dict):
        clean_con_dict[c_1] = {}
        for c_2 in list(clu_dict):
            if c_1 != c_2:
                if c_2 in con_dict[c_1]:
                    clean_con_dict[c_1][c_2] = con_dict[c_1][c_2]
                else:
                    clean_con_dict[c_1][c_2] = 0
    return clean_con_dict

def __update_Con_Dict(clu_dict, con_dict, best_c, c_merge):
    del(con_dict[best_c][c_merge])
    del(con_dict[c_merge][best_c])
    for c in con_dict[c_merge]:
        if c in con_dict[best_c]:
            con_dict[best_c][c] += con_dict[c_merge][c]
            con_dict[c][best_c] += con_dict[c_merge][c]
        else:
            con_dict[best_c][c] = con_dict[c_merge][c]
            con_dict[c][best_c] = con_dict[c_merge][c]
        del(con_dict[c][c_merge])
    del(con_dict[c_merge])
    return con_dict

def get_Connections_Dict(cluster_dict, membership_dict, n_e_dict):
    connections_dict = {}
    for n_1 in membership_dict:
        c_1 = membership_dict[n_1]
        if c_1 not in connections_dict:
            connections_dict[c_1] = {}
        targets_set = n_e_dict[n_1]
        for n_2 in targets_set:
            if n_2 in membership_dict:
                c_2 = membership_dict[n_2]
                if c_1 != c_2:
                    if c_2 not in connections_dict[c_1]:
                        connections_dict[c_1][c_2] = 1
                    else:
                        connections_dict[c_1][c_2] += 1
                else:
                    pass
    return connections_dict

def get_Joins_From_Membership(membership, nodes_dict, n_clusters):
    cluster_dict = get_Clusters_Dict_From_Membership_Dict(membership)
    connections_dict = get_Connections_Dict(cluster_dict, membership, nodes_dict)
    joins_dict = join_Clusters(cluster_dict, connections_dict, n_clusters)
    return joins_dict

def min_Key_By_Lenght(dictionary_of_tuples):
    min_lenght = min([len(value) for value in dictionary_of_tuples.values()])
    max_key = max([key for key in dictionary_of_tuples if len(dictionary_of_tuples[key]) == min_lenght])
    return max_key

def max_Key_By_Value(dictionary_of_values):
    max_value = max([value for value in dictionary_of_values.values()])
    max_key = max([key for key in dictionary_of_values if dictionary_of_values[key] == max_value])
    return max_key