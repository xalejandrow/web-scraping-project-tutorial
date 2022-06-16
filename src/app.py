# your app code here
#print("Hello world")

import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3
import tqdm
import numpy as np

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
pag = requests.get(url)

#print(pag)
pag_text = pag.text
#print(pag_text)

text_beaut = BeautifulSoup(pag_text,"html.parser")

#print(text_beaut)
#type(text_beaut)

tablas = text_beaut.find_all("table")
#print(tablas)
print(len(tablas))
#print(tablas[0])

id_tabla_quarter = None

for i in range(len(tablas)):
    if "Tesla Quarterly Revenue" in str(tablas[i]):
        id_tabla_quarter = i
        print("Tabla encontrada: ", id_tabla_quarter)
        break

#print(tablas[id_tabla_quarter])

tabla_quarter = tablas[id_tabla_quarter]

tabla_quarter_body = tabla_quarter.tbody

#print(tabla_quarter_body)
lista_tr = tabla_quarter_body.find_all("tr")

#print(lista_tr)

revenue_ls = []

for tr in tqdm.tqdm(lista_tr):
    all_tr = tr.find_all("td")
    date = all_tr[0].text
    revenue = all_tr[1].text
    revenue_ls.append([date, revenue])
    # print("*"*10)
    # #print(tr)
    # print(len(date), date)
    # print(date[0].text,date[1].text)

#Saco el $ del revenue

print(revenue_ls)

revenue_df = pd.DataFrame(revenue_ls, columns=["Date","Revenue"])
#print(revenue_df)
print(revenue_df.head())


# elemento = revenue_df["Revenue"][0]
# #print(elemento[1:])
# elemento = elemento.replace("$","")
# elemento = elemento.replace(",",".")
# print(elemento.replace("$",""))
# print(elemento.replace(",","."))



def preProcessRevenue(texto):
    texto = texto.replace("$","")
    texto = texto.replace(",",".")
    if texto == "":
        return np.NaN
    return float(texto)


# val = preProcessRevenue(revenue_df["Revenue"][0])
# print(val)

revenue_df["Revenue"] = revenue_df["Revenue"].apply(preProcessRevenue)
print(revenue_df)

revenue_df = revenue_df.dropna(subset="Revenue")
# revenue_df = revenue_df.dropna()
print(revenue_df)

#Elimino los índices para guardar el CSV
revenue_df.to_csv("revenue_df.csv", index=None)

# Generamos la tabla en sqlite3

connection = sqlite3.Connection("Tesla.db")

c = connection.cursor()

# Create table
c.execute('''CREATE TABLE revenue
(Date, Revenue)''')

records = revenue_df.to_records(index=False)
list_of_tuples = list(records)

# Insert the values
c.executemany('INSERT INTO revenue VALUES (?,?)', list_of_tuples)
# Save (commit) the changes
connection.commit()



# c = connection.cursor()

# # Create table
# c.execute('''CREATE TABLE revenue
#              (Date, Revenue)''')

# records = revenue_df.to_records(index=False)
# list_of_tuples = list(records)

# # Insert the values
# c.executemany('INSERT INTO revenue VALUES (?,?)', list_of_tuples)
# # Save (commit) the changes
# connection.commit()


# print(date[0])
# print(type(date[0]))
# print(type(date[0].text))

# class Point: 

#     def __init__(self,x,y):
#         self.x = x
#         self.y = y
    
#     def __repr__(self):
#         return f"Point({self.x},{self.y})"

# my_point = Point(1,2)
# type(str(my_point))
