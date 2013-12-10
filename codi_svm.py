import os
import xml.etree.ElementTree as ET
import numpy as np
import time
import pandas as pnd
from sklearn import svm
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



event=['concert','conference','exhibition','fashion','other','protest','sports','sports','theater_dance','no_event']
def calcula_svm (s,e):      # funció pel calcul de svm, on s es el supervector
    v_svm = [0] * len(s)
    for te in e:
        if te in s:
            index = s.index(te)
            v_svm[index] = 1
    return v_svm

# classe Imatge -les llistes no es poden inicialitzar dintre la class!
class Imatge:
  iden = ""     # identificador de la imatge
  tags = None   # llista dels tags
  tags_svm = None
  SIFT = None   # [kp][des]
  sol = ''      # solució del fitxer de solucions
  sol_prop = '' # solució proposada despres d'aplicar el classificador
  
# directori metadades xml
dir_xml = "C:\Users\IRENE\Documents\Metadades_imatges\sed2013_task2_dataset_train.xml"
# directori imatges jpg
dir_img = "C:\Users\IRENE\Documents\Metadades_imatges\SED2013_task2_photos2"
#dir_img = "C:\Users\IRENE\Documents\Metadades_imatges\TEST_IMAGE"
# direcotri solucions csv
dir_sol = "C:\Users\IRENE\Documents\Metadades_imatges\sed2013_task2_dataset_train_gs.csv"
# directori supervector
dir_sup = "C:/Users/IRENE/supervector.txt"

# llegim dades supervector # # # # # # # # #
data = open(dir_sup,'r').read().split('\n') #
supervector = data[0].split(" ")[1:]        #
concert = data[1].split(" ")[1:]            #
conference = data[2].split(" ")[1:]         #
exhibition = data[3].split(" ")[1:]         #
fashion = data[4].split(" ")[1:]            #
other = data[5].split(" ")[1:]              #
protest = data[6].split(" ")[1:]            #
sports = data[7].split(" ")[1:]             #
theater_dance = data[8].split(" ")[1:]      #
non_event = data[9].split(" ")[1:]          #
# fi # # # # # # # # # # # # # # # # # # # #

nT = len(supervector)   # numero de tags totals

nom_imatges = os.listdir(dir_img)

sol_imatges = pnd.read_csv(dir_sol,sep='\t')

llista_imatges = []     # variable on guardem totes les imatges - ampliar en cas
                        # de consultar les imatges d'una CARPETA

tree = ET.parse(dir_xml)

root = tree.getroot()   # l'etiqueta "arrel" es <photos> en el nostre xml

for foto in root:
    if len(llista_imatges) < len(nom_imatges):
        imatge = Imatge()   # variable tipus Imatge
        imatge.tags = []    # inicialitzar les llistes
        imatge.tags_svm = [0] * nT    # llista de zeros del tamany de supervector
        imatge.SIFT = []
        
        id_tags = []        # variable individual per guardar el identificador i la llista det tags d'una
                            # foto en la pos [0] tenim el id, en la resta de pos tenim els tags
                            
        att_foto = foto.attrib      # tots els atributs de la imatge

        imatge.iden = att_foto["id"]

        eti_foto = foto.getchildren()
        tags = eti_foto[1].getchildren()    # entrem en l'etiqueta tags
        
        for tag in tags:
            imatge.tags.append(tag.text.encode('ascii','ignore'))      # anem guardant els tags en la variable individual

        # un cop recorregut una foto la guardem en la llista d'imatges, nomes si
        # el nom de la imatge esta en la carpeta
        if imatge.iden+".jpg" in nom_imatges:
            
            # apliquem SIFT en la imatge   
            #img = cv2.imread(directori+"/"+imatge.iden+".jpg")
            #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                
            #sift = cv2.SIFT()
            #kp, des = sift.detectAndCompute(gray,None)
            #kp = sift.detect(gray,None)                 # kp = llista dels keypoints
            
            #img=cv2.drawKeypoints(gray,kp)
            
            #cv2.imwrite(imatge.iden+"_SIFT.jpg",img)    # visualitzem el resultat
            # fi d'aplicar SIFT  
            
            # guardem els resultats en la Imatge
            #imatge.SIFT.append(kp)
            #imatge.SIFT.append(des)
            
            # busquem la solcuio en el csv
            sol_trobada = sol_imatges[sol_imatges.document_id == imatge.iden]
            sol_imatges = sol_imatges[sol_imatges.document_id != imatge.iden] # un cop ja guardem la solució l'eliminem de la llista per reduir temps de cerca
            imatge.sol = sol_trobada.event_type.to_string().split()[-1].encode('ascii','ignore')   # guardem la solució en la imatge

            # calculem tags_svm
            imatge.tags_svm = calcula_svm(supervector,imatge.tags)
            
            #i = 0
            #while i < len(imatge.tags):
            #    if imatge.tags[i] in supervector:
            #        index = supervector.index(imatge.tags[i])
            #        imatge.tags_svm[index] = 1
            #        i = i + 1
                
            llista_imatges.append(imatge)   # guardem la imatge en la llista
                      
# # # # # # # # # # # # # # # # # #

#supervector_svm = [1] * nT    # vector amb 1, no se si es necessari pel svm :P
#concert_svm = calcula_svm(supervector,concert)
#conference_svm = calcula_svm(supervector,conference)
#exhibition_svm = calcula_svm(supervector,exhibition)
#fashion_svm = calcula_svm(supervector,fashion)
#other_svm = calcula_svm(supervector,other)
#protest_svm = calcula_svm(supervector,protest)
#sports_svm = calcula_svm(supervector,sports)
#theater_dance_svm = calcula_svm(supervector,theater_dance)
#non_event_svm = calcula_svm(supervector,non_event)

dir_sup_svm = "C:/Users/IRENE/supervector_svm.txt"
# llegim dades binaries supervector # # # # # # # # #
data = open(dir_sup_svm,'r').read().split('\n') #
#supervector = data[0].split(" ")[1:]        #
concert = data[0].split(" ")[1:]            #
conference = data[1].split(" ")[1:]         #
exhibition = data[2].split(" ")[1:]         #
fashion = data[3].split(" ")[1:]            #
other = data[4].split(" ")[1:]              #
protest = data[5].split(" ")[1:]            #
sports = data[6].split(" ")[1:]             #
theater_dance = data[7].split(" ")[1:]      #
non_event = data[8].split(" ")[1:]          #
# fi # # # # # # # # # # # # # # # # # # # #

mostres = [concert,conference,exhibition,fashion,other,protest,sports,theater_dance,non_event]
#tipo_evento = ['concert', 'conference', 'exhibition', 'fashion', 'other', 'protest', 'sports', 'theater_dance', 'no_event'] 
tipus_event = [1,2,3,4,5,6,7,8,9] # en este ejemplo hay solo cinco pero para cubrir cada evento es necesario un numero


# crear una variable de tipus de svm
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=1.0, probability = True).fit(mostres, tipus_event) # li pasem dos arrais un amb mostres


# llegim les imatges de test i guardem la id per tal de donar la solució

text_id_sol = open("id_sol.txt", "w")

for i in llista_imatges:
        
    class_predicted = rbf_svc.predict(i.tags_svm)

    decision = rbf_svc.decision_function(i.tags_svm)

    text_id_sol.write(str(i.iden)+" "+str(event[class_predicted - 1]))
    text_id_sol.write("\n")
    
text_id_sol.close()
print (time.time()-t1)
