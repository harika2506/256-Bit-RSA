import PrimeGenerator as pg
import sys
sys.path.append( "pathname_to_BitVector_directory" )
import BitVector
import fileinput
# Finding GCD using Euclid Algorithm
def gcd(a,b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a
# Generating p and q using PrimeGenerator.py
def generating_pandq():
    prime = pg.PrimeGenerator(bits = 128, debug = 0, emod = 65537)
    p=prime.findPrime()
    q=prime.findPrime()
    p1=p-1
    q1=q-1
    gcd1=gcd(p1,e)
    gcd2=gcd(q1,e)

    # Find p and q such that p!=q and gcd(p-1,e)=1 and gcd(q-1,e)=1
    while p==q and gcd1!=1 and gcd2!=1:
        p=prime.findPrime()
        q=prime.findPrime()
        p1=p-1
        q1=q-1

        gcd1=gcd(p1,e)
        gcd2=gcd(q1,e)

    return p,q
# Generating d using p,q and using BitVector multiplicative_inverse
def generate_d(p,q):
    phi = (p-1) * (q-1)

    bv_modulus = BitVector.BitVector(intVal=phi)
    bv = BitVector.BitVector(intVal=e)
    d = int(bv.multiplicative_inverse( bv_modulus ))
    return d

def encryption(input_file,output_file,p,q,message):
    n = p * q
    output=open(output_file,'w+')
    message_128bit = message_given
    # Padding 128 block data with zeroes
    bit_block128_count = len(message_128bit)/16
    if(len(message_128bit)%16 == 0):
        bit_block128_count+1
    i=0
    k=0
    new_list=[]

    while(i<bit_block128_count):
        j=0
        s=""
        # 128-bit data means 16 characters.So divding the data into 128 bit
        while(j<16):
            s+= message_128bit[k]
            k=k+1
            j=j+1
        new_list.append(s)
        i=i+1

    m=""
    while k<len(message_128bit):
        m+=message_128bit[k]
        k=k+1
    count=16-len(m)
    while(count!=0):
        m+="\n"
        count=count-1

    new_list.append(m)

    new_list_256=[]
    for i in new_list:
        # Adding zeroes to the data of 128 bit
        j=i.zfill(32)
        new_list_256.append(j)
    for i in new_list_256:
        if(len(i)==16):
            for char in i:

                m_e=ord(char)**e
                cipher=m_e%n
                output.write("%d\n"%cipher)
        else:
            for char in i:
                m_e=ord(char)**e
                cipher=m_e%n
                output.write("%d\n"%cipher)

    output.close()


def decryption(input_file,output_file,p,q,d):
    decrypted_list=[]
    decrypted_list_1=[]
    cipher_list=[]
    n=p * q
    input=open(input_file)
    output=open(output_file,'w+')
    # Read line by line from the output.txt file
    cipher_text = [int(line) for line in input]

    for i in cipher_text:
        c_dmodn=pow(i,d,n)
        cipher_list.append(c_dmodn)
    # Removing the zeroes padded to the message block
    for i in cipher_list:
        x=chr(i)
        decrypted_list.append(x)
    count=1
    decrypted_text_1=""
    # Removing zeroes from the data
    for i in decrypted_list:
        if(count%32<=16 and count%32!=0):
            count+=1
        else:
            count+=1
            decrypted_list_1.append(i)
    decrypted_text=''.join(i for i in decrypted_list_1)
    # Removing the newline characters added
    decrypted_text=decrypted_text.rstrip('\n')
    # Writing  the output to the output_file
    output.write(decrypted_text)
    # closing the otput file
    output.close()



if __name__ == '__main__':
    # Reading the message from message.txt file
    message=open("message.txt",'r')
    message_given=message.read()

    e = 65537
    p,q=generating_pandq()
    d=generate_d(p,q)

    # Creating the commands for both encrypt and decrypt
    length=len(sys.argv)
    if(length==4):
        if sys.argv[1]=="-e":
            input_file=sys.argv[2]
            output_file=sys.argv[3]
            # Storing the values of p and q in a file
            f1=open ('pqfile.txt', 'w')
            f1.write(str(p))
            f1.write("\n")
            f1.write(str(q))
            f1.close()
            encryption(input_file,output_file,p,q,message_given)
        elif sys.argv[1]=="-d":
            input_file=sys.argv[2]
            output_file=sys.argv[3]
            # Storing the values of p and q in a file
            f2 = open('pqfile.txt','r')
            arr = [int(line) for line in f2]
            p = arr[0]
            q = arr[1]
            d = generate_d(p,q)
            decryption(input_file,output_file,p,q,d)
        else:
            print "Give the correct commands"
    else:


        print("ENTER THE CORRECT COMMANDS")
        print "The commands should be"
        print "The correct commands are Encrypt : python hw03.py -e message.txt output.txt and Decrypt : python hw03.py -d output.txt decrypted.txt "
