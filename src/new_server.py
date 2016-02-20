import socket,sys

last_packet_recieved = -1
done_till_packet = 0
window = []

UDP_IP = "10.208.20.207"#"localhost"
UDP_PORT = 3610
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def send_ack(packet,time_,addr):
	global last_packet_recieved,done_till_packet,window
	if packet < done_till_packet:
		sock.sendto(time_+"$#$"+str(done_till_packet)	, addr)
		return
	if packet >= last_packet_recieved:
		window = window + [False]*(packet - last_packet_recieved)
		last_packet_recieved = packet
	#print >>sys.stderr, window,last_packet_recieved,packet, done_till_packet
	if packet != done_till_packet:
		if window[packet -1  - done_till_packet] == True:
			print "num=",packet -1  - done_till_packet,
			return
	window[packet -1  - done_till_packet] = True
	sat = len(window)
	for i in range(len(window)):
		if not window[i]:
			window = window[i:]
			done_till_packet = done_till_packet + i
			print "updated0",done_till_packet
			break
	if window == [True]*(sat):
		done_till_packet = done_till_packet + sat - 1
		print "updated1",done_till_packet
	# send an acknowledgement done till ack
	sock.sendto(time_+"$#$"+(str(done_till_packet)), addr)
	return

 #input("Enter port:")

while True:
	data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
	#print "received message:", 
	a = data.split('$#$')
	print a[0],
	send_ack(int(a[0]),a[1], addr)

