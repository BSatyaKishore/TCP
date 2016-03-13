import socket,sys

last_packet_recieved = -1
done_till_packet = -1
window = []

UDP_IP = "localhost"#"10.208.20.9"#"10.208.20.211"#"localhost"
UDP_PORT = 3610
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def send_ack(packet,time_,addr):
	global window, done_till_packet
	window.append(packet)
	while (done_till_packet+1) in window:
		while (done_till_packet+1) in window:
			window.remove((done_till_packet+1))
		done_till_packet = done_till_packet + 1
	for i in window:
		if i < done_till_packet:
			window.remove(i)
	sock.sendto(time_+"$#$"+(str(done_till_packet)), addr)
	print "recieved", packet, "sent", done_till_packet


def send_ack_old(packet,time_,addr):
	global last_packet_recieved,done_till_packet,window
	if packet < done_till_packet:
		print "recieved", packet, "sent1", done_till_packet,
		sock.sendto(time_+"$#$"+str(done_till_packet)	, addr)
		print "SENT"
		return
	if packet >= last_packet_recieved:
		window = window + [False]*(packet - last_packet_recieved)
		last_packet_recieved = packet
	#print >>sys.stderr, window,last_packet_recieved,packet, done_till_packet
	if packet != done_till_packet:
		if window[packet -1  - done_till_packet] == True:
			print "recieved", packet, "sent2", done_till_packet,
			sock.sendto(time_+"$#$"+(str(done_till_packet)), addr)
			print "SENT"
			return
	window[packet -1  - done_till_packet] = True
	sat = len(window)
	for i in range(len(window)):
		if not window[i]:
			window = window[i:]
			done_till_packet = done_till_packet + i
			break
	if window == [True]*(sat):
		done_till_packet = done_till_packet + sat - 1
	done_till_packet = done_till_packet + 1
	# send an acknowledgement done till ack
	print "recieved", packet, "sent3", done_till_packet,
	sock.sendto(time_+"$#$"+(str(done_till_packet)), addr)
	print "SENT"
	return

 #input("Enter port:")

while True:
	data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
	#print "received message:", 
	a = data.split('$#$')
	print "received",a[0]
	send_ack(int(a[0]),a[1], addr)

