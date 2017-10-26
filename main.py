from threading import Thread
import time
import serial
import speech_recognition as sr
import pyowm
from gtts import gTTS
import os

port = 'com3'

last_received = ''

owm = pyowm.OWM('bd5e378503939ddaee76f12ad7a97608')

observation = owm.weather_at_place('Urbana, IL')

w = observation.get_weather()

r = sr.Recognizer()
m = sr.Microphone()

str1 = 'weather'
weatherstrs = ['weather']
objectstrs = ['find']
busstrs = ['bus']

def receiving(serial_port):
    global last_received
    buffer = ''
    while True:
        buffer += serial_port.read_all()
        if '\n' in buffer:
            lines = buffer.split('\n')  # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            # If the Arduino sends lots of empty lines, you'll lose the last
            # filled line, so you could make the above statement conditional
            # like so: if lines[-2]: last_received = lines[-2]
            buffer = lines[-1]


def listening():
    with m as source: r.adjust_for_ambient_noise(source)
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        try:
            recognizedvalue = r.recognize_google(audio)
            print(u"You said {}".format(recognizedvalue).encode("utf-8"))
            if recognizedvalue.find(str1) > -1:
                temperature = w.get_temperature('fahrenheit')
                print(temperature)
                tts = gTTS(text=('The temperature is ' + str(temperature['temp']) + 'Fahrenheit'), lang='en')
                tts.save('weather.mp3')
                os.system('weather.mp3')
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            pass

class SerialData(object):
    def __init__(self):
        try:
            self.serial_port = serial.Serial(port,115200)
        except serial.serialutil.SerialException:
            # no serial connection
            self.serial_port = None
        else:
            Thread(target=receiving, args=(self.serial_port,)).start()

    def send(self, data):
        self.serial_port.write(data + ",")

    def next(self):
        if self.serial_port is None:
            # return anything so we can test when Arduino isn't connected
            return 100
        # return a float value or try a few times until we get one
        for i in range(40):
            raw_line = last_received
            try:
                return float(raw_line.strip())
            except ValueError:
                print 'bogus data', raw_line
                time.sleep(.005)
        return 0.

    def __del__(self):
        if self.serial_port is not None:
            self.serial_port.close()


if __name__ == '__main__':
    s = SerialData()
    Thread(target=listening).start()