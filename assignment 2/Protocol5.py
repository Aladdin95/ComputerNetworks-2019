#!/usr/bin/env python
# coding: utf-8

# In[32]:


# at first i will define packet size as the size of packet is standard 512 or 1024 but most used is 1024 and maximum sequence
PACKETSIZE = 1024
MAX_SEQ = 7
EVENT_TYPE = {'frame_arrival' : False,'cksum_err' : False ,'timeout' : False, 'network_layer_ready' : False}
LIST_FRAMES = []
# here we will define frame 
class frame:
    def __init___ (self,kind,seq,ack,info):
        self.kind = kind
        self.seq = seq
        self.ack = ack
        self.info = info
        
def enable_network_layer ( ):
    global LIST_FRAMES
    EVENT_TYPE['network_layer_ready'] = True
    LIST_FRAMES = []
    # it can be for sender or receiver
    packet = open('networklayer_sender','r')
    frames = packet.read()
    for i in range (0,1024,8) :
        LIST_FRAMES.append(frames[i:i+8])
    packet.close()
  
def disable_network_layer ( ):
    EVENT_TYPE['network_layer_ready'] = False
    
def wait_for_event ( ):
    while True:
        if EVENT_TYPE['frame_arrival'] or EVENT_TYPE['cksum_err'] or EVENT_TYPE['timeout'] or EVENT_TYPE['network_layer_ready']:
            break
            
def inc (k) :
    if k < MAX_SEQ :
        k = k +1 
    else :
        k = 0
        
def from_network_layer (packet,frame_index) :
    if frame_index is len(packet) :
        packet.append(LIST_FRAMES.pop())
    else :
        packet[frame_index] = LIST_FRAMES.pop()
        
def to_network_layer (packet):
    writer = open('networklayer_receiver','w')
    writer.write(packet+'\n')
    writer.close()
    
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

def between (a,b,c):
    if (a <= b and b < c) or (b < c and c < a) or (c < a and a <= b) :
        return True
    else :
        return False
'''
#so test cases :
print(between(3,1,4))
print(between(6,8,4))
'''
def send_data (frame_nr, frame_expected, buffer):
    global MAX_SEQ
    s = frame()
    s.info = buffer[frame_nr]
    s.ack = (frame_expected + MAX_SEQ)%(MAX_SEQ + 1)
    # to be complete
    
def protocol5 ( ):
    r = frame()
    enable_network_layer()
    ack_expected = 0
    next_frame_to_send = 0
    frame_expected = 0
    nbuffered = 0
    buffer = []
    while True :
        wait_for_event()
        
        if EVENT_TYPE['network_layer_ready']:
            # file name changes according to process name is it sender or receiver
            from_network_layer(buffer,next_frame_to_send)
            nbuffered = nbuffered + 1
            send_data(next_frame_to_send, frame_expected, buffer)
            inc(next_frame_to_send)
        
        elif EVENT_TYPE['frame_arrival']:
            '''
            #to be complete
            from_physical_layer(r)
            '''
            if r.seq == frame_expected:
                to_network_layer(r.info)
                inc(frame_expected)
            while between(ack_expected, r.ack, next_frame_to_send) :
                nbuffered = nbuffered − 1
                '''
                #to be completed
                stop_timer(ack expected)
                '''
                inc(ack_expected)
            
        elif EVENT_TYPE['cksum_err']:
            
            
        elif EVENT_TYPE['timeout']:
            next_frame_to_send = ack_expected
            for i in range(1,nbuffered+1,1):
                send_data(next_frame_to_send, frame_expected, buffer)
                inc(next_frame_to_send)
                
            
    if nbuffered < MAX_SEQ:
        enable_network_layer()
    else:
        disable_network_layer()
        


# In[ ]:




