import camelot
import pandas as pd


def remove_unnecessary_columns(table):
    return table.iloc[:, -3:]


def get_row_index_start_first_table(table):
    first_column = table.iloc[:, 0]
    index = (first_column == 'Learning Resource').idxmax()

    return index - 1 if index > 0 else 0


file = 'input/Ramp-Up_Guide_Developer.pdf'

# use a different table_areas for the first page?
tables = camelot.read_pdf(file, flavor='stream', pages='all', edge_tol=50, row_tol=10)
first_df = remove_unnecessary_columns(tables[0].df)
index_start_first_table = get_row_index_start_first_table(first_df)
first_df = first_df.iloc[index_start_first_table:]
first_df.columns = ['Learning Resource', 'Duration (hrs)', 'Type']

dfs = []
dfs.append(first_df)
for table in tables[1:]:
    df = remove_unnecessary_columns(table.df)
    df.columns = ['Learning Resource', 'Duration (hrs)', 'Type']
    dfs.append(df)

concatenated_df = pd.concat(dfs, axis=0, ignore_index=True)
concatenated_df.to_csv('output.csv', index=False)
print(concatenated_df)

# tables.export('foo.csv', f='csv')  # json, excel, html


# camelot.plot(tables[0], kind='contour').show()
# Print the tables
# print(tables)
# for table in tables:
#     print('table.df', table.df)
#     print()
