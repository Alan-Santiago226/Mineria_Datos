from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import random


def open_csv(path: str, Columna: str) -> str:
    df = pd.read_csv(path)
    contenido = df[Columna].astype(str).str.cat(sep=' ')
    return contenido
    
def custom(word, font_size, position, orientation, random_state=None, **kwargs):
    return f"#{random.randint(0, 255):02X}{random.randint(0, 255):02X}{random.randint(0, 255):02X}"

columnas = ["Publisher", "Platform", "Genre", "Name"]

for i in range(4): 
    all_words = ""
    #if i == 0:
     #   frase = open_csv("videogamesales/vgsales_clean_alt.csv", "Publisher")
    #elif i == 1:
     #   frase = open_csv("videogamesales/vgsales_clean_alt.csv", "Platform")
    #elif i == 2:
     #   frase = open_csv("videogamesales/vgsales_clean_alt.csv", "Genre")
    #elif i == 3:
     #   frase = open_csv("videogamesales/vgsales_clean_alt.csv", "Name")
    #else: 
     #   frase = open_csv("videogamesales/vgsales_clean_alt.csv", "Year")
    if 0 <= i < len(columnas):
        frase = open_csv("videogamesales/vgsales_clean_alt.csv",columnas[i])
    palabras = frase.rstrip().split(" ")

    Palabras_Comun = Counter(" ".join(palabras).split()).most_common(10)
    print(Palabras_Comun)
    # looping through all incidents and joining them to one text, to extract most common words
    for arg in palabras:
        tokens = arg.split()
        all_words += " ".join(tokens) + " "


    #print(all_words)
    wordcloud = WordCloud(
        background_color="white", color_func=custom, min_font_size=5, width=1600, height=800
    ).generate(all_words)

    # print(all_words)
    # plot the WordCloud image
    plt.close()
    plt.figure(figsize=(20, 10), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    # plt.show()
    plt.savefig(f"videogamesales/Nube/Word_cloud_{columnas[i]}.png",)
    plt.close()


# DEFINITIVO #

all_words = ""
Palabras_Comun = ""
for i in range(4):
    if 0 <= i < len(columnas):
        frase = open_csv("videogamesales/vgsales_clean_alt.csv",columnas[i])
        palabras = frase.rstrip().split(" ")
        for arg in palabras:
            tokens = arg.split()
            all_words += " ".join(tokens) + " "
    Palabras_Comun = Counter(" ".join(palabras).split()).most_common(10)

print(Palabras_Comun) 
# # looping through all incidents and joining them to one text, to extract most common words

#print(all_words)
wordcloud = WordCloud(
        background_color="white", min_font_size=5, width=1600, height=800
    ).generate(all_words)

# print(all_words)
# plot the WordCloud image
plt.close()
plt.figure(figsize=(20, 10), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

# plt.show()
plt.savefig("videogamesales/Nube/Word_cloud_definitive.png",)
plt.close()

