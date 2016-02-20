######################################################################################################################################################################################################################################
import time, socket, signal, sys, errno, sys, math
######################################################################################################################################################################################################################################
UDP_IP = "localhost"
UDP_PORT = 3615
######################################################################################################################################################################################################################################
last_ack = 0
repitation_count = 0
window = []
window_size = 1.0
last_packet_sent = 0.0
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
    if last_ack == number:
        repitation_count += 1
        if repitation_count == 1:
            on_dup_ack(number)
            return
        else:
            on_td_ack(number)
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
        ssthreshold = int(window_size+1/2)
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
            window_size = window_size + 1.0/window_size
            transmit_as_allowed()
        elif TCP_Mode == "FastRecovery":
            window_size = ssthreshold
            window.transmit_as_allowed()

    return

def transmit_as_allowed():
    for i in range(int(window_size-len(window))):
        send_packet(last_packet_sent + 1)

def send_packet(packet_number):
    global window, last_packet_sent
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