

import json
import threading
import socketserver

CONNECTION_PORT = 9311

connections = {}
socket_counter = 0

class TCPHandler(socketserver.BaseRequestHandler):
	
	def handle(self):
		try:
			cur_thread = threading.current_thread()
			print("'{ip}' requested connection.".format(ip = self.client_address[0]))
			print("Connection request granted.")
			if threading.activeCount() > 2:
				print("Number of current client connections: {n}".format(n = threading.activeCount() - 2))
			global socket_counter
			connections[self.client_address[0] + "({counter})".format(counter = socket_counter)] = self.request
			socket_counter += 1
			while 1:
				received_from_client = json.loads(self.request.recv(10000).decode("utf-8"))
				for connection in connections:
					try:
						msg = "{user}: {data}".format(user = received_from_client["user"], data = received_from_client["data"][:-1])
						connections[connection].sendall(bytes(msg, "utf-8"))
					except Exception as e:
						print(str(e))
		except ConnectionResetError:
			pass

class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass

if __name__ == '__main__':
	HOST = ""
	print("Social Pie Server initiated.")
	print("Waiting for incoming connection requests...")
	server = TCPServer((HOST, CONNECTION_PORT), TCPHandler)
	server_thread = threading.Thread(target = server.serve_forever)
	server_thread.start()
	

