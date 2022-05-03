#-----------------------------------------Initialisation des bibliothèques--------------------------------

from tkinter import*
from tkinter import messagebox
import random
import socket
from time import*
import threading

#-------------------Définition des fonctions qui aideront la fenêtre d'identification---------------------

firstclick = True
ipclick = True

def on_entry_click(event):       
    global firstclick
    if firstclick:
        firstclick = False
        nomi.delete(0, "end")

def ipclick(event):       
    global ipclick
    if ipclick:
        ipclick = False
        ipi.delete(0, "end")

def entree():
    global cond
    print("a")
    if nomi.get()!='Pseudo...' and nomi.get()!='':
        print("b")
        monnom=nomi.get()
        ip=ipi.get()
        win.destroy()
        loupe(monnom,ip)


#-----------------------------Mise en place de la fenêtre d'identification------------------------------

win=Tk()
win.title('Identification')
win.iconbitmap('./logo.ico')
nomi=Entry(win,text="test",width=100)
ipi=Entry(win,text="aaaa",width=100)
bout=Button(win, text="Entrer", command=entree)
nomi.insert(0, 'Pseudo...')
ipi.insert(0, 'Ip du serveur ?')
nomi.bind('<FocusIn>', on_entry_click)
ipi.bind('<FocusIn>', ipclick)

nomi.pack()
ipi.pack()
bout.pack()

#----------------------------------Création de la fenêtre de chat---------------------------------------

def loupe(monnom,ip):
    W=50
    L=500
    opened=True
    class App(Tk):
        def __init__(self):
            Tk.__init__(self)
            self.title('Blanket')
            self.iconbitmap('./logo.ico')
            """self.canvas=Canvas(width=W,height=L)
            self.canvas.pack()"""
            self.entree=Entry()
            self.entree.bind('<Return>',self.action)
            self.entree.pack(side=BOTTOM)
            self.listbox=Listbox(self,width=W)
            self.listbox.pack(side = LEFT, fill = BOTH)
        
            self.scrollbar = Scrollbar(self)
            self.scrollbar.pack(side = RIGHT, fill = BOTH)
            self.listbox.insert(END,"Bienvenue sur le chat, "+monnom)
            self.listbox.config(yscrollcommand = self.scrollbar.set)
            self.scrollbar.config(command = self.listbox.yview)

#------------------------------------------Initialisation de la connexion-------------------------------

            vox = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            hote = ip
            port = 10444

            self.name = monnom
                
            vox.connect((hote, port))
            self.sock=vox

#--------------------------Lancement du processus de réception des messages----------------------------
            
            self._fred=threading.Thread(target=self.recevoir)
            self._fred.start()
            self.m=[]

#-------------------------------Affichage des messages dans la boîte de chat---------------------------
            
        def affiche(self,text):
            if opened:
                self.listbox.insert(END,text)
                self.listbox.yview_moveto(1)

#----------------------------------Envoi du message encodé au serveur---------------------------------

        def action(self,*args):
                txt=self.entree.get()
                self.sock.send(("<"+self.name+"> "+txt).encode())
                self.entree.delete(0,"end")

#----------------------Paramétrage de la fenêtre de confirmation de fermeture--------------------------
        
        def on_closing(self):
            if messagebox.askokcancel("Quitter", "Voulez vous réellement quitter?"):
                opened=False
                self.sock.send(("disconnected").encode())
                self.destroy()

#-----------------------------------Réception et affichage des messages---------------------------------
                
        def recevoir(self):
            while opened:
                txt=self.sock.recv(1024).decode("UTF-8")
                self.m.append(txt)
                self.affiche(txt)

#-----------------------Mise en place de la boucle qui contient le programme---------------------------
                
    miam=App()
    miam.protocol("WM_DELETE_WINDOW", miam.on_closing)
    miam.mainloop()
    
