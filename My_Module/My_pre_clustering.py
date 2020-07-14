import pyodbc
import pandas as pd
import igraph as ig


def run(user_name, level, cluster_id):
    out_string = _getSqlQuery(level, cluster_id)
    documents_data = _getDocumentsData(out_string, user_name)
    translation = _getTranslationDict(documents_data['translation'])
    graph = _getGraph(
        documents_data['papers'], documents_data['conections'], documents_data['paper_np'])
    preculster_dict = {'graph': graph, 'translation': translation}
    print(list(graph.es))
    return preculster_dict


def _getSqlQuery(level, cluster_id):
    if level == 1:
        cluster_id_level = "cluster_id1 = "
    elif level == 2:
        cluster_id_level = "cluster_id2 = "
    elif level == 3:
        cluster_id_level = "cluster_id3 = "
    out_string = """
    /*select the cluster*/
    SELECT
    ut
    INTO #ut
    FROM [wos_1913_classification].[dbo].[clustering]
    WHERE """ + cluster_id_level + str(cluster_id) + """

    /*create the network of the cluster*/
    SELECT
    [citing_ut]
    ,[cited_ut]
    INTO #citingut_citedut
    FROM [wos_1913].[dbo].[citation]
    WHERE [citing_ut] IN (SELECT ut FROM #ut) AND [cited_ut] IN (SELECT ut FROM #ut)

    /*get the number of citations within the clusters*/
    SELECT
    a.ut
    ,sum(case when b.[citing_ut] is null then 0 else 1 end) as internal_n_cits
    INTO #ut_internalncits
    FROM #ut AS a
    LEFT JOIN #citingut_citedut AS b ON a.ut = b.[cited_ut]
    GROUP BY
    a.ut

    /*create the data table of the papers*/
    SELECT
    a.ut
    ,b.pub_year
    ,b.doi
    ,b.[n_cits]
    ,c.title
    ,d.abstract
    ,e.[source_title]
    ,g.author
    ,h.internal_n_cits
    INTO #ut_data
    FROM #ut AS a
    JOIN [wos_1913].[dbo].[pub] AS b on a.ut = b.ut
    LEFT JOIN [wos_1913].[dbo].[pub_title] AS c ON b.ut = c.ut
    LEFT JOIN [wos_1913].[dbo].[pub_abstract] AS d ON b.ut = d.ut
    LEFT JOIN [wos_1913].[dbo].[source] AS e on b.source_id = e.source_id
    LEFT JOIN
    (
        select ut, [author_id] from [wos_1913].[dbo].[pub_author] where [author_seq] = 1
    ) as f on b.ut = f.ut
    LEFT JOIN [wos_1913].[dbo].[author] as g on f.author_id = g.author_id
    LEFT JOIN #ut_internalncits as h on a.ut = h.ut

    /*get the nounphrase codes of the titles*/
    SELECT
    a.ut
    ,b.[noun_phrase_id]
    INTO #ut_nounphraseid
    FROM #ut as a
    JOIN [wos_1913_text].[dbo].[title_noun_phrase] as b on a.ut = b.ut

    /*get the nounphrase codes of the abstracts*/
    INSERT INTO #ut_nounphraseid
    SELECT
    a.ut
    ,b.[noun_phrase_id]
    FROM #ut as a 
    JOIN [wos_1913_text].[dbo].[abstract_noun_phrase] as b on a.ut = b.ut

    /*remove duplicates*/
    SELECT DISTINCT
    ut
    ,[noun_phrase_id]
    INTO #distinct_ut_nounphraseid
    FROM #ut_nounphraseid

    /*make nounphrase codes unique*/
    SELECT DISTINCT
    [noun_phrase_id]
    INTO #distinct_nounphraseid
    FROM #distinct_ut_nounphraseid

    /*get the nounphrase text of the nounphrase codes*/
    SELECT
    a.[noun_phrase_id],
    b.[noun_phrase]
    INTO #nounphraseid_nounphrase
    FROM #distinct_nounphraseid as a
    JOIN [wos_1913_text].[dbo].[noun_phrase] as b on a.[noun_phrase_id] = b.[noun_phrase_id]
    """
    return out_string


def _getDocumentsData(out_string, user_name):
    conn = _getConn(user_name)
    cursor = conn.cursor()
    cursor.execute(out_string)
    t_query = "select * from #nounphraseid_nounphrase order by noun_phrase_id"
    n_query = "select * from #distinct_ut_nounphraseid order by ut, noun_phrase_id"
    p_query = "select * from #ut_data order by n_cits desc"
    c_query = "select * from #citingut_citedut"
    translation = pd.read_sql(t_query, conn)
    paper_np = pd.read_sql(n_query, conn)
    papers = pd.read_sql(p_query, conn)
    conections = pd.read_sql(c_query, conn)
    documents_data = {'translation': translation,
                      'paper_np': paper_np, 'papers': papers, 'conections': conections}
    cursor.close()
    conn.close()
    del(cursor)
    del(conn)
    return documents_data


def _getConn(user_name):
    conn = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
                          server='p-cwts-010260',
                          user=user_name,
                          trusted_connection='yes',
                          unicode_results=False,
                          MARS_Connection='Yes')
    return conn


def _getTranslationDict(translation):
    translation_dict = dict()
    for i in translation.iterrows():
        row = i[1]
        translation_dict[row['noun_phrase_id']] = row['noun_phrase']
    return translation_dict


def _getGraph(papers, conections, paper_np):
    graph = ig.Graph.DictList(vertices=papers.to_dict('records'),
                              edges=conections.to_dict('records'),
                              directed=True,
                              vertex_name_attr='ut',
                              edge_foreign_keys=('cited_ut', 'citing_ut'))
    ut_dict = dict()
    for index, row in papers.iterrows():
        ut_dict[row['ut']] = index
    paper_np_dict = dict()
    for index in range(len(ut_dict)):
        paper_np_dict[index] = list()
    for index, row in paper_np.iterrows():
        paper_np_dict[ut_dict[row['ut']]].append(row['noun_phrase_id'])
    for node in graph.vs:
        index = node.index
        node['noun_phrase'] = paper_np_dict[index]
    graph.simplify()
    return graph
