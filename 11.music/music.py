from utime import sleep, sleep_ms
from machine import Pin, PWM

octave = {
    'R1': 1, 'A1': 55, '#A1': 58, 'BB1': 58, 'B1': 62, 'C1': 33, '#C1': 35, 'DB1': 35, 'D1': 37, '#D1': 39, 'EB1': 39, 'E1': 41, 'F1': 44, '#F1': 46, 'GB1': 46, 'G1': 49, '#G1': 52, 'AB1': 52,

    'R2': 1, 'A2': 110, '#A2': 117, 'BB2': 117, 'B2': 123, 'C2': 65, '#C2': 69, 'DB2': 69, 'D2': 73, '#D2': 78, 'EB2': 78, 'E2': 82, 'F2': 87, '#F2': 93, 'GB2': 93, 'G2': 98, '#G2': 104, 'AB2': 104,

    'R3': 1, 'A3': 220, '#A3': 233, 'BB3': 233, 'B3': 247, 'C3': 131, '#C3': 139, 'DB3': 139, 'D3': 147, '#D3': 156, 'EB3': 156, 'E3': 165, 'F3': 175, '#F3': 185, 'GB3': 185, 'G3': 196, '#G3': 208, 'AB3': 208,

    'R4': 1, 'A4': 440, '#A4': 466, 'BB4': 466, 'B4': 494, 'C4': 262, '#C4': 277, 'DB4': 277, 'D4': 294, '#D4': 311, 'EB4': 311, 'E4': 330, 'F4': 349, '#F4': 370, 'GB4': 370, 'G4': 392, '#G4': 415, 'AB4': 415,

    'R5': 1, 'A5': 880, '#A5': 932, 'BB5': 932, 'B5': 988, 'C5': 523, '#C5': 554, 'DB5': 554, 'D5': 587, '#D5': 622, 'EB5': 622, 'E5': 659, 'F5': 698, '#F5': 740, 'GB5': 740, 'G5': 784, '#G5': 831, 'AB5': 831,

    'R6': 1, 'A6': 1760, '#A6': 1865, 'BB6': 1865, 'B6': 1976, 'C6': 1047, '#C6': 1109, 'DB6': 1109, 'D6': 1175, '#D6': 1245, 'EB6': 1245, 'E6': 1319, 'F6': 1397, '#F6': 1480, 'GB6': 1480, 'G6': 1568, '#G6': 1661, 'AB6': 1661,

    'R7': 1, 'A7': 3520, '#A7': 3729, 'BB7': 3729, 'B7': 3951, 'C7': 2093, '#C7': 2217, 'DB7': 2217, 'D7': 2349, '#D7': 2489, 'EB7': 2489, 'E7': 2637, 'F7': 2794, '#F7': 2960, 'GB7': 2960, 'G7': 3135, '#G7': 3322, 'AB7': 3322,

    'R8': 1, 'A8': 7040, '#A8': 7459, 'BB8': 7459, 'B8': 7902, 'C8': 4186, '#C8': 4435, 'DB8': 4435, 'D8': 4699, '#D8': 4978, 'EB8': 4978, 'E8': 5274, 'F8': 5588, '#F8': 5920, 'GB8': 5920, 'G8': 6271, '#G8': 6645, 'AB8': 6645,

    'R9': 1, 'A9': 14080, '#A9': 14917, 'BB9': 14917, 'B9': 15804
}
DADADADUM = ['r4:2',  'g',  'g',  'g', 'eb:8',  'r:2',  'f',  'f', 'f',  'd:8']

ETERTAINER = ['d4:1',  'd#',  'e',  'c5:2',  'e4:1', 'c5:2',  'e4:1',  'c5:3',  'c:1',  'd', 'd#',  'e',  'c',
              'd',  'e:2',  'b4:1',  'd5:2', 'c:4']


PRELUDE = ['c4:1',  'e',  'g',  'c5',  'e',  'g4',  'c5',  'e',  'c4',  'e',

           'g',  'c5',  'e',  'g4',  'c5',  'e',  'c4',  'd',  'g',  'd5',  'f',

           'g4',  'd5',  'f',  'c4',  'd',  'g',  'd5',  'f',  'g4',  'd5',  'f',

           'b3',  'd4',  'g',  'd5',  'f',  'g4',  'd5',  'f',  'b3',  'd4',  'g',

           'd5',  'f',  'g4',  'd5',  'f',  'c4',  'e',  'g',  'c5',  'e',  'g4',

           'c5',  'e',  'c4',  'e',  'g',  'c5',  'e',  'g4',  'c5',  'e']


ODE = ['e4',  'e',  'f',  'g',  'g',  'f',  'e',  'd',  'c',  'c',  'd',  'e', 'e:6',  'd:2',

       'd:8',  'e:4',  'e',  'f',  'g',  'g',  'f',  'e',  'd',  'c',  'c',  'd',  'e',  'd:6',

       'c:2',  'c:8']


NYAN = ['f#5:2',  'g#',  'c#:1',  'd#:2', 'b4:1',  'd5:1',  'c#',  'b4:2',  'b',

        'c#5',  'd',  'd:1',  'c#',  'b4:1', 'c#5:1',  'd#',  'f#',  'g#',  'd#',

        'f#',  'c#',  'd',  'b4',  'c#5',  'b4', 'd#5:2',  'f#',  'g#:1',  'd#',

        'f#',  'c#',  'd#',  'b4',  'd5',  'd#',  'd', 'c#',  'b4',  'c#5',  'd:2',  'b4:1',  'c#5',

        'd#',  'f#',  'c#',  'd',  'c#',  'b4', 'c#5:2',  'b4',  'c#5',  'b4',  'f#:1',

        'g#',  'b:2',  'f#:1',  'g#',  'b', 'c#5',  'd#',  'b4',  'e5',  'd#',  'e',  'f#',

        'b4:2',  'b',  'f#:1',  'g#',  'b',  'f#', 'e5',  'd#',  'c#',  'b4',  'f#',  'd#',  'e',

        'f#',  'b:2',  'f#:1',  'g#',  'b:2', 'f#:1',  'g#',  'b',  'b',  'c#5',  'd#',

        'b4',  'f#',  'g#',  'f#',  'b:2',  'b:1', 'a#',  'b',  'f#',  'g#',  'b',  'e5',  'd#',  'e',

        'f#',  'b4:2',  'c#5']


RINGTONE = ['c4:1',  'd',  'e:2',  'g',  'd:1',  'e',  'f:2',

            'a',  'e:1',  'f',  'g:2',  'b',  'c5:4']


FUNK = [

    'c2:2',  'c',  'd#',  'c:1',  'f:2',  'c:1',

    'f:2',  'f#',  'g',  'c',  'c',  'g',  'c:1',

    'f#:2',  'c:1',  'f#:2',  'f',  'd#']


BLUES = [

    'c2:2',  'e',  'g',  'a',  'a#',  'a',  'g',  'e',

    'c2:2',  'e',  'g',  'a',  'a#',  'a',  'g',  'e',  'f',  'a',

    'c3',  'd',  'd#',  'd',  'c',  'a2',  'c2:2',  'e',  'g',

    'a',  'a#',  'a',  'g',  'e',  'g',  'b',  'd3',  'f',  'f2',  'a',

    'c3',  'd#',  'c2:2',  'e',  'g',  'e',  'g',  'f',  'e',

    'd']


BIRTHDAY = [

    'c4:3',  'c:1',  'd:4',  'c:4',  'f',

    'e:8',  'c:3',  'c:1',  'd:4',  'c:4',

    'g',  'f:8',  'c:3',  'c:1',  'c5:4',  'a4',

    'f',  'e',  'd',  'a#:3',  'a#:1',  'a:4',

    'f',  'g',  'f:8']


WEDDING = [

    'c4:4',  'f:3',  'f:1',  'f:8',  'c:4',

    'g:3',  'e:1',  'f:8',  'c:4',  'f:3',

    'a:1',  'c5:4',  'a4:3',  'f:1',  'f:4',

    'e:3',  'f:1',  'g:8']


FUNERAL = [

    'c3:4',  'c:3',  'c:1',  'c:4',

    'd#:3',  'd:1',  'd:3',  'c:1',

    'c:3',  'b2:1',  'c3:4']


PUCHLINE = [

    'c4:3',  'g3:1',  'f#',  'g',  'g#:3',  'g',

    'r',  'b',  'c4']


PYTHOY = [

    'd5:1',  'b4',  'r',  'b',  'b',  'a#',  'b',  'g5',  'r',

    'd',  'd',  'r',  'b4',  'c5',  'r',  'c',  'c',  'r',  'd',

    'e:5',  'c:1',  'a4',  'r',  'a',  'a',  'g#',  'a',

    'f#5',  'r',  'e',  'e',  'r',  'c',  'b4',  'r',  'b',  'b',  'r',

    'c5',  'd:5',  'd:1',  'b4',  'r',  'b',  'b',  'a#',

    'b',  'b5',  'r',  'g',  'g',  'r',  'd',  'c#',  'r',  'a',  'a',

    'r',  'a',  'a:5',  'g:1',  'f#:2',  'a:1',

    'a',  'g#',  'a',  'e:2',  'a:1',  'a',  'g#',

    'a',  'd',  'r',  'c#',  'd',  'r',  'c#',  'd:2',

    'r:3']


BADDY = [

    'c3:3',  'r',  'd:2',  'd#',  'r',  'c',  'r',  'f#:8']


CHASE = [

    'a4:1',  'b',  'c5',  'b4',  'a:2',  'r',  'a:1',  'b',  'c5',  'b4',  'a:2',  'r',  'a:2',  'e5',  'd#',  'e',
    'f',  'e',  'd#',  'e',  'b4:1',  'c5',  'd',  'c',  'b4:2',  'r',  'b:1',  'c5',  'd',  'c',  'b4:2',  'r',  'b:2',
    'e5',  'd#',  'e',  'f',  'e',  'd#',  'e']


BA_DING = [
    'b5:1',  'e6:3']


WAWAWAWAA = ['e3:3',  'r:1',  'd#:3',  'r:1',  'd:4',  'r:1',  'c#:8']


JUMP_UP = ['c5:1',  'd',  'e',  'f',  'g']


JUMP_DOW = ['g5:1',  'f',  'e',  'd',  'c']


POWER_UP = ['g4:1',  'c5',  'e',  'g:2',  'e:1',  'g:3']


POWER_DOW = ['g5:1',  'd#',  'c',  'g4:2',  'b:1',  'c5:3']


time = {'1': 0.3, '2': 0.35, '3': 0.4, '4': 0.5,
        '5': 0.6, '6': 0.7, '7': 0.8, '8': 1.0}

Letter = 'ABCDEFG#R'


def play(tune, pin=25):
    try:
        pwm = PWM(Pin(pin))
        for val in tune:
            val = val.upper()  # 全部转为大写
            size = len(val)
            tim = 0.46
            if ('#' in val) and (val[0] != '#'):
                tem = val.find('#')
                val = val[tem] + val[0:tem] + val[tem + 1:]  # 把#移动到字符串的最开始
                # print(val)
            # print(size)
            if size == 1:
                if val in Letter:
                    freq = octave[(val + '4')]
            elif size == 2:
                if val[0] in Letter:
                    if '#' in val or val[-1] == 'B':
                        freq = octave[(val + '4')]
                    else:
                        freq = octave[val]
            elif size == 3:
                if ':' in val:
                    tim = time[val[-1]]
                    if val[0] in Letter:
                        freq = octave[(val[0] + '4')]
                else:
                    freq = octave[val]

            elif size == 4:
                tim = time[val[-1]]
                if '#' in val or val[1] == 'B':
                    if val[0] in Letter:
                        freq = octave[val[0:2]+'4']
                else:
                    freq = octave[val[0:2]]
            elif size == 5:
                if ':' in val:
                    tim = time[val[-1]]
                    if val[0] in Letter:
                        freq = octave[val[0:3]]
            # print(tim)
            pwm.freq(freq)  # set frequency
            # print('pwm.freq ' + str(pwm.freq()))  # get current frequency
            pwm.duty(500)  # set duty cycle
            sleep(tim)
    finally:
        pwm.deinit()


def pitch(freq, tim, pin=25):
    try:
        pwm = PWM(Pin(pin))
        pwm.freq(freq)  # set frequency
        # print('pwm.freq ' + str(pwm.freq()))  # get current frequency
        pwm.duty(500)  # set duty cycle
        sleep_ms(tim)
    finally:
        pwm.deinit()


def unit_test():
    print('The unit test code is as follows')
    print('\n\
        tune = ["C4:4", "D4:4", "E4:4", "C4:4", "C4:4", "D4:4", "E4:4", "C4:4",\n\
                "E4:4", "F4:4", "G4:8", "E4:4", "F4:4", "G4:8"]\n\
        play(tune)\n\
        for freq in range(880, 1760, 16):\n\
            pitch(freq, 30)\n\
        for freq in range(1760, 880, -16):\n\
            pitch(freq, 30)\n\
    ')
    tune = ["C4:4", "D4:4", "E4:4", "C4:4", "C4:4", "D4:4", "E4:4", "C4:4",
            "E4:4", "F4:4", "G4:8", "E4:4", "F4:4", "G4:8"]
    play(tune)
    for freq in range(880, 1760, 16):
        pitch(freq, 30)
    for freq in range(1760, 880, -16):
        pitch(freq, 30)

if __name__ == '__main__':
    unit_test()
