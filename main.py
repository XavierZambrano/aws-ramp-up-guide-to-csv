import camelot

file = "input/Ramp-Up_Guide_Developer.pdf"

# use a different table_areas for the first page?
tables = camelot.read_pdf(file, flavor='stream', pages='1', edge_tol=50, row_tol=10)
print(tables[0].df)
tables.export('foo.csv', f='csv')  # json, excel, html


# camelot.plot(tables[0], kind='contour').show()
# Print the tables
# print(tables)
# for table in tables:
#     print('table.df', table.df)
#     print()