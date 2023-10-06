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

def Generos_Ventas(file_name: str) -> None:
    df = pd.read_csv(file_name)
    df_por_genero = df.groupby(["Genre", "Year"])[["MAX_Sales"]].aggregate(pd.DataFrame.mean)
    df_por_genero.reset_index(inplace=True)
    df_por_genero.set_index("Year", inplace=True)

    for gen in set(df_por_genero["Genre"]):
        plot_by_gen(df_por_genero, gen)

    df_aux = df.groupby(["Genre", "Year"])[['MAX_Sales']].mean().unstack()
    df_aux.plot(y = 'MAX_Sales', legend = False, figsize=(32,18))
    pyp.xticks(rotation=90)
    pyp.savefig("videogamesales/test-gen.png")
    pyp.close()


def plot_by_gen(df: pd.DataFrame, gen:str)->None:
    df[df["Genre"] == gen].plot(y = ["MAX_Sales"], figsize=(12,8))
    pyp.savefig(f"videogamesales/lt_{gen}.png")
    df[df["Genre"] == gen].boxplot(by = 'Genre', figsize=(12,8))
    pyp.savefig(f"videogamesales/bplt_{gen}.png")   

Ventas(Top, 1)
Generos_Ventas(Generos)
