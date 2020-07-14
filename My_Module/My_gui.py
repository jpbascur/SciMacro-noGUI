import pickle
import tkinter as tk
import igraph
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from My_Module import My_pre_clustering, My_post, load_network, load_attributes, clustering, merging

def execute_clustering_gui():
    root = tk.Tk()
    clustering_gui(root)
    root.mainloop()

class clustering_gui:
    # LeFr = Left Frame
    # LoDa = Load Data
    # Ra = Radiobutton
    # VaRa = Variable of the Radiobutton
    # QuCl = Quantity of Clusters
    # ClId = Cluster Id
    # ClSo = Clustering Solution
    # ShLa = Show Label
    # ShPa = Show Papers
    # DoPa = Download Papers
    # Gr = Graph
    def __init__(self, root):
        LVL = 8
        self.empty_figure = mpl.figure.Figure(figsize=(7.5, 7.5))
        self.selected_papers = []
        self.show_x_papers = 100
        self.data = {'Gr': False,
                     'Attributes': False,
                     'lv': {}}
        for lv in range(LVL):
            self.data['lv'][lv] = {}
            self.data['lv'][lv]['exists'] = False
            self.data['lv'][lv]['cluster_info'] = None
            self.data['lv'][lv]['global_frequency'] = None
            self.data['lv'][lv]['clusters'] = {}
            self.data['lv'][lv]['figure'] = {}
            self.data['lv'][lv]['figure']['nodes'] = []
            self.data['lv'][lv]['figure']['rendering'] = self.empty_figure
        self.VaRa = tk.IntVar()
        self.VaRaText = {x: tk.StringVar() for x in range(1, LVL)}
        self.selected_cluster = tk.IntVar()
        self.selected_cluster_text = tk.StringVar()
        self.sel_row = tk.IntVar()
        self.enviroment = tk.StringVar()
        self.fig = self.empty_figure
        self.root = root
        root.title('Scientific Macroscope')
        
        # Inititate level 0
        self.data['lv'][0]['exists'] = True
        self.VaRa.set(0)
        self.selected_cluster.set(None)
        self.selected_cluster_text.set('No cluster selected')
        self.sel_row.set(0)
        self.enviroment.set('labels')

        # GUI
        
        # LeFr0 Part 1
        self.LeFr0 = tk.Frame(self.root)
        self.LoNeTeLa = tk.Label(self.LeFr0, text='Network file')
        self.LoAtTeLa = tk.Label(self.LeFr0, text='Attributes file')
        self.LoNeTe = tk.Text(self.LeFr0, height=1, width=20)
        self.LoAtTe = tk.Text(self.LeFr0, height=1, width=20)
        self.LoNeLoAtBu = tk.Button(self.LeFr0, text='Load', command=self.load_Data)
        
        # LeFr0 Part 2
        r_t = ['All Data'] + ['Clustering ' + str(x) for x in range(1, LVL)]
        self.Ra_Ra = {x: tk.Radiobutton(self.LeFr0, text=r_t[x], variable=self.VaRa, value=x, command=self.click_Ra) for x in range(LVL)}
        self.Ra_Te = {x: tk.Label(self.LeFr0, text='-', textvariable=self.VaRaText[x]) for x in range(1, LVL)}
        
        # LeFr0 Part 3
        self.QuClLa = tk.Label(self.LeFr0, text='Q Clusters')
        self.QuClTe = tk.Text(self.LeFr0, height=1, width=3, bg='#D3D3D3')
        self.ClIdLa = tk.Label(self.LeFr0, text='Clusters ID')
        self.ClIdTe = tk.Text(self.LeFr0, height=3, width=20)
        self.ClSoBu = tk.Button(self.LeFr0, text='Create clustering solution', command=self.create_ClSo)
        self.QueryLa = tk.Label(self.LeFr0, text='Query search')
        self.QueryTe = tk.Text(self.LeFr0, height=1, width=20)
        self.QueryBu = tk.Button(self.LeFr0, text='Search', command=self.QuerySearch)
        
        # LeFr1
        self.LeFr1 = tk.Frame(self.root)
        self.Canvas = FigureCanvasTkAgg(self.fig, master=self.LeFr1)
        self.Canvas.draw()
        
        # LeFr2
        self.LeFr2 = tk.Frame(self.root)
        self.LiBoFr = tk.Frame(self.LeFr2)
        self.ScrollY = tk.Scrollbar(self.LiBoFr, orient='vertical')
        self.ScrollX = tk.Scrollbar(self.LiBoFr, orient='horizontal')
        self.LiBo = tk.Listbox(self.LiBoFr, yscrollcommand=self.ScrollY.set, xscrollcommand=self.ScrollX.set, height=35, width=80)
        self.ShLaBu = tk.Button(self.LeFr2, text='Show Labels', command=self.CreateShLa)
        self.ShPaBu = tk.Button(self.LeFr2, text='Show Paper List',  command=self.CreateShPa)
        self.DoPaLa = tk.Label(self.LeFr2, text='-', textvariable=self.selected_cluster_text)
        self.DoPaBu = tk.Button(self.LeFr2, text='Download Paper List', command=self.RunDoPa)
        self.DoPaTe = tk.Text(self.LeFr2, height=1, width=40)
   
        # Grid LeFr0 Part 1
        self.LeFr0.grid(row=100, column=100, sticky=tk.W)
        self.LoNeTeLa.grid(row=100, column=100, sticky=tk.W, pady=(10, 0))
        self.LoNeTe.grid(row=101, column=100, sticky=tk.W, pady=(10, 0))
        self.LoAtTeLa.grid(row=102, column=100, sticky=tk.W, pady=(10, 0))
        self.LoAtTe.grid(row=103, column=100, sticky=tk.W, pady=(10, 0))
        self.LoNeLoAtBu.grid(row=104, column=100, pady=(0, 50))
        
        # Grid LeFr0 Part 2
        p2_row = 200
        self.Ra_Ra[0].grid(row=p2_row, column=100, sticky=tk.W)
        for lv in self.Ra_Te:
            p2_row += 1
            self.Ra_Te[lv].grid(row=p2_row, column=100, sticky=tk.W)
            p2_row += 1
            if lv+1 != LVL:
                self.Ra_Ra[lv].grid(row=p2_row, column=100, sticky=tk.W)
            else:
                self.Ra_Ra[lv].grid(row=p2_row, column=100, sticky=tk.W, pady=(0, 50))
                
        # Grid LeFr0 Part 3
        self.LeFr2.grid(row=100, column=300, sticky=tk.W)
        self.QuClLa.grid(row=300, column=100, sticky=tk.W)
        self.QuClTe.grid(row=301, column=100, sticky=tk.W)
        self.ClIdLa.grid(row=302, column=100, sticky=tk.W)
        self.ClIdTe.grid(row=303, column=100, sticky=tk.W)
        self.ClSoBu.grid(row=304, column=100)
        self.QueryLa.grid(row=305, column=100)
        self.QueryTe.grid(row=306, column=100)
        self.QueryBu.grid(row=307, column=100)
        self.QuClTe.insert(tk.INSERT, '10')
        
        # Grid LeFr1
        self.LeFr1.grid(row=100, column=200, sticky=tk.W)
        self.Canvas.get_tk_widget().grid(row=100, column=100, padx=10, pady=10, sticky=tk.W)

        # LeFr2
        self.LiBoFr.grid(row=100, column=100)
        self.ShLaBu.grid(row=101, column=100, sticky=tk.W)
        self.ShPaBu.grid(row=102, column=100, sticky=tk.W)
        self.DoPaLa.grid(row=200, column=100, pady=(50, 0), sticky=tk.W)
        self.DoPaTe.grid(row=201, column=100, sticky=tk.W)
        self.DoPaBu.grid(row=202, column=100, sticky=tk.W)
        self.ScrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.ScrollX.pack(side=tk.BOTTOM, fill=tk.X)
        self.ScrollY.config(command=self.LiBo.yview)
        self.ScrollX.config(command=self.LiBo.xview)
        self.LiBo.bind('<<ListboxSelect>>', self.ClickListbox)
        self.LiBo.pack(side=tk.LEFT, fill=tk.BOTH)

    # Functions
    # Left side

    def load_Data(self):
        PATH_network = self.LoNeTe.get("1.0", "end-1c")
        PATH_attributes = self.LoAtTe.get("1.0", "end-1c")
        self.data['Gr'] = load_network.run(PATH_network)
        self.data['Attributes'] = load_attributes.run(PATH_attributes)

    def click_Ra(self):
        self.render_Level(self, self.VaRa.get())
        
    def present_Level(self, lv):
        self.clean_State()
        self.VaRa.set(lv)
        self.present_Figure(self.data['lv'][lv]['figure']['rendering'])
        self.present_Labels(self.data['lv'][lv]['labels'])
        
    def clean_State(self):
        self.sel_row.set(0)
        self.selected_papers = []
        self.enviroment.set('labels')
        
    def present_Figure(self, fig):
        self.Canvas.get_tk_widget().destroy()
        self.Canvas = FigureCanvasTkAgg(fig, master=self.LeFr1)
        self.Canvas.draw()
        self.Canvas.get_tk_widget().grid(row=100, column=100, padx=10, pady=10, sticky=tk.W)
        
    def present_Labels(self, labels):
        self.enviroment.set('labels')
        self.LiBo.delete(0, tk.END)
        for row in labels:
            self.LiBo.insert(tk.END, row)

    def render_Fig(self, chart_nodes, intensity_list=False):
        fig = plt.figure(figsize=(7.5, 7.5))
        ax = fig.add_axes([0, 0, 1, 1])
        x_list = [x['coor'][0] for x in chart_nodes]
        y_list = [x['coor'][1] for x in chart_nodes]
        radii = [x['radius'] for x in chart_nodes]
        size_dict = {'X_min': 0, 'Y_min': 0, 'X_max': 0, 'Y_max': 0}
        if not intensity_list:
            color_list = [(0, 0, 1, 0.4) for x in chart_nodes]
        else:
            color_list = [(0, 0, 1, (intensity_list[x] + 0.1)/2.0) for x in intensity_list]
        for x, y, r, c in zip(x_list, y_list, radii, color_list):
            size_dict = __update_Size(size_dict, x, y, r)
            circle = mpatches.Circle((x, y), r, facecolor=c, edgecolor='k', linewidth=0.7)
            ax.add_patch(circle)
        ax.set_xlim(size_dict['X_min'], size_dict['X_max'])
        ax.set_ylim(size_dict['Y_min'], size_dict['Y_max'])
        ax.set_axis_off()
        for node in chart_nodes:
            ax.annotate(str(node['id'] + 1), (node['coor'][0], node['coor'][1]))
        return fig

    def create_ClSo(self):
        lv = self.VaRa.get()
        QuCl = int(self.QuClTe.get("1.0", "end-1c"))
        if lv == 0:
            join_dict = cluster_And_Join(QuCl, self.data['Gr'])
        else:
            self.data['lv'][lv]['selected_clusters'] = selected_clusters = self.read_ClIdTe()
            if len(cluster_list) != 0:
                nodes_list = self.get_Cluster_Nodes(lv, selected_clusters)
                sub_Gr = self.data['Gr'].subgraph(nodes_list)
                join_dict = cluster_And_Join(QuCl, sub_Gr)
            else:
                print('No Cluster Selected')
                join_dict = cluster_And_Join(QuCl, self.data['Gr'])
        self.VaRa.set(self.VaRa.get() + 1)
        self.VaRaText[self.VaRa.get()].set(id_string)
        self.data['lv'][lv]['clusters'] = join_dict['merge_dict']
        self.data['lv'][lv]['figure']['nodes'] = figure_nodes_dict = join_dict['graph_dict']
        self.data['lv'][lv]['figure']['rendering'] = self.render_Fig(self.data['lv'][lv]['figure']['nodes'])
        self.present_Level(self.VaRa.get())
        self.TEST_Export_Data()
        
    def read_ClIdTe(self):
        cluster_list_string = self.ClIdTe.get("1.0", "end-1c")
        cluster_list_int = [int(x) for x in id_string.split(',')]
        return cluster_list_int
        
    def get_Cluster_Nodes(self, lv, clusters_list):
        nodes_list = []
        for cluster in cluster_list:
            nodes_list = self.data['lv'][lv]['clusters']['nodes'][cluster]
        return nodes_list

        
        
    def TEST_Export_Data(self):
        pickle.dump(self.data, open("test.p", "wb"))

    def QuerySearch(self):
        level = self.VaRa.get()
        query = self.QueryTe.get("1.0", "end-1c")
        if query in self.data['translation_reverse']:
            query_no = self.data['translation_reverse'][query]
            frecuency = {}
            for i in self.data['cluster_info'][level]:
                if query_no in self.data['cluster_info'][level][i]['local_frequency']:
                    query_local_frequency = self.data['cluster_info'][level][i]['local_frequency'][query_no]
                    local_size = self.data['cluster_info'][level][i]['size']
                    frecuency[i] = {
                        'query_local_frequency': query_local_frequency, 'local_size': local_size}
                else:
                    frecuency[i] = {
                        'query_local_frequency': 0, 'local_size': 0}
            print(frecuency)
            normalized_frecuency = self.__FrecuencyNormalization(frecuency)
            print(normalized_frecuency)
            self.CreateClSo(intensity_list=normalized_frecuency)
        else:
            print('None')

    def __FrecuencyNormalization(self, frecuency):
        ratio_dict = {}
        for i in frecuency:
            if frecuency[i]['local_size'] == 0:
                ratio_dict[i] = 0
            else:
                ratio_dict[i] = float(
                    frecuency[i]['query_local_frequency']) / frecuency[i]['local_size']
        max_ratio = max(ratio_dict.values())
        for i in ratio_dict:
            if ratio_dict[i] == 0:
                ratio_dict[i] = 0
            else:
                ratio_dict[i] = ratio_dict[i] / max_ratio
        return ratio_dict



    def drill_Down(self):
        QuCl = int(self.QuClTe.get("1.0", "end-1c"))
        id_string = self.ClIdTe.get("1.0", "end-1c")
        clusters_id_list = [int(x) for x in id_string.split(',')]
        partition = self.data['cluster_info'][self.VaRa.get()]
        clusters_nodes_list = [partition[cluster_id]['members'] for cluster_id in clusters_id_list]
        nodes = [node for cluster_nodes in clusters_nodes_list for node in cluster_nodes]  # Learn this compress list function
        Gr = self.data['Gr'][self.VaRa.get()]
        sub_Gr = Gr.subgraph(nodes)
        self.VaRa.set(self.VaRa.get() + 1)
        self.VaRaText[self.VaRa.get()].set(id_string)
        self.data['Gr'][self.VaRa.get()] = sub_Gr
        self.data['ClId'][self.VaRa.get()] = id_string
        self.__ClusterizeSomeData(QuCl, sub_Gr)

    def __ClusterizeAllData(self):
        self.VaRa.set(self.VaRa.get() + 1)
        QuCl = int(self.QuClTe.get("1.0", "end-1c"))
        Gr = self.data['Gr']
        self.__ClusterizeSomeData(QuCl, Gr)
        


    
    def __GetLabels(self, cluster_info, global_frequency):
        labels = {}
        for i in cluster_info:
            labels[i] = str(cluster_info[i]['id']) + ': ' + str(cluster_info[i]['size'])
            score_list = []
            for j in cluster_info[i]['local_frequency']:
                if j in global_frequency:
                    score = cluster_info[i]['local_frequency'][j] / (global_frequency[j]+25)
                    score_list.append((j, score))
                else:
                    score_list.append((j, 0))
            score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
            for k in [x[0] for x in score_list[:4]]:
                labels[i] += ' | ' + self.data['translation'][k]
        return labels

    # Right side
    def CreateShLa(self):
        self.enviroment.set('labels')
        self.selected_papers = []
        self.LiBo.delete(0, tk.END)
        level = self.VaRa.get()
        if level != 0:
            for i in self.data['labels'][level]:
                self.LiBo.insert(tk.END, self.data['labels'][level][i])

    def CreateShPa(self):
        if self.enviroment.get() == 'labels':
            self.enviroment.set('papers')
            VaRa = self.VaRa.get()
            nodes = self.data['cluster_info'][VaRa][self.sel_row.get(
            ) + 1]['members']
            sub_Gr = self.data['Gr'][VaRa].subgraph(nodes)
            node_list = [node for node in sub_Gr.vs]
            sorted_list = sorted(node_list, reverse=True,
                                 key=lambda x: x['n_cits'])
            self.selected_papers = sorted_list
            self.LiBo.delete(0, tk.END)
            for node in sorted_list[: self.show_x_papers]:
                self.LiBo.insert(tk.END, str(int(node['pub_year']))
                                 + ' | ' + str(node['n_cits'])
                                 + ' | ' + node['title']
                                 + ' | ' + node['source_title'])

    def ClickListbox(self, event):
        if self.VaRa.get() == 0:
            self.enviroment.set('all_data')
        if self.enviroment.get() == 'labels':
            event_widget = event.widget
            self.sel_row.set(event_widget.curselection()[0])
            self.selected_cluster.set(self.sel_row.get() + 1)
            self.selected_cluster_text.set('Selected cluster ' + str(self.selected_cluster.get())
                                           + ' from clustering ' + str(self.VaRa.get()))

    def RunDoPa(self):
        if self.selected_cluster.get() == None:
            self.selected_cluster_text.set('Please select a cluster')
        else:
            file_name = self.DoPaTe.get("1.0", "end-1c")
            VaRa = self.VaRa.get()
            nodes = self.data['cluster_info'][VaRa][self.selected_cluster.get(
            )]['members']
            sub_Gr = self.data['Gr'][VaRa].subgraph(nodes)
            node_list = [node for node in sub_Gr.vs]
            sorted_list = sorted(node_list, reverse=True,
                                 key=lambda x: x['n_cits'])
            papers_list = self.__CreateListPapers(sorted_list)
            self.__WriteListOfList(file_name, papers_list)

    def __CreateListPapers(self, sorted_list):
        papers_list = [['title',
                        'pub_year',
                        'author',
                        'abstract',
                        'source_title',
                        'doi',
                        'n_cits',
                        'internal_n_cits']]
        for i in sorted_list:
            paper_data = [i['title'],
                          i['pub_year'],
                          i['author'],
                          i['abstract'],
                          i['source_title'],
                          i['doi'],
                          i['n_cits'],
                          i['internal_n_cits']]
            papers_list.append(paper_data)
        return papers_list

            

def cluster_And_Join(n_clusters, ig_network):
    o_c_dict = clustering.optimal_Clusters_Dict(ig_network)
    merge_dict = merging.join_Clusters(o_c_dict['clusters_dict'], o_c_dict['connections_dict'], n_clusters)
    s_merge_dict = __sort_And_Enumerate_Merge_Dict(merge_dict)
    graph_nodes_dict = My_post.__build_Graph(s_merge_dict['mer'], s_merge_dict['con_dict'])
    out_dict = {'merge_dict': s_merge_dict, 'graph_dict': graph_nodes_dict}
    return out_dict

def __get_Words_Frequencies(clusters_dict, attributes_dict):
    all_words_list = []
    c_w_dict = {}
    for cluster in clusters_dict:
        c_w_dict[cluster] = []
        nodes_set = clusters_dict[cluster]
        for node in nodes_set:
            words_list = attributes_dict[node]['words']
            all_words_list += words_list
            c_w_dict[cluster] += words_list
    global_frecuency_dict = dict(collections.Counter(all_words_list))
    local_frecuency_dict = {c: dict(collections.Counter(c_w_dict[c])) for c in c_w_dict}
    frecuency_dict = {'global': global_frecuency_dict, 'local': local_frecuency_dict}
    return frecuency_dict


def __sort_And_Enumerate_Merge_Dict(merge_dict):
    s_clusters = sorted(merge_dict['mer'], reverse=True, key=lambda cluster: len(merge_dict['mer'][cluster]))
    s_tran = {e[1]: e[0] for e in enumerate(s_clusters, start=1)}
    s_merge = {s_tran[cluster]: merge_dict['mer'][cluster] for cluster in merge_dict['mer']}
    s_con = {}
    for c1 in merge_dict['con_dict']:
        s_con[s_tran[c1]] = {}
        for c2 in merge_dict['con_dict'][c1]:
            s_con[s_tran[c1]][s_tran[c2]] =  merge_dict['con_dict'][c1][c2]
    s_rem = []
    for cluster in merge_dict['rem_clusters']:
        s_rem += merge_dict['rem_clusters'][cluster]
    s_merge_dict = {'mer': s_merge, 'con_dict': s_con, 'rem_clusters': s_rem}
    return s_merge_dict
                             
                             
def __update_Size(size_dict, x, y, r):
    size_dict['X_min'] = min([size_dict['X_min'], x - r])
    size_dict['Y_min'] = min([size_dict['Y_min'], y - r])
    size_dict['X_max'] = max([size_dict['X_max'], x + r])
    size_dict['Y_max'] = max([size_dict['Y_max'], y + r])
    return size_dict

