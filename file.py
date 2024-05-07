from PIL import Image
import binascii
import optparse

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def hex2rgb(hexcode):
    return tuple(map(ord,hexcode[1:].decode('hex')))

def str2bin(message):
    binary = bin(int(binascii.hexlify(message),16))
    return binary[2:]

def bin2str(binary):
    message = binascii.unhexlify('%x'%(int('0b'+binary,2)))
    return message

def encode(hexcode,digit):
    if hexcode[-1] in {'0','1','2','3','4','5'}:
        hexcode = hexcode[:-1]+digit
        return hexcode
    else:
        return None
    
def decode(hexcode):
    if hexcode[-1] in {'0','1'}:
        return hexcode[-1]
    else:
        return None

def chaotic_sequence(x0, y0, a, b, length):
    """
    Generates a chaotic sequence using the given chaotic function.

    Args:
    - x0 (float): Initial value for x.
    - y0 (float): Initial value for y.
    - a (float): Chaotic function parameter.
    - b (float): Chaotic function parameter.
    - length (int): Length of the sequence to generate.

    Returns:
    - list: List containing the generated chaotic sequence.
    """
    x_values = [x0]
    y_values = [y0]

    for _ in range(length):
        x_next = 1 - a * x_values[-1]**2 + y_values[-1]
        y_next = b * y_values[-1]
        x_values.append(x_next)
        y_values.append(y_next)

    return x_values[1:], y_values[1:]  # exclude initial values

def xor_with_chaotic(message, x_sequence, y_sequence):
    """
    XORs each bit of the binary message with the corresponding chaotic sequence values.

    Args:
    - message (str): Binary message to be XORed.
    - x_sequence (list): Chaotic sequence for x.
    - y_sequence (list): Chaotic sequence for y.

    Returns:
    - str: Binary message XORed with the chaotic sequence.
    """
    chaotic_sequence_length = min(len(x_sequence), len(y_sequence))
    chaotic_sequence = [(x, y) for x, y in zip(x_sequence[:chaotic_sequence_length], y_sequence[:chaotic_sequence_length])]
    
    binary_message = [int(bit) for bit in message]
    binary_result = []

    for bit, (x, y) in zip(binary_message, chaotic_sequence):
        chaotic_bit = int((x + y) * 1000) % 2  # convert chaotic value to 0 or 1
        xor_result = bit ^ chaotic_bit
        binary_result.append(str(xor_result))

    return ''.join(binary_result)

def retrieve_from_xor(x_sequence, y_sequence, xor_result):
    """
    Retrieves the original binary message from the XOR result with the chaotic sequence.

    Args:
    - x_sequence (list): Chaotic sequence for x.
    - y_sequence (list): Chaotic sequence for y.
    - xor_result (str): XOR result of the binary message with the chaotic sequence.

    Returns:
    - str: Original binary message.
    """
    chaotic_sequence_length = min(len(x_sequence), len(y_sequence))
    chaotic_sequence = [(x, y) for x, y in zip(x_sequence[:chaotic_sequence_length], y_sequence[:chaotic_sequence_length])]

    binary_result = [int(bit) for bit in xor_result]
    binary_message = []

    for bit, (x, y) in zip(binary_result, chaotic_sequence):
        chaotic_bit = int((x + y) * 1000) % 2  # convert chaotic value to 0 or 1
        original_bit = bit ^ chaotic_bit
        binary_message.append(str(original_bit))

    return ''.join(binary_message)

def hide(filename,message):
    img = Image.open(filename)
    binary = str2bin(message).encode() + b'1111111111111110'
    if img.mode in ('RGBA'):
        img.convert('RGBA')
        datas = img.getdata()  #return all the pixels inside the image
        newData = []
        digit = 0
        temp = ''

        #for each pixel in image
        for item in datas:
            if(digit<len(binary)):
                newpix = encode(rgb2hex(item[0],item[1],item[2]),binary[digit])
                if newpix == None:
                    newData.append(item)
                else:
                    r,g,b = hex2rgb(newpix)
                    newData.append((r,g,b,255))
                    digit+=1
            else:
                newData.append(item)
    
        img.putdata(newData)
        img.save( 'out_' + filename,"PNG")
        return "Completed!!"
    
    return "Incorrect Image Mode"


def retr(filename):
    img = Image.open(filename)
    binary = ""

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        for item in datas:
            digit = decode(rgb2hex(item[0],item[1],item[2]))
            if digit == None:
                pass
            else:
                binary = binary + digit
                if binary[-16:] =='1111111111111110':
                    print("Success")
                    return bin2str(binary[:-16])
        
        return bin2str(binary)
    
    return "Incorrect Image Mode"

def Main():
    parser = optparse.OptionParser('usage %prog '+'-e/-d <target file>')
    parser.add_option('-e',dest='hide',type='string',help='target picture path to hide text')
    parser.add_option('-d',dest='retr',type='string',help='target picture path to retrieve text')

    (options, args) = parser.parse_args()

    if (options.hide != None):
        text = "{0}".format(raw_input("Enter a message to hide: "))
        print(hide(options.hide, text  ))
    elif(options.retr!=None):
        print(retr(options.retr))
    else:
        print(parser.usage)
        exit(0)

if __name__ == '__main__':
    Main()