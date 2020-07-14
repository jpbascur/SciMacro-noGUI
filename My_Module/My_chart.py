# Importeren modules
import copy
import math

ERROR_MARGIN = 0.01

def build_Best_Graph(n_dict, c_dict): # main function
    #  n_dict = Nodes Dict
    #  c_dict = Connections Dict
    #  f_nid = First Node Id
    #  o_nid_list = Ordered Nodes Ids List
    solutions_list = []
    for f_nid in n_dict: # for each node in node_list
        print('Creating list of node ' + str(f_nid))
        o_nid_list = ordered_Node_List(f_nid, c_dict, n_dict)
        nodes_list = [n_dict[nid] for nid in o_nid_list] # list of noodes with coordinates
        nodes_list[0]['coor'] = coor_0() # add the first node with coordinates
        nodes_list[1]['coor'] = coor_1(nodes_list[0], nodes_list[1]) # add the second node with coordinates
        for index in range(2, len(nodes_list)):
            print('Evaluating node ' + str(index))
            nodes_list[index]['coor'] = get_Coordinates(nodes_list[index], nodes_list[:index], c_dict)
        solutions_list.append(nodes_list)
    print('Evaluating lists')
    best_solution = min(solutions_list, key=lambda nodes_list: solution_Stress(nodes_list, c_dict)) # get list of nodes with lowest stress
    return best_solution

def ordered_Node_List(f_nid, c_dict, n_dict): # Sort Nodes Ids
    #  nid_l_list = Nodes Ids Left List
    #  s_nid_dict = Score Nodes Ids-To-List Dict
    o_nid_list = [f_nid]
    nid_l_list = list(n_dict.keys())
    nid_l_list.remove(f_nid)
    while len(nid_l_list) > 0:
        print('Done in ' +str(len(nid_l_list)))
        s_nid_dict = {}
        for nid in nid_l_list:
            s_nid_dict[nid] = score_Node_To_List(nid, o_nid_list, c_dict, n_dict)
        max_nid = max(s_nid_dict.keys(), key=lambda nid: s_nid_dict[nid])
        o_nid_list.append(max_nid)
        nid_l_list.remove(max_nid)
    return o_nid_list

def score_Node_To_List(nid1, o_nid_list, c_dict, n_dict):
    score_sum = 0
    for nid2 in o_nid_list:
        score_sum += get_Score(c_dict[nid1][nid2], n_dict[nid1]['lenght'], n_dict[nid2]['lenght'])
    return score_sum

def get_Score(n_connections, lenght_1, lenght_2):
    score = n_connections / (lenght_1*lenght_2)
    return score

def coor_0(): # first node coordinate
    return (0, 0)

def coor_1(node_1, node_2): # second node coordinate
    magnitude_in_X = node_1['radius'] + node_2['radius']
    return ((magnitude_in_X), 0)

def get_Coordinates(node, prior_nodes_list, c_dict):
    stress_list = []
    for prior_pair in pairs_Nodes(prior_nodes_list):
        p_n1 = prior_pair[0]
        p_n2 = prior_pair[1]
        c_1 = {'x': p_n1['coor'][0], 'y': p_n1['coor'][1], 'r': p_n1['radius'] + node['radius'] + ERROR_MARGIN}
        c_2 = {'x': p_n2['coor'][0], 'y': p_n2['coor'][1], 'r': p_n2['radius'] + node['radius'] + ERROR_MARGIN}
        if do_Overlaps(c_1, c_2): #  If circles overlap
            #print('Calculate intersection')
            int_coordinates = coor_Inter(c_1, c_2) # intersection coordinates
            for coordinate in int_coordinates:
                c_3 = {'x': coordinate[0], 'y': coordinate[1], 'r': node['radius']}
                #print('Calculate overlaping wiht any')
                if not overlaps_Any(c_3, prior_nodes_list): #  If nodes don't overlap
                    #print('Node Stress')
                    stress = node_Stress(node['id'], c_3['x'], c_3['y'], prior_nodes_list, c_dict)
                    stress_list.append({'coor': coordinate, 'stress': stress})
                else:
                    pass
        else:
            pass
    best_coordinate = min(stress_list, key=lambda coordinate: coordinate['stress'])['coor']
    return best_coordinate

def overlaps_Any(circle, nodes_list):
    overlaps = False
    index = 0
    while not overlaps and index < len(nodes_list):
        #print('iteration ' + str(index))
        #print('Calculate individual overlaping')
        new_circle = {'x': nodes_list[index]['coor'][0], 'y': nodes_list[index]['coor'][1], 'r': nodes_list[index]['radius']}
        overlaps = do_Overlaps(circle, new_circle)
        index += 1
    return overlaps

def pairs_Nodes(nodes_list): # order-independent combinaton without repetition
    pairs_list  = []
    for n1 in nodes_list:
        for n2 in nodes_list:
            if n1['id'] > n2['id']:
                pairs_list.append((n1, n2))
    return pairs_list

def do_Overlaps(c_1, c_2): # if overlaps return true
    x1 = c_1['x']
    x2 = c_2['x']
    y1 = c_1['y']
    y2 = c_2['y']
    r1 = c_1['r']
    r2 = c_2['r']
    #print(c_1)
    #print(c_2)
    circles_distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    sum_radius = r1 + r2
    overlaps = sum_radius > circles_distance
    #print(overlaps)
    return overlaps

def coor_Inter(c_1, c_2): # intersection points between circles
    # reference: https://math.stackexchange.com/questions/256100/how-can-i-find-the-points-at-which-two-circles-intersect
    # https://gist.github.com/jupdike/bfe5eb23d1c395d8a0a1a4ddd94882ac
    x1 = c_1['x']
    x2 = c_2['x']
    y1 = c_1['y']
    y2 = c_2['y']
    r1 = c_1['r']
    r2 = c_2['r']
    R2 = (x2-x1)**2 + (y2-y1)**2
    R4 = R2**2
    r2r2 = r1**2 - r2**2
    a = r2r2 / (2 * R2)
    c = math.sqrt(2 * (r1**2 + r2**2) / R2 - (r2r2) / R4 - 1)
    fx = (x1+x2) / 2 + a * (x2 - x1)
    gx = c * (y2 - y1) / 2
    ix1 = fx + gx
    ix2 = fx - gx
    fy = (y1+y2) / 2 + a * (y2 - y1)
    gy = c * (x1 - x2) / 2
    iy1 = fy + gy
    iy2 = fy - gy
    int_coordinates = [(ix1, iy1), (ix2, iy1)]
    return int_coordinates


def node_Stress(nid, x1, y1, nodes_list, c_dict): # stress of a node against the graph
    stress = 0
    for p_n in nodes_list:
        p_nid = p_n['id']
        if nid != p_nid:
            x2 = p_n['coor'][0]
            y2 = p_n['coor'][1]
            R2 = (x2-x1)**2 + (y2-y1)**2
            n_edges = c_dict[nid][p_nid]
            stress += n_edges*R2
    return stress

def solution_Stress(nodes_list, c_dict): # total stress of the graph
    solution_stress = 0
    for node in nodes_list:
        node_stress = node_Stress(node['id'], node['coor'][0], node['coor'][1], nodes_list, c_dict)
    solution_stress = solution_stress / 2
    return solution_stress