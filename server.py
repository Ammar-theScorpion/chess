import pickle
import threading
 
from networkstatic import*

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((m_server, port))

 
client_lock = threading.Lock()
clients = set()
clients_addr2 = set()
game = {} 
m_players = []  

header = 64

def handel_connection(conn, client_status):
    print(client_status)
    if client_status == 0:
        print(len(clients_addr2))
        #conn.send(str.encode( str(len(clients_addr2))))
        conn.send(str.encode(str('b')))
   
    else:
        #conn.send(str.encode( str(len(clients_addr2))))
        conn.send(str.encode(str('w')))

     

    while True:
        try:
            piece = conn.recv(1024)
            try:
                bol = False
                piece = piece.decode()

                if piece == 'create game':
                    client_lock.acquire()
                    key = conn.getpeername()
                    game[key[1]] = [conn] 
                    clients_addr2.add(key[1])
                    client_lock.release()
                      

                elif piece == 'start game':
                    print(piece)
                     
                    piece = int(conn.recv(1024).decode() )
                    client_lock.acquire()
                    game[piece ].append(conn)
                    client_lock.release()
                        

                else:    
                    with client_lock:

                        for i in clients:
                            if piece == str(i.getpeername()):
    
                                conn.send(pickle.dumps(clients_addr2))
                                bol = True

                if not bol and type(piece) == str:  
                    
                    print("in text")
                    with client_lock:
                        for s in game:
                            print(game[s][0])
                            print(game[s][1])
                            print(conn)
                            if game[s][0]== conn:
                                game[s][1].send(str(piece).encode())
                                print('sent', piece)
                            elif game[s][1] == conn:
                                    game[s][0].send(str(piece).encode())
                                    print('sent', piece)




            except socket.error as e:
                print (e)
                pass
                #print(piece)
               # print("r")
               # with client_lock:
                #    for c in clients:
                 #       if c is not conn:
                  #          print("3434")

                   #         c.send( (piece))

           

            if not piece:
                break
         
        except socket.error as e:
            print("lost connection", e, client_status)
            break
server.listen()
def start():
    client_counter = 0
    client_status  = 0
    while True:
        conn, addr = server.accept()
        client_status = client_counter%2
        client_counter+=1
        with client_lock:
            clients.add(conn)
          
        
        thread = threading.Thread(target=handel_connection, args=(conn, client_status))
        thread.start()

print("server [Running]")
start()
