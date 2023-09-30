import numpy as np
import pandas as pd
from matplotlib import pyplot as pyp

#Leemos los csv de la practica anterior (3)
Top='videogamesales/vgsales_BestGames.csv'
Generos = 'videogamesales/vgsales_BestGenres.csv'
Compañias = 'videogamesales/vgsales_DS.csv'

#print(df_1.head)
#print(df_2.head)
#print(df_3.head)

def Ventas(file_name: str, opcion: int) -> None:
    df = pd.read_csv(file_name)
    df['Year'] = pd.to_datetime( df['Year'], format = "%Y-%m-%d")
    df['Years'] = df['Year'].dt.year
    #ax = df.boxplot(column="Total_Sales", by='Years', figsize=(36,12))
    #ax.set_ylabel("Total Sales")
    #ax.set_title("Sales by Best Games")
    if opcion == 1:
        Del = "1900"
        df = df.loc[df['Years'] != int(Del)]
        print("Se descarta los juegos con año desconocido")
    else: 
        print("Se mantienen los juego con año desconocido")
    pyp.figure(figsize=(10,6))
    pyp.bar(df['Years'], df['Total_Sales'])
    pyp.savefig("videogamesales/test.png")
    pyp.close()
    

Ventas(Top, 1)
