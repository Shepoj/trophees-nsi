#-----------------------------------------Initialisation des bibliothèques--------------------------------

import socket
import threading
import sys

#------------------------------------------Initialisation de la connexion---------------------------------

maPrise = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nomOrdi = socket.gethostname()
ipOrdi = socket.gethostbyname(nomOrdi)

print('adresse serveur :', ipOrdi)                                                          
print('='*50)

maPrise.bind((ipOrdi, 10444)) 
maPrise.listen(1)                                           
lesClients=[]
clientsIds={}

#-----------Définition du Thread, distribution des messages et traitement des déconnexions-----------

def threaded(c):
    while True:
        data = c.recv(1024)
        if data.decode()=='disconnected':
            lesClients.pop(clientsIds[c])
            clientsIds.pop(c)
            c.close()
            sys.exit()
            for ref2 in lesClients:
                ref2.send("Un utilisateur a déconnecté")
                clientsIds[ref2]-=1
            print(data)
        else:
            for ref2 in lesClients:
                ref2.send(data)
            print(data)
    c.close()

#------------------------------------Entrée des différents clients---------------------------------------

while True :
        refClient, ipClient = maPrise.accept()
        print('-'*20+' '+str(ipClient)+str(refClient)+' '+'-'*20)
        lesClients.append(refClient)
        clientsIds[refClient]=len(lesClients)-1
        threading.Thread(target=threaded, args=(refClient,)).start()

maPrise.close() 
print('FIN')
