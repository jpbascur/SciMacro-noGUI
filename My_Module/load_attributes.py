def run(filename):
    tab_delimited = parse_Tab_Delimited(filename)
    attributes_dict = parse_Attributes(tab_delimited)
    return attributes_dict

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

def parse_Attributes(tab_delimited):
    attributes_dict = {}
    for row in tab_delimited:
        network_id = row[0]
        words = row[1]
        database_id = row[2]
        title = row[3]
        pub_year = row[4]
        author_name = row[5]
        abstract = row[6]
        source_title = row[7]
        doi = row[8]
        n_cits = row[9]
        attributes_dict[int(network_id)] = {'words': words.split('¶'),
                                            'database_id': database_id, 'title': title, 'pub_year': pub_year, 'author_name': author_name,
                                            'abstract': abstract, 'source_title': source_title, 'doi': doi, 'n_cits': n_cits}
    return attributes_dict