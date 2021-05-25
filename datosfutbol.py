import requests
import numpy as np
from datetime import  date, timedelta
import xml.etree.ElementTree as ET
from operator import itemgetter
torneos = ["Champions","Copa America", "Copa Paraguay", "Eliminatorias","España","Italia","Libertadores","Paraguay","Premier League","Recopa","Sudamericana"]
torneovec =["champions","copaamerica", "copaparaguay", "eliminatorias","espana","italia","libertadores","paraguay","premierleague","recopa","sudamericana"]
x='-1111'
while int(x) < 0  or int(x) > 10:
    print("Seleccionar torneo:")
    for i in range(len(torneos)):
        print(str(i) + "- " + torneos[i])
    x = input()
    

torneo = torneovec[int(x)]
url = 'https://editorialdenegocios.com/datafactory/xml/es/'+ torneo +'/deportes.futbol.'+ torneo +'.posiciones.xml'
web = requests.get(url)
root = ET.fromstring(web.text)
titulocsv = f'datos{torneo}.csv'
f = open(titulocsv,'w')
print(f)
if torneo == 'champions' or torneo == 'libertadores' or torneo == 'sudamericana':
    
    root[:] = sorted(root, key=lambda child: (child.tag,child.get('zona')))
    
    for c in root:
        c[:] = sorted(c, key=lambda child: (child.tag,child.get('puntos')))



f.write('Tabla de posiciones ; PJ ; G ; E ; P ; GF ; GC ; DF ; Pts;\n')
contador=0
for i in root.findall('equipo'):
    if contador % 4 == 0 and (torneo == 'champions' or torneo == 'libertadores' or torneo == 'sudamericana'):
        f.write(i.get("zona") + "\n")
    
    f.write(i.find('nombre').text + ';' + i.find('jugados').text + ';' + i.find('ganados').text + ';' + i.find('empatados').text + ';' + i.find('perdidos').text +  ';' + i.find('golesfavor').text + ';' + i.find('golescontra').text + ';' + i.find('difgol').text + ';' + i.find('puntos').text +'\n')
    contador = contador + 1



url = 'https://editorialdenegocios.com/datafactory/xml/es/'+ torneo +'/deportes.futbol.'+ torneo +'.fixture.xml'
web = requests.get(url)
root = ET.fromstring(web.text)

for i in root.findall("fecha"):
    
    if(i.get('estado')=='ultima'):
        f.write(i.get('nombrenivel')+"\n")
        for j in i:
            if(j.find('local')!= None):
                f.write(f'{j.find("local").text};{j.find("goleslocal").text}; - ;{j.find("golesvisitante").text} ;{j.find("visitante").text}\n') 
    if(i.get('estado')=='actual'):
        f.write(i.get('nombrenivel')+"\n")
        for j in i:
            if(j.find('local')!= None):
                if (j.find('estado').attrib['id'] == '2'):
                    f.write(f'{j.find("local").text};{j.find("goleslocal").text}; - ;{j.find("golesvisitante").text} ;{j.find("visitante").text} - {j.get("tipo")}; - ;fecha:{j.get("fecha")[6:8]}/{j.get("fecha")[4:6]}/{j.get("fecha")[0:4]}; hora:{j.get("hora")}\n')
                else:
                    f.write(f'{j.find("local").text};; vs ;;{j.find("visitante").text} - {j.get("tipo")}; - ;fecha:{j.get("fecha")[6:8]}/{j.get("fecha")[4:6]}/{j.get("fecha")[0:4]}; hora:{j.get("hora")}\n')


goleadores = np.array([0,-1,0],dtype=object)
url = 'https://editorialdenegocios.com/datafactory/xml/es/'+ torneo +'/deportes.futbol.'+ torneo +'.jugadores.estadisticas.xml'
web = requests.get(url)
root = ET.fromstring(web.text)
for i in root.findall('Tournament/Players/Player'):
    text = [i.attrib['name'] + " " + i.attrib['lastName'], int(i.find('Goals').attrib['total']) , i.attrib['currentTeam']]
    goleadores = np.vstack([goleadores,np.asarray(text,object)])    
f.write("\n Goleadores \n")
goleadores = sorted(goleadores, key=lambda a_entry: a_entry[1], reverse=True)
for i in range(5):
    a=goleadores[i]
    f.write(a[0]+ ";" +str(a[1]) + ";" + a[2] +"\n")
asistencias = np.array([0,-1,0],dtype=object)
f.write('\n Asistencias \n')
for i in root.findall('Tournament/Players/Player'):
    text = [i.attrib['name'] + " " + i.attrib['lastName'], int(i.find('GoalAssistances').attrib['total']) , i.attrib['currentTeam']]
    asistencias = np.vstack([asistencias,np.asarray(text,object)])   


asistencias = sorted(asistencias, key=lambda a_entry: a_entry[1], reverse=True)

for i in range(5):
    a=asistencias[i]
    f.write(a[0]+ ";" +str(a[1]) + ";" + a[2] + "\n")  


pases = np.array([0,-1,0,0, 0],dtype=object)
f.write('\n Pases \n')
for i in root.findall('Tournament/Players/Player'):
    text = [i.attrib['name'] + " " + i.attrib['lastName'], int(i.find('Passes').attrib['successful']) , int(i.find('Passes').attrib['total']), float(i.find('Passes').attrib['effectiveness'])  , i.attrib['currentTeam']]
    pases = np.vstack([pases,np.asarray(text,object)])    

pases = sorted(pases, key=lambda a_entry: a_entry[2], reverse=True)
pases10 = np.array([0,-1,0,0, 0],dtype=object)
for i in range(11):
    pases10 = np.vstack([pases10,pases[i]])  
    pases10[i][3] = int(pases10[i][3])
    
pases10 = sorted(pases10, key=lambda a_entry: a_entry[3], reverse=True)


for i in range(10):
    a=pases10[i]
    f.write(a[0]+ ";" +str(a[1]) + ";" + str(a[2]) + ";" + str(a[3]) + ";" + a[4] +"\n")

disparos = np.array([0,-1,0],dtype=object)
f.write('\n Disparos \n')
for i in root.findall('Tournament/Players/Player'):
    text = [i.attrib['name'] + " " + i.attrib['lastName'], int(i.find('Shots').attrib['total']) , i.attrib['currentTeam']]
    disparos = np.vstack([disparos,np.asarray(text,object)])   


disparos = sorted(disparos, key=lambda a_entry: a_entry[1], reverse=True)

for i in range(5):
    a=disparos[i]
    f.write(a[0]+ ";" +str(a[1]) + ";" + a[2] + "\n")    

recuperacion = np.array([0,-1,0],dtype=object)
f.write('\n Recuperacion \n')
for i in root.findall('Tournament/Players/Player'):
    text = [i.attrib['name'] + " " + i.attrib['lastName'], int(i.find('Stealing').attrib['total']) , i.attrib['currentTeam']]
    recuperacion = np.vstack([recuperacion,np.asarray(text,object)])   


recuperacion = sorted(recuperacion, key=lambda a_entry: a_entry[1], reverse=True)

for i in range(5):
    a=recuperacion[i]
    f.write(a[0]+ ";" +str(a[1]) + ";" + a[2] + "\n")  


faltas_com = np.array([0,-1,0],dtype=object)
f.write('\n Faltas Cometidas \n')
for i in root.findall('Tournament/Players/Player'):
    text = [i.attrib['name'] + " " + i.attrib['lastName'], int(i.find('Fouls').attrib['total']) , i.attrib['currentTeam']]
    faltas_com = np.vstack([faltas_com,np.asarray(text,object)])   


faltas_com = sorted(faltas_com, key=lambda a_entry: a_entry[1], reverse=True)

for i in range(5):
    a=faltas_com[i]
    f.write(a[0]+ ";" +str(a[1]) + ";" + a[2] + "\n")  

faltas_rec = np.array([0,-1,0],dtype=object)
f.write('\n Faltas Recibidas \n')
for i in root.findall('Tournament/Players/Player'):
    text = [i.attrib['name'] + " " + i.attrib['lastName'], int(i.find('FoulsOpponents').attrib['total']) , i.attrib['currentTeam']]
    faltas_rec = np.vstack([faltas_rec,np.asarray(text,object)])   


faltas_rec = sorted(faltas_rec, key=lambda a_entry: a_entry[1], reverse=True)

for i in range(5):
    a=faltas_rec[i]
    f.write(a[0]+ ";" +str(a[1]) + ";" + a[2] + "\n")  

tar_ama = np.array([0,-1,0],dtype=object)
f.write('\n Tarjetas Amarillas \n')
for i in root.findall('Tournament/Players/Player'):
    text = [i.attrib['name'] + " " + i.attrib['lastName'], int(i.find('YellowCards').attrib['total']) , i.attrib['currentTeam']]
    tar_ama = np.vstack([tar_ama,np.asarray(text,object)])   


tar_ama = sorted(tar_ama, key=lambda a_entry: a_entry[1], reverse=True)

for i in range(5):
    a=tar_ama[i]
    f.write(a[0]+ ";" +str(a[1]) + ";" + a[2] + "\n")  

tar_roj = np.array([0,-1,0],dtype=object)
f.write('\n Tarjetas Rojas \n')
for i in root.findall('Tournament/Players/Player'):
    text = [i.attrib['name'] + " " + i.attrib['lastName'], int(i.find('RedCards').attrib['total']) , i.attrib['currentTeam']]
    tar_roj = np.vstack([tar_roj,np.asarray(text,object)])   


tar_roj = sorted(tar_roj, key=lambda a_entry: a_entry[1], reverse=True)

for i in range(5):
    a=tar_roj[i]
    f.write(a[0]+ ";" +str(a[1]) + ";" + a[2] + "\n")  
