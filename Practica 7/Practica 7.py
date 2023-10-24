import pandas as pd
import matplotlib.pyplot as pyp

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

df = pd.read_csv('videogamesales/vgsales_clean_alt.csv')
df = df.drop(['Rank'], axis = 1)
#print(df.head())

def fit_sales(df: pd.DataFrame) -> None:
    ventas = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
    #df_max = pd.DataFrame()    #Columas duplicadas que no se como arreglar, algo similar ocurre en la practica 3
    
    for venta in ventas:
        df_max = pd.DataFrame()
        df_aux = df.groupby(['Name','Platform'])[venta].agg(['sum']).reset_index()
        df_aux.rename(columns = {'sum' : 'MAX_Sales'}, inplace = True)

        if df_max.empty:
            df_max = df_aux
        else:
            df_max = pd.merge(df_max, df_aux, on=['Name','Platform'])
    
    
    #df_max['MAX_Sales'] = df_max[ventas].sum(axis=1)
    #df_max = df.groupby('Name')['MAX_Sales']

    df_max_perfect = df.merge(df_max)
    df_max_perfect = df_max_perfect.drop(ventas, axis = 1) # Haciendo esto me di cuenta HASTA AHORITA que la columna Global_Sales ya representaba las ventas maximas, aunque eso no afecto los trabajos anteriores. Curioso

    #df_max_perfect = df_max_perfect.sort_values(by = ['MAX_Sales'], ascending = False)
    #print(df_max.head())

    return df_max_perfect

def KNN(df:pd.DataFrame) -> None:
    le = LabelEncoder() #Utilizamos LE para calcular la "distancia" de las columnas que no son valores numericos para convertirlos a tal
    df['Genre'] = le.fit_transform(df['Genre'])
    df['Platform'] = le.fit_transform(df['Platform'])
    df['Year'] = le.fit_transform(df['Year'])
    df['Publisher'] = le.fit_transform(df['Publisher'])

    X = df[['Platform', 'Year', 'Genre', 'Publisher']]
    #print(X.head())
    y = (df['MAX_Sales'] * 10).round(0).astype(int) #Que desvario me dio convertir los continuos a cerrados
    #print(y.head())
    

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    k = 10  
    knn = KNeighborsClassifier(n_neighbors=k) # Al convertir en valores las columnas de X y cambiar el tipo de variable a entero en Y, por ende, se utiliza este y no Regression

    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)

    for ajuste in X.columns:
        pyp.figure(figsize=(10,6))
        pyp.scatter(X_test[ajuste], y_test, label = 'Successful')
        pyp.scatter(X_test[ajuste], y_pred, label = 'Missful')
        pyp.xlabel(ajuste)
        pyp.ylabel('Max_Sales')
        pyp.title(f'K-Nearest Neighbors for {ajuste}')
        pyp.legend()
        pyp.savefig(f"videogamesales/KNN/test-{ajuste}.png")

    accuracy = accuracy_score(y_test, y_pred)
    print(f'Precisión del modelo: {accuracy * 100:.2f}%')
    
    """
    pyp.figure(figsize=(10, 6))
    n_ejemplos = 10 
    for i in range(n_ejemplos):
        pyp.subplot(2, 5, i + 1)
        pyp.imshow(np.random.rand(8, 8), cmap='gray')
        pyp.title(f'Predicción: {y_pred[i]}')
        pyp.axis('off')

    pyp.savefig("videogamesales/KNN/test.png")
    """

df = fit_sales(df)
#print(df.head())
#df.to_csv('videogamesales/vgsales_TEST.csv', header = True, index = False)
KNN(df)
#Me da gracia porque soy el claro ejemplo de combinar palabras en ingles y español tal y como se expuso en clase de IA, lo admito, fue culpa de Stack overflow
#Ver line 32
