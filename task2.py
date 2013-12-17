# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET
import numpy as np
import time
import pandas as pnd
from sklearn import svm
import tfidf
import cv2

t1 = time.time()

def tradueix (class_predicted):
    if( class_predicted == [1] ): class_predicted = 'concert'
    elif( class_predicted == [2] ): class_predicted = 'conference'
    elif( class_predicted == [3] ): class_predicted = 'exhibition' 
    elif( class_predicted == [4] ): class_predicted = 'fashion'
    elif( class_predicted == [5] ): class_predicted = 'other'
    elif( class_predicted == [6] ): class_predicted = 'protest' 
    elif( class_predicted == [7] ): class_predicted = 'sports'
    elif( class_predicted == [8] ): class_predicted = 'theater_dance'
    elif( class_predicted == [9] ): class_predicted = 'no_event'



event=['concert','conference','exhibition','fashion','other','protest','sports','theater_dance','no_event']

# classe Imatge -les llistes no es poden inicialitzar dintre la class!
class Imatge:
  iden = ""     # identificador de la imatge
  tags = None   # llista dels tags
  SIFT = None   # [kp][des]
  sol = ''      # solucio del fitxer de solucions
  sol_prop = '' # solucio proposada despres d'aplicar el classificador
  
# directori metadades xml
dir_xml = "C:/Users/marc/Documents/GDSA/Projecte/train/metadata/xml/sed2013_task2_dataset_train.xml"
# directori imatges jpg
dir_img = "C:/Users/marc/Documents/GDSA/Projecte/Imatges/class"
# direcotri solucions csv
dir_sol = "C:/Users/marc/Documents/GDSA/Projecte/train/annotation/sed2013_task2_dataset_train_gs.csv"
# directori supervector
dir_sup = "C:/Users/marc/supervector_task2.txt" # # # # # # # # # # # # # # # <- ATENCIO: Utilitzar el fitxer de supervector_task2

# llegim dades supervector # # # # # # # # #
data = open(dir_sup,'r').read().split('\n') #
classificacio = data[0].split(" ")[1:]      #   <- PART NOVA (llegim els index de les imatges ha classificar)
supervector = data[0].split(" ")[1:]        #   s'han canviat les linies ha llegir perque tenim una nova linia
concert = data[1].split(" ")[1:]            #   on indica els index de les imatges a classificar
conference = data[2].split(" ")[1:]         #
exhibition = data[3].split(" ")[1:]         #
fashion = data[4].split(" ")[1:]            #
other = data[5].split(" ")[1:]              #
protest = data[6].split(" ")[1:]            #
sports = data[7].split(" ")[1:]             #
theater_dance = data[8].split(" ")[1:]      #
non_event = data[9].split(" ")[1:]         #
# fi # # # # # # # # # # # # # # # # # # # #

# inicialitzacio tfidf # # # # # # # # # # # # # #
table = tfidf.tfidf()                            #
table.addDocument("concert", concert)            #
table.addDocument("conference", conference)      #
table.addDocument("exhibition", exhibition)      #
table.addDocument("fashion", fashion)            #
table.addDocument("other", other)                #
table.addDocument("protest", protest)            #
table.addDocument("sports",sports)               #
table.addDocument("theater_dance",theater_dance) #
table.addDocument("non_event", non_event)        #
# fi # # # # # # # # # # # # # # # # # # # # # # #

 
nT = len(supervector)   # numero de tags totals

nom_imatges = os.listdir(dir_img)

sol_imatges = pnd.read_csv(dir_sol,sep='\t')

llista_imatges = []     # variable on guardem totes les imatges - ampliar en cas
                        # de consultar les imatges d'una CARPETA

tree = ET.parse(dir_xml)

root = tree.getroot()   # l'etiqueta "arrel" es <photos> en el nostre xml

classificacio = [int(i) for i in classificacio] # # # # <- PART NOVA (convertim strings en ints)

for i in classificacio: # # # # # # ARA JA NO MIREM LA CARPETA D'IMATGES, NOMÉS METADADES
    
    foto = root[i]
    
    imatge = Imatge()   # variable tipus Imatge
    imatge.tags = []    # inicialitzar les llistes
    imatge.SIFT = []
        
    id_tags = []        # variable individual per guardar el identificador i la llista det tags d'una
                            # foto en la pos [0] tenim el id, en la resta de pos tenim els tags
                            
    att_foto = foto.attrib      # tots els atributs de la imatge

    imatge.iden = att_foto["id"]

    eti_foto = foto.getchildren()
    tags = eti_foto[1].getchildren()    # entrem en l'etiqueta tags
        
    for tag in tags:
        if (tag.text.encode('ascii','ignore').isdigit() == False and len(tag.text.encode('ascii','ignore')) > 1):
            imatge.tags.append(tag.text.encode('ascii','ignore'))      # anem guardant els tags en la variable individual   
        # un cop recorregut una foto la guardem en la llista d'imatges, nomes si
        # el nom de la imatge esta en la carpeta
            
    # busquem la solcuio en el csv
    sol_trobada = sol_imatges[sol_imatges.document_id == imatge.iden]
    sol_imatges = sol_imatges[sol_imatges.document_id != imatge.iden] # un cop ja guardem la soluciÃ³ l'eliminem de la llista per reduir temps de cerca
    imatge.sol = sol_trobada.event_type.to_string().split()[-1].encode('ascii','ignore')   # guardem la soluciÃ³ en la imatge
            
    llista_imatges.append(imatge)   # guardem la imatge en la llista
                      


# llegim les imatges de test i guardem la id per tal de donar la solucio

text_id_sol_tfidf = open("Results_task2_1.txt", "wb")   # # # # # # # PART NOVA, canviar el numero final per les diferents validacions creuades
text_id_sol_tfidf.write("document_id event_type \n")

sol_prop = 0

for i in llista_imatges:

#    new_llindar = event_decision.similarities(i.tags)
    sol = table.similarities(i.tags)
#    if ( sol[8][1] > 0.37 ): 
#        sol_prop = sol[8][0] 
#    else:
#        sol=sol[:-1]
    m = 0
    for s in sol:    
        if (m < s[1]):
            m = s[1]
            sol_prop = s[0]
        if( sol_prop == ' ' ): sol_prop = sol[4][0]

    i.sol_prop = str(sol_prop)            
    text_id_sol_tfidf.write(str(i.iden)+" "+str(sol_prop))
    text_id_sol_tfidf.write("\n")

text_id_sol_tfidf.close()

print (time.time()-t1)
