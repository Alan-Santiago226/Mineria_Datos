import pandas as pd

df = pd.read_csv('videogamesales/vgsales_clean.csv')

def Maximos(opcion): #Ventas por año
    ventas = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
    for venta in ventas:
        cambios = pd.DataFrame()
        df_2 = df.groupby(['Publisher','Year'])[venta].agg(['max', 'mean']).reset_index()
        df_2.rename(columns = {'max' : 'MAX_Sales', 'mean' : 'Mean_Sales'}, inplace = True)

        if cambios.empty:
            cambios = df_2
        else:
            cambios = pd.merge(cambios, df_2, on=['Publisher', 'Year'])

    if opcion == 1: # Por Desarolladora
        print(cambios.head)
        cambios.to_csv('videogamesales/vgsales_DS.csv', header = True, index = False)
    else: # Top ventas por año 
        if opcion == 2: #(más reciente a más antiguo)
            cambios = cambios.sort_values(by = ['Year','MAX_Sales'], ascending = [False, False])
        else:   #(más antiguo a más reciente)
            cambios = cambios.sort_values(by = ['Year','MAX_Sales'], ascending = [True, False])
        print(cambios.head)
        cambios.to_csv('videogamesales/vgsales_DS.csv', header = True, index = False)


def Generos(opcion): 
    ventas = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']   
    if opcion == 1:
        for venta in ventas:
            cambios = pd.DataFrame()
            df_3 = df.groupby(['Genre','Year'])[venta].agg(['max', 'mean']).reset_index()
            df_3.rename(columns = {'max' : 'MAX_Sales', 'mean' : 'Mean_Sales'}, inplace = True)
            if cambios.empty:
                cambios = df_3
            else:
                cambios = pd.merge(cambios, df_3, on=['Genre','Year'])
        cambios = cambios.sort_values(by = ['Year','MAX_Sales'], ascending = [True, False])

    else:
        for venta in ventas:
            cambios = pd.DataFrame()
            df_3 = df.groupby(['Platform','Genre'])[venta].agg(['max', 'mean']).reset_index()
            df_3.rename(columns = {'max' : 'MAX_Sales', 'mean' : 'Mean_Sales'}, inplace = True)
            if cambios.empty:
                cambios = df_3
            else:
                cambios = pd.merge(cambios, df_3, on=['Platform','Genre'])
        cambios = cambios.sort_values(by = ['Genre','MAX_Sales'], ascending = [False, False])

    print('\n\n')
    print(cambios.head)
    cambios.to_csv('videogamesales/vgsales_BestGenres.csv', header = True, index = False)


def Tendencia(): #Mejores videojuegos historicamente 
    df['Total_Sales'] = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].sum(axis=1)
    mejores_ventas = df.groupby(['Year'])['Total_Sales'].idxmax()   #El mejor por año, si se le agrega más (columnas), categorizara más secciones
    Top = df.loc[mejores_ventas, ['Year', 'Platform', 'Genre', 'Name', 'Total_Sales']]
    print('\n\n')
    print(Top.head)
    Top.to_csv('videogamesales/vgsales_BestGames.csv', header = True, index = False)

    



Maximos(2) # Tiene hasta 3 opciones de ordenamiento    1 - Ventas máximas por desarrolladora  ;  2 - Top ventas por año descendente  ;  3 - Top ventas por año ascendente
Generos(1) # Tiene 2 opciones de ordenamiento      1 - Generos a traves de los años  ;  2 - Generos en plataformas
Tendencia() # Por defecto, mejores videojuegos historicamente
