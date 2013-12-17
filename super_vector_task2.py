# -*- coding: cp1252 -*-
import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2
import pandas as pnd
import random # # # # # # # # # # # # PART NOVA
from sklearn.feature_extraction.text import TfidfVectorizer

class Imatge:
  iden = ''     # identificador de la imatge
  tags = None   # llista dels tags
  sol = ''      # soluciÃ³ del fitxer de solucions

  
# directori metadades xml
dir_xml = "C:/Users/marc/Documents/GDSA/Projecte/train/metadata/xml/sed2013_task2_dataset_train.xml"
# directori imatges jpg
dir_img = "C:/Users/marc/Documents/GDSA/Projecte/Imatges/class"
# direcotri solucions csv
dir_sol = "C:/Users/marc/Documents/GDSA/Projecte/train/annotation/sed2013_task2_dataset_train_gs.csv"

nom_imatges = os.listdir(dir_img) 

sol_imatges = pnd.read_csv(dir_sol,sep='\t')

# recordar posar totes les imatges en la carpeta!
supervector = set()
concert = set()
conference = set()
exhibition = set()
fashion = set()
other = set()
protest = set()
sports = set()
theater_dance = set()
non_event = set()
# fi de les variables del supervector

tree = ET.parse(dir_xml)

root = tree.getroot()   # l'etiqueta "arrel" es <photos> en el nostre xml

# # # # # # # # # # # # PART NOVA # # # # # # # # # # # #
total = range(len(root))                                #
entrenament = random.sample(total,len(root)*70/100)     #
classificacio = list(set(total) - set(entrenament))     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

for i in entrenament: # # # # PART NOVA
    
    foto = root[i]
    
    imatge = Imatge()   # variable tipus Imatge
    imatge.tags = []    # inicialitzar les llistes
        
    id_tags = []        # variable individual per guardar el identificador i la llista det tags d'una
                        # foto en la pos [0] tenim el id, en la resta de pos tenim els tags
                            
    att_foto = foto.attrib      # tots els atributs de la imatge

    imatge.iden = att_foto["id"]

    eti_foto = foto.getchildren()
    tags = eti_foto[1].getchildren()    # entrem en l'etiqueta tags
        
    for tag in tags:
        if (tag.text.encode('ascii','ignore').isdigit() == False and len(tag.text.encode('ascii','ignore')) > 1): # # # # # PART NOVA
            imatge.tags.append(tag.text.encode('ascii','ignore'))      # anem guardant els tags en la variable individual

    sol_trobada = sol_imatges[sol_imatges.document_id == imatge.iden]
    # un cop ja guardem la soluciÃ³ l'eliminem de la llista per reduir temps de cerca
    sol_imatges = sol_imatges[sol_imatges.document_id != imatge.iden]
    imatge.sol = sol_trobada.event_type.to_string().split()[-1].encode('ascii','ignore')   # guardem la soluciÃ³ en la imatge
            
    # creem el supervector
    for tag in imatge.tags:
        if (tag.isdigit() == False and len(tag) > 1):
            supervector.add(tag)
    if imatge.sol == 'concert':
        for tag in imatge.tags:
            if (tag.isdigit() == False and len(tag) > 1):
                concert.add(tag)
    elif imatge.sol == 'conference':
        for tag in imatge.tags:
            if (tag.isdigit() == False and len(tag) > 1):
                conference.add(tag)
    elif imatge.sol == 'exhibition':
        for tag in imatge.tags:
            if (tag.isdigit() == False and len(tag) > 1):
                exhibition.add(tag)
    elif imatge.sol == 'fashion':
        for tag in imatge.tags:
            if (tag.isdigit() == False and len(tag) > 1):
                fashion.add(tag)
    elif imatge.sol == 'other':
        for tag in imatge.tags:
            if (tag.isdigit() == False and len(tag) > 1):
                other.add(tag)
    elif imatge.sol == 'protest':
        for tag in imatge.tags:
            if (tag.isdigit() == False and len(tag) > 1):
                protest.add(tag)
    elif imatge.sol == 'sports':
        for tag in imatge.tags:
            if (tag.isdigit() == False and len(tag) > 1):
                sports.add(tag)
    elif imatge.sol == 'theater_dance':
        for tag in imatge.tags:
            if (tag.isdigit() == False and len(tag) > 1):
                theater_dance.add(tag)
    elif imatge.sol == 'non_event':
        for tag in imatge.tags:
            if (tag.isdigit() == False and len(tag) > 1):
                non_event.add(tag)
    # fi de la creacio del supervector
    i += 1

#ordenem alfabeticament i guardem en el .txt
supervector = sorted(supervector)
concert = sorted(concert)
conference = sorted(conference)
exhibition = sorted(exhibition)
fashion = sorted(fashion)
other = sorted(other)
protest = sorted(protest)
sports = sorted(sports)
theater_dance = sorted(theater_dance)
non_event = sorted(non_event)
text_file = open("supervector_task2.txt", "w")

# # # # # # PART NOVA # # # # # # #
for i in classificacio:           #
    text_file.write(" "+str(i))   #
text_file.write("\n")             #
# # # # # # # # # # # # # # # # # # 

text_file.write("supervector")
for i in supervector:
    text_file.write(" "+i)
text_file.write("\n")
text_file.write("concert")
for i in concert:
    text_file.write(" "+i)
text_file.write("\n")
text_file.write("conference")
for i in conference:
    text_file.write(" "+i)
text_file.write("\n")
text_file.write("exhibition")
for i in exhibition:
    text_file.write(" "+i)
text_file.write("\n")
text_file.write("fashion")
for i in fashion:
    text_file.write(" "+i)
text_file.write("\n")
text_file.write("other")
for i in other:
    text_file.write(" "+i)
text_file.write("\n")
text_file.write("protest")
for i in protest:
    text_file.write(" "+i)
text_file.write("\n")
text_file.write("sports")
for i in sports:
    text_file.write(" "+i)
text_file.write("\n")
text_file.write("theater_dance")
for i in theater_dance:
    text_file.write(" "+i)
text_file.write("\n")
text_file.write("non_event")
for i in non_event:
    text_file.write(" "+i)
text_file.close()
