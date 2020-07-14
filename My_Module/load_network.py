# Network functions
import igraph as ig

def run(filename):
    tab_del = parse_Tab_Delimited(filename)
    network = tab_Delimited_To_Network(tab_del)
    nodes_set = get_Set_Of_Nodes(network)
    ig_network = create_Igraph_Network(network, len(nodes_set))
    return ig_network

def parse_Tab_Delimited(filename):
    #  Takes a tab-delemited file and returns a list of lists
    with open(filename, 'r') as f:
        read_string = f.read()
        #  Create list of lists like file[rows[columns]]
        parsed_string = [row.split('\t') for row in read_string.split('\n')]
        #  Remove lingering line breaks
        while parsed_string[-1] == ['']:
            parsed_string = parsed_string[:-1]
    return parsed_string

def tab_Delimited_To_Network(tab_delimited, clean_duplicates=False):
    #  Convert the values inside the list of lists from strints into integers
    network = set()
    for row in tab_delimited:
        n_1 = int(row[0])
        n_2 = int(row[1])
        edge = (n_1, n_2)
        if clean_duplicates:
            if n_1 < n_2:
                network.add(edge)
        else:
            network.add(edge)
    return network

def get_Set_Of_Nodes(network):
    nodes = set()
    for row in network:
        nodes.add(row[0])
        nodes.add(row[1])
    return nodes

def create_Igraph_Network(network, size):
    ig_network = ig.Graph()
    ig_network.add_vertices(range(size))
    ig_network.add_edges(list(network))
    ig_network.es['weight'] = 1
    return ig_network