import time
import pandas as pd
files = 'file.xlsx'
df = pd.read_excel(files, sheet_name='Hoja1', usecols="A")
list_barcode=df['Code-barres'].tolist()


# authentification
import discogs_client
d = discogs_client.Client('my_user_agent/1.0', user_token='token')

erreur=[]

def url(barcode):
    global objet_image
    #FIND RELEASE
    
    fbarcode=(str(barcode)).replace(" ", "")
    if fbarcode=="nan": return "wrong format / missing"
    
    
    ref=str(d.search(fbarcode, type="barcode").page(0))
    #EXTRACT release reference
    #release 
    if ref=="[]":
        erreur.append(barcode)
        return("not found  ",fbarcode)
    imaster=0
    ajust=0
    if ref.find("Master")==2:
        imaster=ref.find("Release")
        ajust=2
    l=[ref.find(" '"),ref.find(' "')]
    refdiscogs=ref[10+imaster-ajust:min([i for i in l if i > 0])+imaster]
    
    #EXTRACT IMAGE URL
    try:
        objet_image=d.release(refdiscogs).images[0]
    except TypeError:       #avoid releases without image"
        erreur.append(barcode)
        return(barcode,"  has no image")
    except Exception:        #avoid barcodes non registered in the data base
        if str(barcode).find("\xa0")==-1:
            erreur.append(barcode)
            return(barcode,"  not found  on discogs")           
    objet_diccionnaire=str(objet_image)
    i=objet_diccionnaire.find(".jpeg")+5
    j=objet_diccionnaire.find("'https")+1
    return(objet_diccionnaire[j:i])
moment=time.localtime().tm_sec+time.localtime().tm_min*60
momentb=moment+2
n=0
for n, barcode in enumerate(list_barcode,start=1):
    if n%20==0:
        delta=abs(momentb-moment)
        if delta<30:
            #print("PAUSE")
            time.sleep(61-delta)
            moment=time.localtime().tm_sec+time.localtime().tm_min*60
    print(url(barcode))
    momentb=time.localtime().tm_sec+time.localtime().tm_min*60
print("erreurs:",erreur) 
while 1:
    continue
