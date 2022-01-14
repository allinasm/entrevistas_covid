# ProgDS-2-20202-PAC4
Template repository for the PAC4/PEC4 of ProgDS-2 20202.

ANÀLISI D'ENTREVISTES I LA SEVA CREDIBILITAT

En aquest petit projecte es produeix una anàlisi del grau de preocupació
dels entrevistats en vers a diversos temes.

TAULA DE CONTINGUT:
--
* Fitxers del projecte
* Execució del projecte
* Testeig dels resultats
* Llicència

FITXERS DEL PROJECTE:
--
- main.py: desenvolupa el projecte
- utils.py: conté les funcions a cridar
- tests.py: conté el codi per testejar les funcions
- requirements.txt: llistat amb els mòduls necessaris per 
  desenvolupar el projecte.
- README.md: Instruccions per desenvolupar el projecte.

EXECUCIÓ DEL PROJECTE
--
Descomprimim els fitxers al directori on volem guardar el projecte.
Obrim el projecte amb un IDE com Pycharm i des de el fitxer main.py
podem executar el projecte sencer que ens mostrarà les respostes i 
gràfics corresponents a la PAC 4 de l'assignatura "Programació per a
la ciència de Dades" del Grau de Ciència de dades aplicada de la UOC.
Les crides executen les funcions de l'arxiu utils.py.
A requirements es troben especificats els mòduls necessaris per executar
el codi. Si no es visualitzen els plots a la consola, s'ha d'executar
'$ sudo apt-get install python3-tk' al terminal per poder carregar el
modul matplotlib amb l'opció de visualitzar-se per la consola.

TESTEIG DE RESULTATS
--
Executant tests.py es produeix el testeig de les funcions amb la 
llibreria unittest.
Per comprovar la cobertura del projecte executarem la llibreria coverage.py.
Des de la terminal del IDE executem '$ pip install coverage'.
Llavors '$ coverage run -m --source=. unittest tests.py', i seguidament
'$ coverage report' que ens mostrarà el % de cobertura dels arixus del projecte.

LLICÈNCIA
--
El codi d'aquest projecte és 'Open source', el que vol dir que l'usuari pot
fer ús lliure del contingut; copiar-lo, modificar-lo i/o redistribuir-lo.


