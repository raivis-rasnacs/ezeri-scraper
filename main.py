import requests
import bs4
from pprint import pprint

url = "https://lv.wikipedia.org/wiki/Latvijas_ezeru_uzskaitījums"

# Lasa datus no Wiki
data = requests.get(url)
html = bs4.BeautifulSoup(data.text, 'html.parser')

tabula = html.select("table")[0]
ezeri = tabula.select("tr")

# Ieraksta datus failā
with open("ezeri.txt", "a", encoding="UTF-8") as f:
    for ezers in ezeri[1:]:
        lauki = ezers.select("td")
        f.write(lauki[2].text.strip()+"-"+lauki[6].text.strip()+"\n")

# Ielasa datus no faila sarakstā
ezeri = []
with open("ezeri.txt", "r", encoding="utf-8") as f:
    for rinda in f:
        rindas_dati = rinda.split("-")
        if rindas_dati[1] != "\n":
            ezers = {"Nosaukums":rindas_dati[0],
                    "Dziļums":float(rindas_dati[1].strip().replace(",", "."))}
            ezeri.append(ezers)

# Burbuļkārto ezerus pēc dziļuma
for i, ezers in enumerate(ezeri):
    for j, ezers in enumerate(ezeri):
        if j < len(ezeri) - 1:
            if ezeri[j]["Dziļums"] > ezeri[j + 1]["Dziļums"]:
                ezeri[j], ezeri[j + 1] = ezeri[j + 1], ezeri[j]

# Izdrukā sakārtotus datus
pprint(ezeri)
