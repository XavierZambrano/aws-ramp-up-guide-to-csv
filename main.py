import camelot
import pandas as pd


def remove_unnecessary_columns(table):
    return table.iloc[:, -3:]


def get_row_index_start_first_table(table):
    learning_resource_column = table['Learning Resource']
    index = (learning_resource_column == 'Learning Resource').idxmax()

    return index - 1 if index > 0 else 0


def get_start_end_indexes_and_table_title(table):
    learning_resource_column = table['Learning Resource']
    indexes_learning_resource = learning_resource_column[learning_resource_column == 'Learning Resource'].index.tolist()
    last_index = len(table.index)

    start_end_indexes = []
    for n, index_title in enumerate(indexes_learning_resource):
        table_title = learning_resource_column[index_title - 1]
        index_start_table_content = index_title + 1

        if n == len(indexes_learning_resource) - 1:
            index_end_table_content = last_index + 1
        else:
            index_end_table_content = indexes_learning_resource[n + 1] - 1

        start_end_indexes.append((index_start_table_content, index_end_table_content, table_title))

    return start_end_indexes


def clean_rows(df):
    df = df[~df['Learning Resource'].str.contains('AWS Ramp-Up Guide', case=False)]
    return df


def add_is_paid_column(df):
    df[''] = df['Learning Resource'].apply(lambda x: '$' if '$' in x else '')
    # move this column to the first position
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    return df


def clean_learning_resource_column(df):
    df['Learning Resource'] = df['Learning Resource'].apply(lambda x: x.replace('$', '').strip())
    return df


file = 'input/Ramp-Up_Guide_Developer.pdf'

# use a different table_areas for the first page?
tables = camelot.read_pdf(file, flavor='stream', pages='all', edge_tol=50, row_tol=13)
first_df = remove_unnecessary_columns(tables[0].df)
first_df.columns = ['Learning Resource', 'Duration (hrs)', 'Type']
index_start_first_table = get_row_index_start_first_table(first_df)
first_df = first_df.iloc[index_start_first_table:]

dfs = []
dfs.append(first_df)
for table in tables[1:]:
    df = remove_unnecessary_columns(table.df)
    df.columns = ['Learning Resource', 'Duration (hrs)', 'Type']
    dfs.append(df)

concatenated_df = pd.concat(dfs, axis=0, ignore_index=True)
concatenated_df = clean_rows(concatenated_df)
concatenated_df = add_is_paid_column(concatenated_df)
concatenated_df = clean_learning_resource_column(concatenated_df)

print('concatenated_df')
print(concatenated_df)

start_end_indexes = get_start_end_indexes_and_table_title(concatenated_df)

ramp_up_tables = []
for start, end, title in start_end_indexes:
    my_df = concatenated_df.copy()
    ramp_up_tables.append({'title': title, 'df': my_df.iloc[start:end]})

dfs_to_concat = []
for ramp_up_table in ramp_up_tables:
    # get number of columns
    n_columns = len(ramp_up_table['df'].columns)

    # create emtpy row df
    empty_row = ['' for i in range(n_columns)]

    # create title row df
    title = empty_row.copy()
    title[1] = ramp_up_table['title']

    title_df = pd.DataFrame([title], columns=ramp_up_table['df'].columns)
    headers_row_df = pd.DataFrame([ramp_up_table['df'].columns], columns=ramp_up_table['df'].columns)
    empty_row_df = pd.DataFrame([empty_row], columns=ramp_up_table['df'].columns)

    ramp_up_df = pd.concat([title_df, headers_row_df, ramp_up_table['df'], empty_row_df], axis=0)
    dfs_to_concat.append(ramp_up_df)
    print('ramp_up_df')
    print(ramp_up_df)

concatenated_df = pd.concat(dfs_to_concat, axis=0, ignore_index=True)
print('concatenated_df')
print(concatenated_df)
concatenated_df.to_csv('output/ramp_up.csv', index=False, header=False)
