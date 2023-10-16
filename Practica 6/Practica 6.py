import matplotlib.pyplot as plt
import statsmodels.api as sm
import numbers
import pandas as pd
from tabulate import tabulate


def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt="orgtbl"))

def transform_variable(df: pd.DataFrame, x:str)->pd.Series:
    if isinstance(df[x][0], numbers.Number):
        return df[x] # type: pd.Series
    else:
        return pd.Series([i for i in range(0, len(df[x]))])


def linear_regression(df: pd.DataFrame, x:str, y: str, z:int, a:str)->None:
    fixed_x = transform_variable(df, x)
    model= sm.OLS(df[y],sm.add_constant(fixed_x)).fit()
    print(model.summary())
    coef = pd.read_html(model.summary().tables[1].as_html(),header=0,index_col=0)[0]['coef']
    plt.figure(figsize=(10,6))
    df.plot(x=x,y=y, kind='scatter') 
    plt.plot(df[x],[pd.DataFrame.mean(df[y]) for _ in fixed_x.items()], color='green')
    plt.plot(df_by_sales[x],[ coef.values[1] * x + coef.values[0] for _, x in fixed_x.items()], color='red')
    plt.title(f'{a}')
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()  
    plt.savefig(f'videogamesales/Linear Regression/lr_{y}_{x}_{z}.png')
    plt.close()


csv = ['videogamesales/vgsales_BestGames.csv','videogamesales/vgsales_BestGenres.csv','videogamesales/vgsales_DS_Clean.csv']
ctr = 0

for archivos in csv:
    df = pd.read_csv(archivos)
    if archivos == 'videogamesales/vgsales_BestGames.csv':
        df_by_sales = df.groupby("Year")[["Total_Sales"]].aggregate(pd.DataFrame.mean)
    else:
        df_by_sales = df.groupby("Year").aggregate(Total_Sales=pd.NamedAgg(column="MAX_Sales", aggfunc=pd.DataFrame.mean))
    
    df_by_sales.reset_index(inplace=True)
    label = archivos[:-3]
    print(label)
    print_tabulate(df_by_sales.head())
    linear_regression(df_by_sales, "Year", "Total_Sales", ctr, label)
    print("\n")
    ctr = ctr + 1
