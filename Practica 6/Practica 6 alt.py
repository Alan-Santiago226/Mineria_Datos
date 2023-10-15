#Se importan las librerias a utilizar
import warnings
import pandas as pd # Estructura de datos
import numpy as np # Operaciones matematicas
import seaborn as sns

sns.set_style('darkgrid')

# Preparar Datos #
# Se extrae datos de un excel delimitado por comas #
datos = pd.read_csv(r"Modelo.csv")
datos2 = pd.read_csv(r"Modelo.csv")
print(datos.head())
#print(len(datos))

# Modelo de Regresion #
X = pd.DataFrame({"x0":[1 for _ in range(datos.shape[0])]})
Y = datos.iloc[:,0]
datos = datos.iloc[:,1:]
X = pd.concat([X,datos], axis=1)

# Operaciones #
xT_x = np.dot(np.array(X).transpose(),np.array(X))

inversa = np.linalg.inv(xT_x)

xT_y = np.dot(np.array(X).transpose(),Y)

invTx_Ty = np.dot(inversa,xT_y)

# Modelo extraido para interpretar la ecuación #

class modelo:
    def __init__(self,params,variables):
        self.params = params
        self.variables = variables
        self.equation = self.__createEquation(params,variables)
        self.labels = self.__dictEquation(params,variables)
        
    def __repr__(self):
        return "y = " + self.equation
    
    def __getitem__(self,key):
        return [str(self.labels[i])+(str(i) if i != "b" else "") for i in self.labels][key]
    
    def __createEquation(self,params,variables):
        modelEquation = ""
        for j,i in enumerate(params):
            modelEquation += (" + "+str(i) if i>0 else " - "+str(i)[1:]) + (variables[j-1] if j != 0 and j-1 < len(variables) else "")
        return modelEquation
    
    def __dictEquation(self,params,variables):
        modelDict = {}
        modelDict["b"] = params[0]
        for i,j in zip(params[1:],variables):
            modelDict[j] = i
        return modelDict
    
    def predict(self,X):
        """
        X: DataFrame
        
        return: np.array with predictions
        """
        bias = self.labels["b"]
        result = 0
        for i in list(self.labels.keys())[1:]:
            result += self.labels[i]*X[i]
        return np.array(result+bias)
        
    def evaluation(self,X,variables):
        """
        Evaluates the model with specific variables, if variables are the same as self.labels it is equivalent to model.predict
        """
        is_equal_to_predict = True
        variables = list(set(variables))
        for i in variables:
            if i not in list(self.labels.keys()):
                is_equal_to_predict = False
        
        if is_equal_to_predict:
            warnings.warn("variables = self.labels, it is recommended to use the predict method")
            
        result = 0
        for i in variables:
            if i != "b":
                result += self.labels[i]*X[i]
            else:
                result += self.labels[i]
        return np.array(result)

##
print("\n")
modelToPredict = modelo(invTx_Ty,list(datos.columns))
print("La curva de regresión lineal multiple de",datos2.columns[0] ,"es:")
print(modelToPredict)
print("\n")

# Intento de predición #
interacion = 1
while interacion == 1:
        numero = int(input("¿Desea predecir una regresión? 0-No 1-Si: "))
        resultado = 0
        Entrada = []
        while numero <0 or numero >1:
                print("Error -> Fuera de rango")
                numero = int(input("¿Desea predecir una regresión? 0-No 1-Si: "))
        if(numero == 1):
            total_columnas = len(datos.axes[1])
            for i in range(0,total_columnas+1,1):
                if(i == 0):
                    Entrada.append(1)
                else: 
                    print("Ingrese el dato de x",i,": ") 
                    n = eval(input())
                    Entrada.append(n)
            for i in range(0,total_columnas+1,1):
                resultado = resultado + (invTx_Ty[i]*Entrada[i])
            print("\ny =",resultado)
        else:
            print("Fin del programa")
            interacion = 0
        print("\n")
# Fin #     
#  #
