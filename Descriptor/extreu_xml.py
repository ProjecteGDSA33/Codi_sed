# -*- coding: cp1252 -*-
import xml.etree.ElementTree as ET

# ruta fitxer metadades
fitxer_xml = "C:/Users/marc/Documents/GDSA/Projecte/train/metadata/xml/sed2013_task2_dataset_train.xml"

llista_meta = []    # variable on guardem tots els id i els tags de totes les fotos

tree = ET.parse(fitxer_xml)

root = tree.getroot()   # l'etiqueta "arrel" es <photos> en el nostre xml

for foto in root:
    
    id_tags = []        # variable individual per guardar el identificador i la llista det tags d'una
                        # foto en la pos [0] tenim el id, en la resta de pos tenim els tags
                        
    att_foto = foto.attrib
    id_foto = att_foto["id"]    # aqui tenim el identificador de la foto
    id_tags.append(id_foto)     # guardem en la variable global el id de la foto, que estará en la pos [0]
    eti_foto = foto.getchildren()
    tags = eti_foto[1].getchildren()    # entrem en l'etiqueta tags
    print id_foto,  # comprovacio
    
    for tag in tags:
        
        nom_tag = tag.text
        id_tags.append(nom_tag)      # anem guardant els tags en la variable individual
        if tag == tags[-1]:
            print nom_tag   # comprovacio
        else:
            print nom_tag,  # comprovacio
        
    # un cop recorregut una foto la guardem en la llista de metadades
    llista_meta.append(id_tags)
