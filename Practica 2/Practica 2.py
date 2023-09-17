import pandas as pd


df = pd.read_csv('videogamesales/vgsales.csv')

#Print(df.isnull().sum())

null_values = df.isnull().sum().to_frame(name='totals').query('totals > 0')
null_values = null_values[null_values > 0]
#nulls = null_values.sum(axis=0)
nulls = null_values['totals'].sum()

print("La suma de los valores nulos en el dataset es de: ",nulls)

if(nulls > 0): # En casos de que existan valores nulos
    df_new = df
    means = df.mean(numeric_only= True)
    #print(means)
    df_new['Year'].fillna( 1900 , inplace= True) #Fechas no encontradas
    df_new['Publisher'].fillna("Unknown", inplace = True) #Se colocó en ingles para concordar con el dataset
    df_new.fillna(means) #Nulos numericos 
    null_values = df.isnull().sum().to_frame(name='totals').query('totals > 0')
    null_values = null_values[null_values > 0]
    #nulls = null_values.sum(axis=0)
    nulls = null_values['totals'].sum()
    #df_new['Publisher'] = df_new.fillna("Desconocido", inplace = True) #Empresas no encontradas
   
    if nulls == 0:
        print('Valores nulos limpiados')
    else:
        print("Existen valores nulos que no se limpuaron, verifica con tu proveedor de datatset xd")
else: # En caso de no encontrar valores nulos
    print("No hay valores nulos por limpiar")


df_new['Year'] = pd.to_datetime(df_new['Year'], format='%Y')
print("\n")
print("La fecha del dataset ahora esta en el formato YYYY-MM-DD")
print(df_new['Year'].head())

df_new.to_csv('videogamesales/vgsales_clean.csv', header = True, index = False)
