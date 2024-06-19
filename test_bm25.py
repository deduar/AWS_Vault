import difflib

a = 'CASA PRETO'
b = 'Mamma Roma'

print(difflib.SequenceMatcher(a=a.lower(), b=b.lower()).ratio())


# adidas,adidases www.adidas.es,0.0
# adidas,adidases www.adidas.es,0.0
# alberto cerdán,peluqueria ortega y gasse,0.0