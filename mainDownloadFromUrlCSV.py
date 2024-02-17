import csv
from urllib.request import urlopen
import urllib.request
from os.path import basename

with open('UrlToDownload.CSV') as f:
    reader=csv.reader (f,delimiter=',')
   
    print(reader)
    for url in reader:
        print('Downloading:', url[0])
        response = urllib.request.urlopen(url[0])
        print (response)
        filename = basename(response.url[0])
        print(filename)
        urllib.request.urlretrieve(url[0], filename)
       


   