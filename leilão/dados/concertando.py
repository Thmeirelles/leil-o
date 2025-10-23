# import csv
# with open('Planilha sem título - Página1.csv', 'r', encoding='utf-8') as file:
#     reader = csv.reader("tabela.csv")
#     rows = list(reader)
# processed_rows = []
# for row in rows:
#     processed_row = []
#     for value in row:
#         if value.startswith('R$'):
#             clean_value = value.replace('R$', '').replace('.', '').replace(' ', '')
#             temp_value = clean_value.replace(',', '.')
#             try:
#                 numeric_value = float(temp_value)
#                 formatted_value = f'{numeric_value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
#                 processed_row.append(formatted_value)
#             except ValueError:
#                 processed_row.append(value)
#         else:
#             processed_row.append(value)
#     processed_rows.append(processed_row)

# with open('planilha_formatada.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerows(processed_rows)
# print("'planilha_formatada.csv', Ok!")