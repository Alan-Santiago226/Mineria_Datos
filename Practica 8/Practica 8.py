import matplotlib.pyplot as plt
import statsmodels.api as sm
import numbers
import pandas as pd
from tabulate import tabulate
from typing import Tuple

def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt="orgtbl"))

def transform_variable(df: pd.DataFrame, x:str)->pd.Series:
    if not df.empty and isinstance(df[x].iloc[0], numbers.Number):
        return df[x] # type: pd.Series
    else:
        return pd.Series([i for i in range(0, len(df[x]))], dtype='float64')
    
def plt_lr(df: pd.DataFrame, x:str, y: str, m: float, b: float, r2: float, r2_adj: float, low_band: float, hi_band: float, colors: Tuple[str,str]):
    fixed_x = transform_variable(df, x)
    plt.scatter(df[x], df[y], color='black', s=10)
    plt.plot(df[x],[ m * x + b for _, x in fixed_x.items()], color=colors[0])
    plt.fill_between(df[x],[ m * x  + low_band for _, x in fixed_x.items()],[ m * x + hi_band for _, x in fixed_x.items()], alpha=0.25, color=colors[1])


def linear_regression(df: pd.DataFrame, x:str, y: str, z:int, a:str, inicio: str, final: str)->None:
    df_filtrada = df[(pd.to_datetime(df[x]) >= inicio) & (pd.to_datetime(df[x]) <= final)]
    df_filtrada.reset_index(drop=True, inplace=True)
    print_tabulate(df_filtrada.head())
    fixed_x = transform_variable(df_filtrada, x)
    model= sm.OLS(df_filtrada[y],sm.add_constant(fixed_x)).fit()
    print(model.summary())
    coef = pd.read_html(model.summary().tables[1].as_html(),header=0,index_col=0)[0]['coef']
    plt.figure(figsize=(10,6))
    df_filtrada.plot(x=x,y=y, kind='scatter') 
    plt.plot(df_filtrada[x],[pd.DataFrame.mean(df_filtrada[y]) for _ in fixed_x.items()], color='green')
    #plt.plot(df_by_sales[x],[ coef.values[1] * x + coef.values[0] for _, x in fixed_x.items()], color='red')
    plt.plot(df_filtrada[x][:len(fixed_x)], [coef.values[1] * x + coef.values[0] for _, x in fixed_x.items()], color='red')
    #plt.bar(df_filtrada[x][:len(fixed_x)], df_filtrada[y][:len(fixed_x)], alpha=0.5, color='blue', label='Barras Azules')
    if (z == 1):
        plt_lr(df_filtrada, x, y, coef.values[1], coef.values[0], model.rsquared, model.rsquared_adj,
            model.conf_int().iloc[1, 0], model.conf_int().iloc[1, 1], ('red', 'orange'))
        plt_lr(df_filtrada.tail(2),x,y,coef.values[1], coef.values[0], model.rsquared, model.rsquared_adj,
            model.conf_int().iloc[1, 0], model.conf_int().iloc[1, 1], ('red', 'purple'))        
        plt_lr(df_filtrada.head(2),x,y,coef.values[1], coef.values[0], model.rsquared, model.rsquared_adj,
           model.conf_int().iloc[1, 0], model.conf_int().iloc[1, 1], ('blue', 'blue'))  
    elif (z == 4):
        plt_lr(df_filtrada, x, y, coef.values[1], coef.values[0], model.rsquared, model.rsquared_adj,
            model.conf_int().iloc[1, 0], model.conf_int().iloc[1, 1], ('red', 'orange'))
        plt_lr(df_filtrada.tail(3),x,y,coef.values[1], coef.values[0], model.rsquared, model.rsquared_adj,
            model.conf_int().iloc[1, 0], model.conf_int().iloc[1, 1], ('red', 'purple'))
        plt_lr(df_filtrada.head(2),x,y,coef.values[1], coef.values[0], model.rsquared, model.rsquared_adj,
           model.conf_int().iloc[1, 0], model.conf_int().iloc[1, 1], ('blue', 'blue'))           
    else:
        plt_lr(df_filtrada, x, y, coef.values[1], coef.values[0], model.rsquared, model.rsquared_adj,
            model.conf_int().iloc[0, 1], model.conf_int().iloc[0, 0], ('red', 'orange'))
        plt_lr(df_filtrada.tail(3),x,y,coef.values[1], coef.values[0], model.rsquared, model.rsquared_adj,
            model.conf_int().iloc[0, 1], model.conf_int().iloc[0, 0], ('red', 'purple'))
        plt_lr(df_filtrada.head(2),x,y,coef.values[1], coef.values[0], model.rsquared, model.rsquared_adj,
           model.conf_int().iloc[0, 1], model.conf_int().iloc[0, 0], ('blue', 'blue'))   
        
    
     
    plt.title(f'{a}')
    plt.xticks(rotation=90)
    plt.tight_layout()  
    plt.savefig(f'videogamesales/Linear Regression/lr_{y}_{x}_in_range_{z}.png')
    plt.close()


csv = ['videogamesales/vgsales_BestGames.csv','videogamesales/vgsales_BestGenres.csv','videogamesales/vgsales_DS_Clean.csv']
ctr = 0

inicio = '01-01-2013'
final = '01-01-2021'

for archivos in csv:
    df = pd.read_csv(archivos)
    if ctr == 1:
        inicio = '01-01-2004'
        final = '01-01-2006'
    elif ctr == 2:
        inicio = '01-01-1996'
        final = '01-01-2000'

    if archivos == 'videogamesales/vgsales_BestGames.csv':
        df_by_sales = df.groupby("Year")[["Total_Sales"]].aggregate(pd.DataFrame.mean)
    else:
        df_by_sales = df.groupby("Year").aggregate(Total_Sales=pd.NamedAgg(column="MAX_Sales", aggfunc=pd.DataFrame.mean))
    
    df_by_sales.reset_index(inplace=True)
    label = archivos[:-3]
    print(label)
    print_tabulate(df_by_sales.head())
    linear_regression(df_by_sales, "Year", "Total_Sales", ctr, label, inicio, final)
    print("\n")
    ctr = ctr + 1

#csv_extra = 'videogamesales/vgsales_clean_alt.csv'
#df_x = pd.read_csv(csv_extra)
#linear_regression(df_x, "Year", "Global_Sales", 4, label, '01-01-2013', '01-01-2021')
#print("\n")
