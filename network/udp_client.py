import argparse
import socket
import re
import select
import sys
import threading

# Connects to the server and returns a socket object.
# You should not have to modify this function.
def connect(host, port):
  # HOST, PORT = "eig.isi.edu", 63682
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
    sock.connect((host,port))
    sock.settimeout(300)
    return sock
  except Exception as e:
    print("Cannot connect to:" + host + ":" + port)
    print(e)
    return None
# Takes in a socket and a string (message) and attempts to send to the server.
def send(sock, message):
  try:
    sock.sendall(message.encode('utf-8'))
  except Exception as e: 
    print(e)

# Takes a socket object, attempts to read a message from the server.
def recv(sock):
  try:
    data = sock.recv(1024)
    return data.decode('utf-8')
  except socket.timeout:
    return "TIMEOUT"
  except Exception as e:
    print(e)
    return "ERROR"

def register(sock):
  send(sock, "SRC:000;DST:999;PNUM:1;HCT:1;MNUM:100;VL:;MESG:Register")
  data = recv(sock)
  if(data.find('Error') != -1):
    return False
  return data

def pullRegistry(sock, idNumber):
  send(sock, "SRC:" + idNumber + ";DST:999;PNUM:5;HCT:1;MNUM:101;VL:;MESG:get map")
  data = recv(sock)
  if(data.find("Error") != -1):
    return False
  return data

def listenpeers(host,port):
  peerconnect = connect(host,port);
  return recv(peerconnect)

def sendToPeer(msg, peer):
  try:
    # send(sock, msg)
    UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPSock.sendto(msg, (peer.get("ip"), int(peer.get("port"))))
    print "Send Message To" + peer.get("ip") + peer.get("port")
    # UDPSock.settimeout(10)
    (message, sender) = UDPSock.recvfrom(1024)
    return message
  except socket.timeout:
    return False

def receiveData():
  server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server.bind(("0.0.0.0", int(myPort[0])))
  while True:
    data, client_addr = server.recvfrom(1024)
    print data
    dst = re.findall(r'DST:([^;]+)', data)[0]
    src = re.findall(r'SRC:([^;]+)', data)[0]
    msg = "SRC:" + dst + ";DST:" + src + ";PNUM:4;HCT:1;MNUM:###;VL:;MESG:ACK"
    server.sendto(msg, client_addr)
    # print "Connected by", client_addr, " Receive Data : ", data

  server.shutdown(socket.SHUT_RDWR)
  server.close()

if __name__ == "__main__":
  # Connect
  serverhost = "eig.isi.edu"
  serverport = 63682
  sock = connect(serverhost, serverport);
  if sock == None:
    exit();

  # Register
  registerData = register(sock)
  if(registerData):
    # print registerData
    ID = re.findall(r'DST:([^;]+)', registerData)
    idNumber = ID[0]
    myIp = re.findall(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})@', registerData)
    myPort = re.findall(r'@(\d{1,5})', registerData)
    print myIp[0], myPort[0]
    print "Successfully registered. My ID is: " + ID[0] + "\n"
  else:
    print "Error"
    exit()

  # Pull Registry
  pullRegistryData = pullRegistry(sock, idNumber)
  if(pullRegistryData):
    res = re.findall(r'ids=([^and]+)', pullRegistryData)
    print "******************** \n"
    print "Recently Seen Peers: " + res[0] + "\n"
    ids = re.findall(r'(\d{1,3})=', pullRegistryData)
    ips = re.findall(r'=(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})@', pullRegistryData)
    ports = re.findall(r'@(\d{1,5})', pullRegistryData)
    print "Known addresses: \n"
    peers = {}

    for i in range(0, len(ids)):
      peers.update({ids[i] : {"ip" : eval(repr(ips[i])[1:]), 'port' : ports[i]}})
      print ids[i] + "\t" + eval(repr(ips[i])[1:]) + "\t" + ports[i]
    print "******************** \n"
  else:
    print "Error"
    exit()

  # Send Data
  sock.close()

  thread = threading.Thread(target=receiveData)
  thread.daemon = True
  thread.start()
  
  while True:
    command = raw_input("Please enter your command: ")
    # print command
    # stdio.write(command)
    args = command.split()
    if(len(args) < 3):
      print "Error: Too few args"
      print "Please enter your command: "
      continue

    if(args[0] in ['msg', 'ids']):
      peer = peers.get(args[1], False)
      if(not peer):
        print "Error: Peer not found"
        continue
    message = "SRC:" + ID[0] + ";DST:" + args[1] + ";PNUM:3;HCT:1;MNUM:102;VL:;MESG:" + args[2]
    for times in range(0, 5):
      response = sendToPeer(message, peer)
      if(response):
        print response
        break
    
      print "********************"
      print "ERROR: Gave up sending to " + args[1]
      print "********************"import argparse
import socket
import re
import select
import sys
import threading

# Connects to the server and returns a socket object.
# You should not have to modify this function.
def connect(host, port):
  # HOST, PORT = "eig.isi.edu", 63682
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
    sock.connect((host,port))
    sock.settimeout(300)
    return sock
  except Exception as e:
    print("Cannot connect to:" + host + ":" + port)
    print(e)
    return None
# Takes in a socket and a string (message) and attempts to send to the server.
def send(sock, message):
  try:
    sock.sendall(message.encode('utf-8'))
  except Exception as e: 
    print(e)

# Takes a socket object, attempts to read a message from the server.
def recv(sock):
  try:
    data = sock.recv(1024)
    return data.decode('utf-8')
  except socket.timeout:
    return "TIMEOUT"
  except Exception as e:
    print(e)
    return "ERROR"

def register(sock):
  send(sock, "SRC:000;DST:999;PNUM:1;HCT:1;MNUM:100;VL:;MESG:Register")
  data = recv(sock)
  if(data.find('Error') != -1):
    return False
  return data

def pullRegistry(sock, idNumber):
  send(sock, "SRC:" + idNumber + ";DST:999;PNUM:5;HCT:1;MNUM:101;VL:;MESG:get map")
  data = recv(sock)
  if(data.find("Error") != -1):
    return False
  return data

def listenpeers(host,port):
  peerconnect = connect(host,port);
  return recv(peerconnect)

def sendToPeer(msg, peer):
  try:
    # send(sock, msg)
    UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPSock.sendto(msg, (peer.get("ip"), int(peer.get("port"))))
    print "Send Message To" + peer.get("ip") + peer.get("port")
    # UDPSock.settimeout(10)
    (message, sender) = UDPSock.recvfrom(1024)
    return message
  except socket.timeout:
    return False

def receiveData():
  server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server.bind(("0.0.0.0", int(myPort[0])))
  while True:
    data, client_addr = server.recvfrom(1024)
    print data
    dst = re.findall(r'DST:([^;]+)', data)[0]
    src = re.findall(r'SRC:([^;]+)', data)[0]
    msg = "SRC:" + dst + ";DST:" + src + ";PNUM:4;HCT:1;MNUM:###;VL:;MESG:ACK"
    server.sendto(msg, client_addr)
    # print "Connected by", client_addr, " Receive Data : ", data

  server.shutdown(socket.SHUT_RDWR)
  server.close()

if __name__ == "__main__":
  # Connect
  serverhost = "eig.isi.edu"
  serverport = 63682
  sock = connect(serverhost, serverport);
  if sock == None:
    exit();

  # Register
  registerData = register(sock)
  if(registerData):
    # print registerData
    ID = re.findall(r'DST:([^;]+)', registerData)
    idNumber = ID[0]
    myIp = re.findall(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})@', registerData)
    myPort = re.findall(r'@(\d{1,5})', registerData)
    print myIp[0], myPort[0]
    print "Successfully registered. My ID is: " + ID[0] + "\n"
  else:
    print "Error"
    exit()

  # Pull Registry
  pullRegistryData = pullRegistry(sock, idNumber)
  if(pullRegistryData):
    res = re.findall(r'ids=([^and]+)', pullRegistryData)
    print "******************** \n"
    print "Recently Seen Peers: " + res[0] + "\n"
    ids = re.findall(r'(\d{1,3})=', pullRegistryData)
    ips = re.findall(r'=(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})@', pullRegistryData)
    ports = re.findall(r'@(\d{1,5})', pullRegistryData)
    print "Known addresses: \n"
    peers = {}

    for i in range(0, len(ids)):
      peers.update({ids[i] : {"ip" : eval(repr(ips[i])[1:]), 'port' : ports[i]}})
      print ids[i] + "\t" + eval(repr(ips[i])[1:]) + "\t" + ports[i]
    print "******************** \n"
  else:
    print "Error"
    exit()

  # Send Data
  sock.close()

  thread = threading.Thread(target=receiveData)
  thread.daemon = True
  thread.start()
  
  while True:
    command = raw_input("Please enter your command: ")
    # print command
    # stdio.write(command)
    args = command.split()
    if(len(args) < 3):
      print "Error: Too few args"
      print "Please enter your command: "
      continue

    if(args[0] in ['msg', 'ids']):
      peer = peers.get(args[1], False)
      if(not peer):
        print "Error: Peer not found"
        continue
    message = "SRC:" + ID[0] + ";DST:" + args[1] + ";PNUM:3;HCT:1;MNUM:102;VL:;MESG:" + args[2]
    for times in range(0, 5):
      response = sendToPeer(message, peer)
      if(response):
        print response
        break
    
      print "********************"
      print "ERROR: Gave up sending to " + args[1]
      print "********************"