from utime import sleep, sleep_ms
from machine import Pin, PWM

octave = {
    'R1': 0, 'A1': 55, '#A1': 58, 'B1': 62, 'C1': 33, '#C1': 35, 'D1': 37, '#D1': 39, 'E1': 41, 'F1': 44, '#F1': 46, 'G1': 49, '#G1': 52,

    'R2': 0, 'A2': 110, '#A2': 117, 'B2': 123, 'C2': 65, '#C2': 69, 'D2': 73, '#D2': 78, 'E2': 82, 'F2': 87, '#F2': 93, 'G2': 98, '#G2': 104,

    'R3': 0, 'A3': 220, '#A3': 233, 'B3': 247, 'C3': 131, '#C3': 139, 'D3': 147, '#D3': 156, 'E3': 165, 'F3': 175, '#F3': 185, 'G3': 196, '#G3': 208,

    'R4': 0, 'A4': 440, '#A4': 466, 'B4': 494, 'C4': 262, '#C4': 277, 'D4': 294, '#D4': 311, 'E4': 330, 'F4': 349, '#F4': 370, 'G4': 392, '#G4': 415,

    'R5': 0, 'A5': 880, '#A5': 932, 'B5': 988, 'C5': 523, '#C5': 554, 'D5': 587, '#D5': 622, 'E5': 659, 'F5': 698, '#F5': 740, 'G5': 784, '#G5': 831,

    'R6': 0, 'A6': 1760, '#A6': 1865, 'B6': 1976, 'C6': 1047, '#C6': 1109, 'D6': 1175, '#D6': 1245, 'E6': 1319, 'F6': 1397, '#F6': 1480, 'G6': 1568, '#G6': 1661,

    'R7': 0, 'A7': 3520, '#A7': 3729, 'B7': 3951, 'C7': 2093, '#C7': 2217, 'D7': 2349, '#D7': 2489, 'E7': 2637, 'F7': 2794, '#F7': 2960, 'G7': 3135, '#G7': 3322,

    'R8': 0, 'A8': 7040, '#A8': 7459, 'B8': 7902, 'C8': 4186, '#C8': 4435, 'D8': 4699, '#D8': 4978, 'E8': 5274, 'F8': 5588, '#F8': 5920, 'G8': 6271, '#G8': 6645,

    'R9': 0, 'A9': 14080, '#A9': 14917, 'B9': 15804
}
time = {'1': 0.3, '2': 0.35, '3': 0.4, '4': 0.5,
        '5': 0.6, '6': 0.7, '7': 0.8, '8': 1.0}

Letter = 'ABCDEFG#'


def play(tune, pin=25):
    try:
        pwm = PWM(Pin(pin))
        for val in tune:
            val = val.upper()
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
                    if '#' in val:
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
                if ':' in val:
                    tim = time[val[-1]]
                    if val[0] in Letter:
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


BIRTHDAY = [
    "C5:3", "C5:2", "D5:4", "C5:4", "F5", "E5:8",
    "C5:3", "C5:2", "D5:4", "C5:4", "G5", "F5:8",
    "C5:3", "C5:2", "C6:4", "A6", "F5", "E5", "D5",
    "#A6:3", "#A6:2", "A6:4", "F5", "G5", "F5:8"
]


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
