import time, socket, signal, sys, errno, sys, math

window = []
repetation_count = 0
window_size = 1.0
last_packet_sent = 0
largest_ack_recieved = 0
time_out = 10
UDP_IP = "10.208.20.195"
UDP_PORT = 3610 #input("UDP target Port:")
td_for = 0
missing_segment = 0
mode = "CUBIC"
sshthreshold = 1000
Wmax = 100
TCP_Name = "BIC"
C = 2
last_td_time = time.time()
#MESSAGE = raw_input("Enter Message:")
increase = 1
decrease = 2

retranmission = False

# BIC_Parameters
Smax = 32
Smin = 0.01
beta = 0.125


def increase_decrease_values():
   global increase,decrease,mode, TCP,window_size,retranmission
   print TCP_Name, mode,
   if TCP_Name == "Reno":
   		if mode == "SlowStart":
			increase = int(window_size)
			if window_size > sshthreshold:
				mode = "CongestionAvoidance"
   		elif mode == "CongestionAvoidance":
		#TODO: Update the logic to make it for HSTCP
			if TCP_Name == "Reno":
				increase = 1
				decrease = 2
   elif TCP_Name == "WestWood":
   		increase = 0
   		if not retranmission:
			window_size = C*math.pow( (time.time()-last_td_time)-math.pow(Wmax*(C*1.0/decrease), 1/3.0), 3) +Wmax
		#window_size = window_size+1
		decrease = 2
   elif TCP_Name == "BIC":
   		if window_size < Wmax:
   			increase = (Wmax - window_size)/2.0
   		else:
   			increase = (window_size-Wmax)
   		if increase > Smax:
   			increase = Smax
   		elif increase < Smin:
   			increase = Smin
   		print "+",increase,"Wmax",Wmax
   elif TCP_Name == "WestWood":
   		pass



def on_time_out(signum, frame):
	global mode
	mode = "SlowStart"
	window_size = 1
	last_td_time = time.time()
	send_packet(last_packet_sent)
	return

lost_packets = []
def on_triple_ack(num):
	global window,window_size,last_packet_sent, td_for, repetation_count, missing_segment, sshthreshold,Wmax, decrease, lost_packets
	#print "TD num=",num,"td_for=",td_for
	#lost_packets.append(num)
	if num > missing_segment:
		if TCP_Name == "BIC":
			td_for = num
			missing_segment = num + window_size
			last_td_time = time.time()
			if window_size < Wmax:
				Wmax = window_size*(1-(1/2.0*decrease))
			else:
				Wmax = window_size # max*(decrease)
			window_size = window_size*(1-1.0/decrease)
		elif TCP_Name == "Reno":		
			td_for = num
			missing_segment = num + window_size
			window_size = float(int(window_size/decrease))
			sshthreshold = window_size
	
signal.signal(signal.SIGALRM, on_time_out)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

my_ack_count = 0
def on_ack(number,time_):
	global window, repetation_count, window_size, increase, retranmission, largest_ack_recieved, my_ack_count,lost_packets
	largest_ack_recieved = max(largest_ack_recieved,number)
	my_ack_count = my_ack_count - 1
	increase_decrease_values()
	rtt = int(1000000*(time.time())-time_)
	throughput = 10000*window_size/rtt
	print >> sys.stderr, rtt, throughput, number
	print "RTT =", str(rtt),"rc",repetation_count,"w",len(window), "Throughput=",throughput,"Ack = ",number, "MS",missing_segment, "td", td_for,"window_size =", window_size,"Sent_packets =",
	signal.alarm(time_out)
	if number > missing_segment:
		retranmission = True
	if number in window:
		window.remove(number)
		#send_packet(last_packet_sent + 1)
		repetation_count = 0
	else:
		repetation_count += 1
		if repetation_count == 2:
			on_triple_ack(number)
			print "#$#",
			send_packet(number+1)
			repetation_count = 0
		#else:
			#send_packet(last_packet_sent + 1)
	change = increase/window_size
	window_size = window_size + change
	for i in range(0,int(window_size)-my_ack_count):
		send_packet(last_packet_sent +1)
	print ""
#####################################################################################################################################################################################################################################
last_ack = -1
repitation_count = 0
window = []
window_size = 1.0
last_packet_sent = 0
######################################################################################################################################################################################################################################
signal.signal(signal.SIGALRM, on_time_out)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
######################################################################################################################################################################################################################################
TCP_Name = "Reno"
TCP_Mode = "SlowStart"
######################################################################################################################################################################################################################################
ssthreshold = 100.0
######################################################################################################################################################################################################################################

def ack_reader(number,timestamp):
    global last_ack, repitation_count, window
    print TCP_Name, TCP_Mode,"ACK", number, "window", window_size, "Sending",
    if last_ack == number:
        repitation_count += 1
        if repitation_count == 1:
            on_dup_ack(number)
            return
        else:
            on_triple_ack(number)
            return
    else:
        repitation_count = 0
        last_ack = number
        for i in window:
            if i <= number:
                window.remove(i)
        on_new_ack(number)

def on_dup_ack(number):
    global window_size
    if TCP_Name == "Reno":
        if TCP_Mode == "FastRecovery":
            window_size = window_size + 1
    return

def on_triple_ack(number):
    global ssthreshold, window_size, TCP_Mode
    if TCP_Name == "Reno":
        ssthreshold = int((window_size+1)/2)
        window_size = 1.0
        repitation_count = 0
        send_packet(number+1)
        if TCP_Mode != "SlowStart":
            TCP_Mode = "FastRecovery"

def on_time_out():
    return

def on_new_ack(number):
    global TCP_Name, TCP_Mode,window_size, ssthreshold
    if TCP_Name == "Reno":
        if TCP_Mode == "SlowStart":
            window_size = window_size + 1
            transmit_as_allowed()
            if window_size >= ssthreshold:
                TCP_Mode = "CongestionAvoidance"
        elif TCP_Mode == "CongestionAvoidance":
            window_size = window_size + 100.0/window_size
            transmit_as_allowed()
        elif TCP_Mode == "FastRecovery":
            window_size = ssthreshold
            transmit_as_allowed()

    return

def transmit_as_allowed():
    global window
    print window_size - len(window),
    for i in range(int(window_size-len(window))):
        send_packet(last_packet_sent + 1)

def send_packet(packet_number):
    global window, last_packet_sent
    window.append(packet_number)
    #print packet_number,
    if packet_number > last_packet_sent :
        last_packet_sent = packet_number
    sock.sendto(str(packet_number)+'$#$'+str(int(time.time()*1000000))+"$#$"+'a'*9990, (UDP_IP, UDP_PORT))

send_packet(0)
while True:
    try:
        recv_data, addr = sock.recvfrom(2048)
    except socket.error as (code, msg):
         if code != errno.EINTR:
             print "Test"
    a = recv_data.split('$#$')
    ack_reader(int(a[1]),float(a[0]))
    print "Sent"




'''
#TODO: Add a timer to it using signals
def send_packet(packet_number):
	global window, last_packet_sent, my_ack_count
	print packet_number,
	my_ack_count = my_ack_count + 1
	if packet_number not in window:
		window.append(packet_number)
	if packet_number > last_packet_sent :
		last_packet_sent = packet_number
	sock.sendto(str(packet_number)+'$#$'+str(int(time.time()*1000000))+"$#$"+'a'*9990, (UDP_IP, UDP_PORT))

	
send_packet(0)
while True:
	try:
		recv_data, addr = sock.recvfrom(2048)
	except socket.error as (code, msg):
	     if code != errno.EINTR:
	         print "Test"
	a = recv_data.split('$#$')
	on_ack(int(a[1]),float(a[0]))

'''
