import xml.etree.ElementTree as ET
import os 
import pandas as pd

dir='DATI'
#INPUT_KML_FILE = "MyTracks_Lonetti_20231127181706.kml"
# Itera attraverso le righe del file KML
lista=[['Name','Total distance','Total time','Max speed','Data']]
for filename in os.listdir(dir):       
    if filename.endswith(".kml"):
        file_path = os.path.join(dir, filename)
        print(filename)
        dati_da_inserire=[]
        tree = ET.parse(file_path)
        root = tree.getroot()
               
        for element in root.iter():
            if element.text is not None and element.text.strip() != "":
                # Divide il testo in righe e stampa ciascuna riga
                lines = element.text.splitlines()
                 # Start from the first cell below the headers.                            
                for line in lines:
                    #print(line)
                    if line[0:5]=='Name:':
                        dati_da_inserire.append(line[6:])
                    if line[0:15]=='Total distance:':
                        dati_da_inserire.append(line[16:])
                    if line[0:11]=='Total time:':
                        dati_da_inserire.append(line[12:])
                    if line[0:10]=='Max speed:':
                        dati_da_inserire.append(line[11:])
                    if line[0:9]=='Recorded:':
                        dati_da_inserire.append(line[10:])            
        lista.append(dati_da_inserire)
#print(dati_da_inserire)
print (lista)
df=pd.DataFrame(lista)
writer=pd.ExcelWriter('dati.xlsx',engine='xlsxwriter')
df.to_excel(writer, sheet_name='Foglio1', index=False, header=False)
    
writer.close()     
                    