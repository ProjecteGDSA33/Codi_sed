import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2
import time
import pandas as pnd
from sklearn.feature_extraction.text import TfidfVectorizer

t1 = time.time()

class Imatge:
  iden = ''     # identificador de la imatge
  tags = None   # llista dels tags
  sol = ''      # soluciÃ³ del fitxer de solucions

def calcula_svm (s,e):      # funció pel calcul de svm, on s es el supervector
    v_svm = [0] * len(s)
    for te in e:
        if te in s:
            index = s.index(te)
            v_svm[index] = 1
    return v_svm

  
# directori metadades xml
dir_xml = "C:\Users\IRENE\Documents\Metadades_imatges\sed2013_task2_dataset_train.xml"
# directori imatges jpg
dir_img = "C:\Users\IRENE\Documents\Metadades_imatges\SED2013_task2_photos1"
# direcotri solucions csv
dir_sol = "C:\Users\IRENE\Documents\Metadades_imatges\sed2013_task2_dataset_train_gs.csv"

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

for foto in root:
    imatge = Imatge()   # variable tipus Imatge
    imatge.tags = []    # inicialitzar les llistes
        
    id_tags = []        # variable individual per guardar el identificador i la llista det tags d'una
                            # foto en la pos [0] tenim el id, en la resta de pos tenim els tags
                            
    att_foto = foto.attrib      # tots els atributs de la imatge

    imatge.iden = att_foto["id"]

    eti_foto = foto.getchildren()
    tags = eti_foto[1].getchildren()    # entrem en l'etiqueta tags
        
    for tag in tags:
        imatge.tags.append(tag.text.encode('ascii','ignore')) # anem guardant els tags en la variable individual

    if imatge.iden+".jpg" in nom_imatges:    
        sol_trobada = sol_imatges[sol_imatges.document_id == imatge.iden]
        # un cop ja guardem la solucio l'eliminem de la llista per reduir temps de cerca
        sol_imatges = sol_imatges[sol_imatges.document_id != imatge.iden]
        imatge.sol = sol_trobada.event_type.to_string().split()[-1].encode('ascii','ignore')   # guardem la solucio en la imatge
            
        # creem el supervector
        for tag in imatge.tags:
            supervector.add(tag)
        if imatge.sol == 'concert':
            for tag in imatge.tags:
                concert.add(tag)
        elif imatge.sol == 'conference':
            for tag in imatge.tags:
                conference.add(tag)
        elif imatge.sol == 'exhibition':
            for tag in imatge.tags:
                exhibition.add(tag)
        elif imatge.sol == 'fashion':
            for tag in imatge.tags:
                fashion.add(tag)
        elif imatge.sol == 'other':
            for tag in imatge.tags:
                other.add(tag)
        elif imatge.sol == 'protest':
            for tag in imatge.tags:
                protest.add(tag)
        elif imatge.sol == 'sports':
            for tag in imatge.tags:
                sports.add(tag)
        elif imatge.sol == 'theater_dance':
            for tag in imatge.tags:
                theater_dance.add(tag)
        elif imatge.sol == 'non_event':
            for tag in imatge.tags:
                non_event.add(tag)
        # fi de la creacio del supervector

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

concert_svm = calcula_svm(supervector,concert)
conference_svm = calcula_svm(supervector,conference)
exhibition_svm = calcula_svm(supervector,exhibition)
fashion_svm = calcula_svm(supervector,fashion)
other_svm = calcula_svm(supervector,other)
protest_svm = calcula_svm(supervector,protest)
sports_svm = calcula_svm(supervector,sports)
theater_dance_svm = calcula_svm(supervector,theater_dance)
non_event_svm = calcula_svm(supervector,non_event)

text_file = open("supervector.txt", "w")
text_file_svm = open("supervector_svm.txt", "w")
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

text_file_svm.write("concert")
for i in concert_svm:
    text_file_svm.write(" "+str(i))
text_file_svm.write("\n")
text_file_svm.write("conference")
for i in conference_svm:
    text_file_svm.write(" "+str(i))
text_file_svm.write("\n")
text_file_svm.write("exhibition")
for i in exhibition_svm:
    text_file_svm.write(" "+str(i))
text_file_svm.write("\n")
text_file_svm.write("fashion")
for i in fashion_svm:
    text_file_svm.write(" "+str(i))
text_file_svm.write("\n")
text_file_svm.write("other")
for i in other_svm:
    text_file_svm.write(" "+str(i))
text_file_svm.write("\n")
text_file_svm.write("protest")
for i in protest_svm:
    text_file_svm.write(" "+str(i))
text_file_svm.write("\n")
text_file_svm.write("sports")
for i in sports_svm:
    text_file_svm.write(" "+str(i))
text_file_svm.write("\n")
text_file_svm.write("theater_dance")
for i in theater_dance_svm:
    text_file_svm.write(" "+str(i))
text_file_svm.write("\n")
text_file_svm.write("non_event")
for i in non_event_svm:
    text_file_svm.write(" "+str(i))
text_file_svm.write("\n")

text_file_svm.close()

print (time.time()-t1)
