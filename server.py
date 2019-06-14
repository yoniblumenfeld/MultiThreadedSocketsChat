import socket
import threading

class TCPServer(object):
    """
    class used to create new Multi-Threaded TCPServer.
    """
    #TODO:add method for spreading messages being sent by clients to all other clients (chat-like)
    #TODO:add method for answering specific client
    def __init__(self,ip,port,listeners=3):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(0,socket.SO_REUSEADDR,1)
        self.server.bind((ip,int(port)))
        self.server.listen(listeners)
        self.clients_threads_dict = {}
        self.started_clients_threads_list = []

    def _accept_connections(self):
        """
        method responsible for accepting new connections.
        every new connection is added to the client threads dict.
        the addr tuple is being used as key and the client socket object as value
        """
        while True:
            client,addr = self.server.accept()
            self.clients_threads_dict[addr] = client
            print("Got new connection from {}".format(addr))

    def _check_for_new_input_from_client(self,addr,client):
        """
        method responsible for checking input for specific client
        repeatedly
        """
        while True:
            #TODO:Handle bigger data being sent (may only be relevant if sending something other than text messages)
            data = client.recv(4096)
            if data == b'': #b'' is data sent "recieved" when a socket is closed.
                #TODO:Close thread properly when closed socket is spotted (previous line).
                #TODO:make sure to remove from clients dict and clients threads list
                client.close()
                self.started_clients_threads_list.remove(addr)
                threading.current_thread().join()
                break
            print("{} sent: {}".format(addr,data))

    def check_for_new_input_from_clients(self):
        """
        method responsible for start checking the client threads dict
        for new clients. if a new client is spotted, a thread for input checking is initiated started for it.
        """
        while True:
            for addr,client in self.clients_threads_dict.items():
                if addr not in self.started_clients_threads_list:
                    self.started_clients_threads_list.append(addr)
                    threading.Thread(target=self._check_for_new_input_from_client,args=(addr,client)).start()


    def start_server(self):
        """
        method responsible for initiating all of the required threads
        for the server to function properly
        """
        accept_conns_thread = threading.Thread(target=self._accept_connections)
        accept_conns_thread.start()
        check_for_new_inputs_thread = threading.Thread(target=self.check_for_new_input_from_clients)
        check_for_new_inputs_thread.start()




if __name__ == "__main__":
    server = TCPServer("127.0.0.1",5656)
    server.start_server()
g