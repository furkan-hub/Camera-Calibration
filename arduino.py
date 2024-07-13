import serial

# Seri portunuzu ve baud hızını belirleyin
ser = serial.Serial('/dev/ttyUSB1', 9600)  # Windows için
# ser = serial.Serial('/dev/ttyACM0', 9600)  # Linux için

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
