# This is a test with given parameters and fields

from Bio import Entrez, SeqIO
import os
Entrez.email = "eliasvera2013@gmail.com" # cambia esto
# Entrez.esearch se encarga de buscar en la base de datos del NCBI
"""
La variable parámetro se puede editar según la siguiente lista https://www.ncbi.nlm.nih.gov/books/NBK49540/
Generalmente, se añadirá 'Parámetro'[Campo al que corresponde] seguido de una proposición AND (y), OR (o), NOT (no)
Ir cambiando los parámetros 'País' y los campos [Publication Date] (puede ser en los intervalos que se prefieran)
Si no se encuentra ningún resultado con los parámetros ejecutados se devolverá una lista vacía -> []. Puede deberse a conflictos con el país o año
"""
organism = "Dengue virus"
country = "Brazil" # cambiar esto (sensible)
start_date = "2010" # esto
end_date = "2015" # y esto
min_length = "10000"
max_length = "20000"
parámetros = '((((("{0}"[Organism] OR ("{0}"[Organism] OR {0}[All Fields])) AND complete[All Fields] AND genome[All Fields])\
        AND country=[All Fields] AND "{1}"[Text Word]) AND ("{2}"[PDAT] : "{3}"[PDAT])) AND {4}[SLEN] : {5}[SLEN])\
        NOT UNVERIFIED[Title]'.format(organism, country, start_date, end_date, min_length, max_length)
""" 
Entrez.esearch parámetros:
db: base de datos a utilizar --no tocar
term: términos de búsqueda --no tocar, editar la variable 'parámetros'
retstart: punto inicial de datos que devolverá --ir editando a medida que se obtienen los datos
retmax: cantidad de datos que devolvera (retmax = 20 devuelve 20 resultados) --editar este parámetro (NO RECOMENDABLE ESTABLECER RETMAX > 100)
"""
##############################
##### Ignorar esta parte ##### 
##############################
handle = Entrez.esearch(db="nucleotide", term=parámetros, sort="pub_date")
rec_list = Entrez.read(handle)
handle.close()
cantidad_resultados = rec_list["Count"]
##############################
###### Seguir ignorando ######
##############################

# Programa principal
comienzo_lectura = "1"
cantidad_lecturas = "5"
handle = Entrez.esearch(db="nucleotide", term=parámetros, retstart=comienzo_lectura, retmax=cantidad_lecturas, sort="pub_date")
# El código anterior devuelve un handle, que se lee utilizando Entrez.read
rec_list = Entrez.read(handle)
handle.close()
id_list = rec_list['IdList']

print("Usted está realizando una búsqueda con los siguientes parámetros: \n" + 
    "País: " + country + "\n" + "Publication date: " + start_date + '-' + end_date)
print("Resultados: " + str(cantidad_resultados))
print("Los ID leídos fueron: \n" + str(id_list))

# Entrez.efetch sirve para buscar cada id conseguido anteriormente y devolvernos los contenidos de esos id en formato gb = 'genbank'
# Se puede cambiar el formato a fasta haciendo rettype='fasta'
id_procesados = []
for id in id_list:
    seq_handle = Entrez.efetch(db="nucleotide", id=id, rettype="fasta", retmode="text")
    filename = "seq_fasta_" + country + "_" + start_date + "-" + end_date + ".txt"
    if not os.path.isfile(filename): # si no existe ningún documento con el nombre de "filename" crear uno nuevo
        with open(filename, "w") as file:
            fst_format = seq_handle.read()
            fst_format = fst_format.replace(">", "")
            file.write("> " + start_date + "-" + end_date + " | " + fst_format)
    else:
        with open(filename, "a") as file:
            fst_format = seq_handle.read()
            fst_format = fst_format.replace(">", "")
            file.write("> " + start_date + "-" + end_date + " | " + fst_format)
    id_procesados.append(id)
    seq_handle.close()

print("Los ID procesados fueron: \n" + str(id_procesados))
print("Terminado y guardado, a continuación, el archivo se abrirá automáticamente.")
print("La ubicación del .txt es la misma que la de este programa (probablemente descargas)")
os.startfile(filename)