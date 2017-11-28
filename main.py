import speech_recognition as sr #Python speech recognition
from gtts import gTTS   #Google Text To Speech
import os   #Using the System's sound playback software
import busreader    #Using the busreader Eric wrote

r = sr.Recognizer() #speech recognition's recognizer
m = sr.Microphone() #

b = busreader.BusData()

str1 = 'weather'
str2 = 'bus'
str3 = 'find'
str4 = 'calender'

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))
            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))
            if value.find(str1) > -1:
                pass
            elif value.find(str2) > -1:
                for busstopname in b.busstopnames:
                    if value.lower().find(busstopname.lower()) > -1:
                        departures = b.getdeparturesbystopname(busstopname)['departures']
                        text = ''
                        count = 0
                        for departure in departures:
                            if (departure['expected_mins'] > 5 and count >= 3):
                                break
                            text += departure['headsign']
                            text += ' is arriving in '
                            text += str(departure['expected_mins'])
                            text += ' minutes. '
                            count += 1
                        tts = gTTS(text=text, lang='en')
                        tts.save('bus.mp3')
                        os.system('bus.mp3')
            elif value.find(str3) > -1:
                print ("finding the object")
                #bluetooth function here

                #bluetooth function ends
                pass
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
