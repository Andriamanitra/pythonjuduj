from xml.etree import ElementTree as ET
import random

PITUUS = 94110
sanalista = ET.parse("kotus-sanalista_v1.xml")
juuri = sanalista.getroot()


# palauttaa num:nnen sanatietueen
def st(num):
    return juuri[num-1]


# palauttaa num:nnen sanan
def sana(num):
    return st(num)[0].text


# palauttaa sanan taivutusluokan tai False jos kyseessä on yhdyssana
def taivutus(num):
    try:
        tn = st(num).find("t").find("tn").text
        return int(tn)
    except AttributeError:
        return False


# palauttaa astevaihtelun stringin tai False
def astevaihtelu(num):
    av = st(num).find("t").find("av").text
    if av:
        return av
    else:
        return False


# palauttaa True jos sana on homonyymi, False jos ei
def homonyymi(num):
    if st(num).find("hn").text:
        return True
    else:
        return False


# palauttaa satunnaisen sanan
def satunnaissana():
    sana_num = random.randint(1, PITUUS)
    return sana(sana_num)


# palauttaa satunnaisen verbin, ei kuitenkaan yhdyssanaa
def verbi():
    sana_num = random.randint(1, PITUUS)
    while taivutus(sana_num) < 52 or taivutus(sana_num) > 78:
        sana_num = random.randint(1, PITUUS)
    return sana(sana_num)


# palauttaa satunnaisen nominin, ei kuitenkaan yhdyssanaa
def nomini():
    sana_num = random.randint(1, PITUUS)
    while taivutus(sana_num) > 51 or taivutus(sana_num) == 0:
        sana_num = random.randint(1, PITUUS)
    return sana(sana_num)


# palauttaa satunnaisen yhdyssanan
def yhdyssana():
    sana_num = random.randint(1, PITUUS)
    while taivutus(sana_num) != 0:
        sana_num = random.randint(1, PITUUS)
    return sana(sana_num)


# palauttaa sanan numeron (1-94110) tai False jos sanaa ei löytynyt
def etsi_sana(etsittava):
    j = 0
    i = PITUUS-1
    while i >= j:
        mid = (i+j)//2
        if etsittava == juuri[mid][0].text:
            return mid+1
        elif etsittava > juuri[mid][0].text:
            j = mid+1
        else:
            i = mid-1
    return False
