import socket
import threading
import sys
import random
from time import sleep
if sys.version_info[0] >= 3:
    import queue
else:
    import Queue as queue

'''
Kommunication Ready Over NetworK
                                       /
                                       (,
                                        (
                                         .
                                         ,
                                         ,,,,...
                                     .,,,,,,,,,,,,,..
                                   .,,,,,,,,,,,,,,,,,,,.
                                  .,,,,,,,,,,,,,,,,,,,,,,,.
                                 ,,,,,,,,*/////////////////*.
                               .,,,,*%&&(////////////((///////,
                              .,*%&&&&&/////(((((///(&&///(/#&&&&.
                             *&&&&@&&&(///(&&&&&&&&&&&%///(@&&&&@%
                           ,%&&&&@&&&////#@%(////((#%#////#%(///(
                         ,%&&%/(/#&&(////&///////////////(/////*
                       #&&&&@(////%(//////////(//(#///////(*(//
                    #&&&@&&&///////////////    * //////. . /*
                   .&@&&&&&&&%(//////////////((//(///////*((/(/.
                   #&&&&&&&&&//((///////////////////////////////,
                 *&&&&&&&&&&////(///////(///////////////////////*
             /#&&&&&&&&&&&&////////////////(//////////////////*
           %&&&&&&@&&&&&&&////(//////////%//////////(////////
           &&&&&%&&&&&&&&////(///////////%#//////////////(/%&.
           &&&&&&&@&&&&&////(////////////((.,//////////((/#&&%.
          #&@&@&&&&&&&&////(//////////////(((/,       *//(&&&&.
        ,&&&&&&&&&&&&%//////(//////////////((((((%%&%////%&&&%
      ,&&&&&&@&&&&&&&////////(//////////////((((((%%%%((/&&&&(
     /&&&@&&&&&&&&&%//////////(////////////////////////(/&&&&%.
    .&@@&&&&&&&&&&%////////////(/////////////////////////&&%@&&
    .&@&@&&&&&&&//////////////(////////////////////////%&&%&&%.
     (&&@&&&&&&&%////////////////((//////////////////////#&&&&&&&.
     .%&&&&&&&&(//////////////(////#//////////////////////&&&&&&&(
       (&@&&&//////////////////(///(////////////////(///(&&&&&&,
         ,&&&////////////////////////(#////////////////////&@&&&*
           .////////////////////////////(///////////////////%&(
           ///////////////////////////////(//////////////////
         ,/////////////////////////////////((////////////((.
        ,//////////////////////////////////////////(////////.
       ///////////////////////////////////////////(//////////,
     ./////////////////////////////////////////////////////////.
   *(((///////////////////////////////////////////(//////////////*.
 *(((((((///////////////////////////////////////////////////////////,
((((((((((/////////////////////////////////////////////////////////////*.
(((((((((((///////////////////////////////////////////////////////////////*(/,.



==============================================================================
Usage:
    You need to derivate Kronk class and overwrite "attitude" methode
==============================================================================
'''

'''
Kronk class :D
'''
class Kronk():
    '''
    @param port Integer
    @param ip String
        Put 0.0.0.0 to listen connection from outside
    @param gentil Boolean If the Kronk will respond to other
    @param messageLenght Integer Size of messages
    @param verbose Boolean gag Kronk
    '''
    def __init__(self, port, ip='127.0.0.1', gentil=True, messageLenght=255, verbose=True):
        self.verbose = verbose
        self.messageLenght = messageLenght
        self.gentil = gentil
        self.ecureuil = {}
        self.clients = []
        self.port = port
        self.ip = ip
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((self.ip, self.port))
        except:
            exit(1)
        self.runningQueue = queue.Queue()
        if(self.verbose):
            print("[+] Kronk ecoute sur {}:{}"
                .format(self.ip, self.port))

        self.talk()

    '''
    Attitude to adopt when receiving a message
    @param message String Message rreceived by an other kronk
    '''
    def attitude(self, message):
        if(message == "Coucou"):
            return "Coucou Kronk"
        elif(message == "Y-a pas quelque chose qui brule ?"):
            return "Aahhh, mes gougeres aux epinards !"
        else:
            return "Comment ?"

    '''
    Start listening for other Kronk
    '''
    def run(self):
        t = FuncThread(self._run, self.runningQueue)
        t.start()

    def _run(self, runningQueue):
        def talker(socket):
            while runningQueue.empty():
                try:
                    request = client.recv(self.messageLenght)
                    if request != "":
                        request = request.decode()
                        if(request == "__Amis?__"):
                            if(self.gentil):
                                client.send(bytearray("__oui__".encode()))
                            else:
                                client.send(bytearray("__non__".encode()))
                        elif(request == "__bye__"):
                            client.send(bytearray("__bye__".encode()))
                            client.close()
                            return 0
                        else:
                            response = self.attitude(request)
                            client.send(bytearray(response.encode()))
                except:
                    return 1

        while self.runningQueue.empty():
            self.socket.listen(5)
            client, address = self.socket.accept()
            if(self.verbose):
                print("[+] Kronk a gagne un nouvel Ecureuil sur {}"
                    .format(address))
            c = FuncThread(talker, client)
            self.clients.append(c)
            c.start()
        pass

    '''
    Connect to an other Kronk
    @param port Integer
    @param ip String
    '''
    def findEcureuil(self, port, ip):
        c = Ecureuil(port, ip, verbose=self.verbose)
        self.ecureuil["{}:{}".format(port, ip)] = c
        return c

    '''
    Remove a Kronk from your friends
    @param ecureuil Ecureuil
    '''
    def removeEcureuil(self, ecureuil):
        if(self.verbose):
            print("[+] Kronk a perdu un Ecureuil :( sur {}:{}"
                .format(self.ip, self.port))
        for e in self.ecureuil:
            if(e == str(ecureuil.ip) + ":" + str(ecureuil.port)):
                del self.ecureuil[e]

    '''
    Encourage les gens a demarer uen revolution.
    Et rappelez vous que les evolution viennent toujours du bas,
    et pas du haut !
    '''
    def makeRevolution (self) :
        print ("C'est la luuuuuuuuuuuuuuuuuteeeeueuuuuuh finaaaaaaleeeuuh !!!")
        for i in range (4) :
            print ("Allende ! Allende ! El pueblo suportate !")
        print ("C'est la luuuuuuuuuuuuuuuuuteeeeueuuuuuh finaaaaaaleeeuuh !!!")

    def talk(self):
        if(self.verbose):
            citation = [
                "Aahhh, mes gougeres aux epinards !",
                "Quelle etait la probabilite que cette trappe debouche ici ?",
                "Trois porcinets a billet jambon a pouce au vent, \nun petit dejeuner grand-mere edente, \nun steak sans arretes, ca roule !",
                "Cadeau d'anniversaire de moi a moi ! \nOh ! Comment me remercier ?",
                "Tu m'as pourri mon groove !",
                "Kronk, abaisse le levier. \nPAAS CELUIII LAAAAA...!!",
                "Vous avez pourri le groove de l'empereur.",
                "Bouhouhou qu'il est vilain le lama, mechant lama !",
                "Je suis devenu un vieux lama qui pue !! \nAhhhh ! Face de lama !!",
                "Euh... comment te l'dire ? \nTon service vient d'etre reduit, \non doit faire des couts drastiques, \ntu as ete victime d'un changement d'cap, \ntu sors du cadre de nos activites... \nEuh choisis ce que tu veux j'en ai plein.",
                "J'ai vu ma cousine aujourd'hui. \nElle avait une de ces robes !",
                "90 macaques qui sautaient sur la couette, \nle premier qu'est tombe s'est ramasse sur la tete !"
            ]
            print('[BlaBla] {}'.format(citation[random.randrange(0, len(citation))]))
            threading.Timer(random.randrange(10, 60), self.talk).start()


    def __del__(self):
        print("Oh oui, le poison ! Le poison destine a Kuzco ! \nLe poison que tu as choisi specialement pour tuer Kuzco ! \nLe poison de Kuzco ! ... ce poison-la ?")
        self.socket.close()
        self.runningQueue.put("STOP")
        for c in self.clients:
            c.join()
        self.runningQueue.get()

'''
Ecureuil class
Representation of a Kronk friend
'''
class Ecureuil():
    '''
    @param port Integer
    @param ip String
    @param messageLenght Integer Size of messages
    @param verbose Boolean gag Ecureuil
    '''
    def __init__(self, port, ip, messageLenght=255, verbose=True):
        self.verbose = verbose
        self.messageLenght = messageLenght
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

        def handshake(response):
            if(response == "__oui__"):
                if(self.verbose):
                    print("[+] Ecureuil gentil :D sur {}:{}"
                        .format(self.ip, self.port))
            else:
                if(self.verbose):
                    print("[+] Ecureuil mechant :'( sur {}:{}"
                        .format(self.ip, self.port))
                self.socket.close()

        self.send("__Amis?__", handshake)

    '''
    Send a message to an ecureuil
    @param message String Message for the ecureuil
    @param callback Function function to call when receiving the answer
        If ecureuil is mean response is None
        Exemple:
            def callback(reponse):
                print(response)
    '''
    def send(self, message, callback):
        try:
            self.socket.send(bytearray(message.encode()))
            response = self.socket.recv(self.messageLenght)
            callback(response.decode())
        except Exception as e:
            if(self.verbose):
                print(e)
                print("[+] Ecureuil n'ecoute pas :( sur {}:{}"
                    .format(self.ip, self.port))
            callback(None)

    '''
    Deconnect from the ecureuil
    @param callback Function function to call when receiving the answer
        If ecureuil is mean response is None
        Exemple:
            def callback(reponse):
                print(response)
    '''
    def bye(self, callback):
        print("[+] Au revoir petit Ecureuil sur {}:{}"
            .format(self.ip, self.port))
        self.send("__bye__", callback)

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        threading.Thread.__init__(self)
        self._target = target
        self._args = args

    def run(self):
        self._target(*self._args)

if __name__ == "__main__":
    k = Kronk(7777, "127.0.0.1")
    k2 = Kronk(7778, "127.0.0.1")

    k.run()
    k2.run()
    c = k.findEcureuil(7778, '127.0.0.1')

    sleep(1)
    def callback(rep):
        print("<== {}".format(rep))

    print("==> {}".format("coucou"))
    c.send("Coucou", callback)
    print("==> {}".format("Y-a pas quelque chose qui brule ?"))
    c.send("Y-a pas quelque chose qui brule ?", callback)

    def end(rep):
        pass

    c.bye(end)

    sleep(100)
    del k
    del k2
