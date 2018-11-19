#!/usr/bin/env python
# coding: utf-8

# In[85]:


#crcCore Function
def crcCore(intMessage,intGenerator):
    '''
        Function takes :
        two Inputs -> intMessage (int) and intGenerator (int) 
        Return -> intRemainder (int)
    '''
    #Transform Inputs from int to binary
    binMessage = format(intMessage,'b')
    binGenerator = format(intGenerator,'b')
    #Get Length of Generator
    lenGenerator = len(binGenerator)
    dividend = int(binMessage[0:4],2)
    for i in range(len(binMessage)-(lenGenerator - 1)):
        #Check Most Significat Bit to choose Divisor
        if format(dividend,'b').zfill(lenGenerator)[0] == '1':
            divisor = int(binGenerator,2)
        else:
            divisor = 0
        #We have 2 cases First Case : Last iteration to get Remainder , Second Case : usual case drop most significat bit of xor and take another bit from binMessage
        if i == len(binMessage)-(lenGenerator):
            dividend = dividend ^ divisor
        else:
            dividend = int(format(dividend ^ divisor,'b')+ binMessage[i+4],2)
    return dividend
    
    
    
    


# In[86]:


#TestCase
print(crcCore(1256,9))

