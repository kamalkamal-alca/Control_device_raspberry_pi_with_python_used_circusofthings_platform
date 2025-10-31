import requests   
import json     
import time
import RPi.GPIO as GPIO

KEY_1   ="xxxxxxxxxxx"              
VALUE_1 = "ON1"                
TOKEN_1  ="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" #the token is found under account in circusofthings.com

data_1={'Key':'0','Value':0,'Token':'0'}     
# Configure GPIO
GPIO.setmode(GPIO.BCM)
dataPin  = 24  # Pin for Data (GPIO 24)
latchPin = 23  # Pin for Latch (GPIO 23)
clockPin = 18  # Pin for Clock (GPIO 18)

GPIO.setup(dataPin, GPIO.OUT)
GPIO.setup(clockPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT)

# Variables
shift_data = 0b00000000  # Initial state of the shift register (all LEDs off)
previous_shift_data = 0b00000000

# Function to update shift register
def update_shift_register():
    global shift_data, previous_shift_data
    if shift_data != previous_shift_data:
        previous_shift_data = shift_data
        GPIO.output(latchPin, GPIO.LOW)
        shift_out(shift_data)
        GPIO.output(latchPin, GPIO.HIGH)

# Shift out data (similar to Arduino's shiftOut function)
def shift_out(data):
    for i in range(8):
        GPIO.output(clockPin, GPIO.LOW)
        GPIO.output(dataPin, (data >> (7 - i)) & 0x01)
        GPIO.output(clockPin, GPIO.HIGH)

while True:
    data_1['Key'] = KEY_1 
    data_1['Value']=VALUE_1
    data_1['Token']=TOKEN_1

    data_1['Lat'] = 62.3725  #denoted in decimaldegrees
    data_1['Lon'] = 9.061667
    data_1['Alt'] = 1985 
    response=requests.put('https://circusofthings.com/WriteValue',
				data=json.dumps(data_1),headers={'Content-Type':'application/json'}) #There can be additional things 
    if(response.status_code==200):
        print("succsess")
    else:
        print("error %d" % (response.status_code))

    payload = data_1
    #print(data_1)
    response=requests.get('https://circusofthings.com/ReadValue',params=payload)

    #print(response.content) #prints the content

    datahandling=json.loads(response.content)  
    print(datahandling["Value"]) #here we parse and get the value of the signal
    
    # Remove the global declaration here since we're in the global scope already
    if (datahandling["Value"])==0:
       shift_data |= 0b00000001  # Turn LED1 on
       print("LED1=0")
    elif (datahandling["Value"])== 1:
       shift_data &= 0b11111110  # Turn LED1 off
       print("LED1=1")

    elif (datahandling["Value"])== 2:
       shift_data |= 0b00000010  # Turn LED2 on
       print("LED2=0")
    elif (datahandling["Value"])== 3:
       shift_data &= 0b11111101  # Turn LED2 off       
       print("LED2=1")

    elif (datahandling["Value"])== 4:
       shift_data |= 0b00000100  # Turn LED3 on
       print("LED3=0")
    elif (datahandling["Value"])== 5:
       shift_data &= 0b11111011  # Turn LED3 off
       print("LED3=1")
    elif (datahandling["Value"])== 6:
       shift_data |= 0b00001000  # Turn LED4 on
       print("LED4=0")
    elif (datahandling["Value"])== 7:
       shift_data &= 0b11110111  # Turn LED4 off
       print("LED4=1")
    
    # Add update call to actually send data to shift register
    update_shift_register()

    time.sleep(3)
