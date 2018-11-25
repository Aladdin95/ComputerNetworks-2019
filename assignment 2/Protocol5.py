from Physical import *
from threading import Thread
# at first i will define packet size as the size of packet is standard 512 or 1024 but most used is 1024 and maximum sequence

#PACKETSIZE = 512
MAX_SEQ = 7
EVENT_TYPE = {'frame_arrival': False, 'cksum_err': False, 'timeout': False, 'network_layer_ready': False}
LIST_FRAMES_SENDER = []
LIST_FRAMES_RECEIVER = []
arrived = None
FRAMES_START_TIMEOUT = []
FRAMES_STOP_TIMEOUT = []


# here we will define frame
class frame:
    kind = None
    seq = 0
    ack = 0
    info = None

    def __init___(self, kind, seq, ack, info):
        self.kind = kind
        self.seq = seq
        self.ack = ack
        self.info = info

    def __str__(self):
        return str(self.seq) + ' ' + str(self.ack) + ' ' + str(self.info)


def enable_network_layer(type_process):
    global LIST_FRAMES_SENDER
    global LIST_FRAMES_RECEIVER
    EVENT_TYPE['network_layer_ready'] = True

    if type_process == 'server':
        fname = 'networklayer_sender.txt'
        list = LIST_FRAMES_SENDER
    elif type_process == 'client':
        fname = 'networklayer_receiver.txt'
        list = LIST_FRAMES_RECEIVER

    packet = open(fname, 'r')
    frames = packet.read()
    if frames != '' and len(list) == 0:
        for i in range(0, 14, 2):
            list.append(frames[i:i+2])
        packet.close()


def disable_network_layer():
    EVENT_TYPE['network_layer_ready'] = False


def wait_for_event():
    print('waiting')
    while True:
        if any(EVENT_TYPE.values()):
            break
    print('done waiting')
    print(EVENT_TYPE)
            #['frame_arrival'] or EVENT_TYPE['cksum_err'] or EVENT_TYPE['timeout'] or EVENT_TYPE['network_layer_ready']:


def inc(k):
    if k < MAX_SEQ:
        k = k + 1
    else:
        k = 0
    return k


def from_network_layer(packet, frame_index, type_process):
    if type_process == 'server':
        if len(LIST_FRAMES_SENDER) > 0 and frame_index <= MAX_SEQ:
            packet.append(LIST_FRAMES_SENDER.pop(0))
        else:
            disable_network_layer()
    elif type_process == 'client':
        if len(LIST_FRAMES_RECEIVER) > 0 and frame_index <= MAX_SEQ:
            packet.append(LIST_FRAMES_RECEIVER.pop(0))
        else:
            disable_network_layer()


def to_network_layer(packet, type_process):
    if type_process == 'client':
        writer = open('networklayer_receiver.txt', 'a')
        writer.write(packet)
        writer.close()


def start_timer(k):
    if k is len(FRAMES_START_TIMEOUT):
        FRAMES_START_TIMEOUT.append(time.time())
    else:
        FRAMES_START_TIMEOUT[k] = time.time()
    
    #EVENT_TYPE['timeout'] = True


def stop_timer(k):
    if k is len(FRAMES_STOP_TIMEOUT):
        FRAMES_STOP_TIMEOUT.append(time.time()-FRAMES_START_TIMEOUT[k])
    else :
        FRAMES_STOP_TIMEOUT[k] = time.time()-FRAMES_START_TIMEOUT[k]
    
    EVENT_TYPE['timeout'] = False

    
'''
#so test cases :
s = frame
s.kind = 0
s.seq = 5
s.ack = 2
s.info = 'adadkadkaazfksfsnfgsgsjbnjshgdfkjghkdfkhgzdfkgj.zdkgzdgnzdfgzdngbmgzdbnzdm,bzf,mzsfgjskgsfg'
#print(s.info)
#print(s.ack)
'''     


def between(a, b, c):
    if (a <= b and b < c) or (b < c and c < a) or (c < a and a <= b) :
        return True
    else:
        return False


'''
#so test cases :
print(between(3,1,4))
print(between(6,8,4))
'''


def send_data(frame_nr, frame_expected, buffer, type_process, process):
    global MAX_SEQ
    if len(buffer) > 0:
        s = frame()
        s.info = buffer[frame_nr]
        s.seq = frame_nr
        s.ack = (frame_expected + MAX_SEQ) % (MAX_SEQ + 1)
        if type_process == 'server':
            print(s.info)
            process.send(s)
            time.sleep(2)
        start_timer(frame_nr)


def receive(process):
    global EVENT_TYPE
    while True:
        global arrived
        while EVENT_TYPE['frame_arrival'] is True:
            pass
        arrived = process.get().decode()
        EVENT_TYPE['frame_arrival'] = True


def protocol5(type_process, process):
    r = frame()
    enable_network_layer(type_process)
    ack_expected = 0
    next_frame_to_send = 0
    frame_expected = 0
    nbuffered = 0
    buffer = []
    thread = Thread(target=receive, args=(process,))
    thread.start()
    while True:
        wait_for_event()
        
        if EVENT_TYPE['network_layer_ready']:
            # file name changes according to process name is it sender or receiver
            if nbuffered < MAX_SEQ:
                from_network_layer(buffer, next_frame_to_send, type_process)
                nbuffered = nbuffered + 1
                send_data(next_frame_to_send, frame_expected, buffer, type_process, process)
                next_frame_to_send = inc(next_frame_to_send)
            disable_network_layer()

        elif EVENT_TYPE['frame_arrival']:
            temp = arrived
            temp = temp.split()
            r.seq = int(temp[0])
            r.ack = int(temp[1])
            r.info = temp[2]
            print(r.info)
            if r.seq == frame_expected:
                to_network_layer(r.info, type_process)
                frame_expected = inc(frame_expected)
            while between(ack_expected, r.ack, next_frame_to_send):
                nbuffered -= 1
                stop_timer(ack_expected)
                ack_expected = inc(ack_expected)
            EVENT_TYPE['frame_arrival'] = False

        elif EVENT_TYPE['cksum_err']:
            pass

        elif EVENT_TYPE['timeout']:
            next_frame_to_send = ack_expected
            for i in range(1,nbuffered+1,1):
                send_data(next_frame_to_send, frame_expected, buffer,type_process,process)
                next_frame_to_send = inc(next_frame_to_send)
            EVENT_TYPE['timeout'] = False
            
        if nbuffered < MAX_SEQ:
            enable_network_layer(type_process)
        else:
            disable_network_layer()
        

