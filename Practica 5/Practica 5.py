import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from matplotlib import pyplot as pyp
from tabulate import tabulate

Clean = "videogamesales/vgsales_BestGenres.csv"
Clean_2 = "videogamesales/vgsales_DS.csv"

def print_tabulate(df: pd.DataFrame) -> None:
    print(tabulate(df, headers = df.columns, tablefmt='orgtbl'))

def anova(fn: str, fn_2: str):
    df_clean = pd.read_csv(fn)
    #df_clean_2 = pd.read_csv(fn_2)
    df_clean_2 = Limpieza_2(fn_2)
    df_by_genre = df_clean.groupby(["Genre", "Year"])[["MAX_Sales"]].aggregate(pd.DataFrame.sum)
    df_by_pub = df_clean_2.groupby(["Publisher", "Year"])[["MAX_Sales"]].aggregate(pd.DataFrame.sum)

    df_by_pub.reset_index(inplace=True)
    df_by_pub.set_index("Publisher", inplace=False)

    #print(df_by_pub.head())

    complement = df_by_pub['Publisher'].unique()

    df_by_genre.reset_index(inplace=True)
    df_by_genre.set_index("Year", inplace=True)

    #df_by_pub.boxplot(by= 'Publisher', figsize=(36,18))
    #pyp.xticks(rotation = 90)
    #pyp.savefig("videogamesales/Anova/BPL_Publishers.PNG")
    #pyp.close

    

    for i, Pub in enumerate(complement):
        df_complement = df_by_pub[df_by_pub['Publisher'] == Pub]
        fig, axs = pyp.subplots(figsize =(12,6))

        axs.boxplot(df_complement['MAX_Sales'], vert=False)
        #axs.set_title(Pub)
        axs.set_title(f'Max sales {Pub}', y=1.02)
        pyp.xlabel('MAX_Sales')
        pyp.grid(True)
        pyp.savefig(f"videogamesales/Anova/BPL_Publisher_{Pub}.PNG")
        pyp.close()

    #df_by_pub.reset_index(inplace=True)
    df_aux = df_by_pub.drop(['Year'], axis=1)
    print(df_aux.head())
    print("\n")

    modl = ols("MAX_Sales ~ Publisher", data=df_aux).fit()
    anova_df = sm.stats.anova_lm(modl,  typ= 2)
    if anova_df["PR(>F)"][0] < 0.005:
        print("Hay diferencias\n")
        print(anova_df)
    else:
        print("No hay diferencias")
        print(anova_df)    


def Limpieza_2(file_name: str) -> None:
    df = pd.read_csv(file_name)
    Mantenimiento = 'Publisher'
    df[Mantenimiento] = df[Mantenimiento].apply(limpiar_slashes)
    df.to_csv('videogamesales/vgsales_DS_Clean.csv', index=False)
    return df

def limpiar_slashes(Publisher):
    return Publisher.replace('//', '')

anova(Clean, Clean_2)

#Se tarda en aproximado 2 - 5 minutos en procesar los boxplot generando 578 de 2731
#Se limpió (nuevamente) el csv de compañias por error de slashes "//"
