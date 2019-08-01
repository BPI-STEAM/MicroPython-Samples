from task import *

from machine import Pin, PWM
from utime import sleep_ms

from music_bulid_in import *


class RTTTL(object):

    normal_tone = {
        'A1': 55, 'B1': 62, 'C1': 33, 'D1': 37, 'E1': 41, 'F1': 44, 'G1': 49,

        'A2': 110, 'B2': 123, 'C2': 65, 'D2': 73, 'E2': 82, 'F2': 87, 'G2': 98,

        'A3': 220, 'B3': 247, 'C3': 131, 'D3': 147, 'E3': 165, 'F3': 175, 'G3': 196,

        'A4': 440, 'B4': 494, 'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392,

        'A5': 880, 'B5': 988, 'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784,

        'A6': 1760, 'B6': 1976, 'C6': 1047, 'D6': 1175, 'E6': 1319, 'F6': 1397, 'G6': 1568,

        'A7': 3520, 'B7': 3951, 'C7': 2093, 'D7': 2349, 'E7': 2637, 'F7': 2794, 'G7': 3135,

        'A8': 7040, 'B8': 7902, 'C8': 4186, 'D8': 4699, 'E8': 5274, 'F8': 5588, 'G8': 6271,

        'A9': 14080, 'B9': 15804
    }

    rising_tone = {
        'A1': 58, 'C1': 35, 'D1': 39, 'F1': 46, 'G1': 52,

        'A2': 117, 'C2': 69, 'D2': 78, 'F2': 93, 'G2': 104,

        'A3': 233, 'C3': 139, 'D3': 156, 'F3': 185, 'G3': 208,

        'A4': 466, 'C4': 277, 'D4': 311, 'F4': 370, 'G4': 415,

        'A5': 932, 'C5': 554, 'D5': 622, 'F5': 740, 'G5': 831,

        'A6': 1865, 'C6': 1109, 'D6': 1245, 'F6': 1480, 'G6': 1661,

        'A7': 3729, 'C7': 2217, 'D7': 2489, 'F7': 2960, 'G7': 3322,

        'A8': 7459, 'C8': 4435, 'D8': 4978, 'F8': 5920, 'G8': 6645,

        'A9': 14917
    }

    falling_tone = {
        'B1': 58, 'D1': 35, 'E1': 39, 'G1': 46, 'A1': 52,

        'B2': 117, 'D2': 69, 'E2': 78, 'G2': 93, 'A2': 104,

        'B3': 233, 'D3': 139, 'E3': 156, 'G3': 185, 'A3': 208,

        'B4': 466, 'D4': 277, 'E4': 311, 'G4': 370, 'A4': 415,

        'B5': 932, 'D5': 554, 'E5': 622, 'G5': 740, 'A5': 831,

        'B6': 1865, 'D6': 1109, 'E6': 1245, 'G6': 1480, 'A6': 1661,

        'B7': 3729, 'D7': 2217, 'E7': 2489, 'G7': 2960, 'A7': 3322,

        'B8': 7459, 'D8': 4435, 'E8': 4978, 'G8': 5920, 'A8': 6645,

        'B9': 14917
    }

    Letter = 'ABCDEFG#R'

    def set_tempo(self, ticks=4, bpm=120):
        self.ticks = ticks
        self.bpm = bpm
        self.beat = 60000 / self.bpm / self.ticks

    def set_octave(self, octave=4):
        self.octave = octave

    def set_duration(self, duration=4):
        self.duration = duration

    def reset(self):
        self.set_duration()
        self.set_octave()
        self.set_tempo()

    def __init__(self):
        self.reset()

    def parse(self, tone, dict):
        # print(tone)
        time = self.beat * self.duration
        pos = tone.find(':')
        if pos != -1:
            time = self.beat * int(tone[(pos + 1):])
            tone = tone[:pos]
        # print(tone)
        freq, tone_size = 1, len(tone)
        if 'R' in tone:
            freq = 1
        elif tone_size == 1:
            freq = dict[tone[0] + str(self.octave)]
        elif tone_size == 2:
            freq = dict[tone]
            self.set_octave(tone[1:])
        # print(int(freq), int(time))
        return int(freq), int(time)

    def rtttl(self, tone):
        # print(tone)
        pos = tone.find('#')
        if pos != -1:
            return self.parse(tone.replace('#', ''), RTTTL.rising_tone)
        pos = tone.find('B')
        if pos != -1 and pos != 0:
            return self.parse(tone.replace('B', ''), RTTTL.falling_tone)
        return self.parse(tone, RTTTL.normal_tone)

    def set_default(self, tone):
        pos = tone.find(':')
        if pos != -1:
            self.set_duration(int(tone[(pos + 1):]))
            # tone = tone[:pos]


class music(RTTTL):

    def __init__(self, pin=25):
        super(music, self).__init__()

        self.flag = ''
        self.tune = []
        self.task = Task(music.pre, self)
        self.pwm = PWM(Pin(pin))
        self.out()

    def __del__(self):
        self.stop()
        self.pwm.deinit()

    def out(self, freq=0, tim=0):
        self.pwm.freq(freq)
        self.pwm.duty(tim)
        sleep_ms(tim)

    def pre(Self):

        if Self.flag is 'play' and len(Self.tune) > 0:
            # print(Self.tune)
            tone = Self.tune[0].upper()  # all to upper
            if tone[0] in Self.Letter:
                tmp = Self.rtttl(tone)
                # print(tone)
                Self.out(tmp[0], tmp[1])
            Self.tune.pop(0)

        if Self.flag is 'pitch':
            # print(Self.tune)
            tmp = Self.tune
            for freq in (tmp[0]):
                Self.out(freq, tmp[1])
            Self.tune = []

        if Self.flag != 'stop' and len(Self.tune) == 0:
            Self.flag = 'stop'
            Self.out()

        if Self.flag == 'stop':
            sleep_ms(1000)

    def play(self, tune, duration=None):
        self.task.stop()
        self.flag = 'play'
        self.tune = list(tune)
        # print(self.tune)
        if duration is None:
            self.set_default(tune[0])
        else:
            self.set_duration(duration)
        self.task.start()

    def pitch(self, freq, tim):
        self.task.stop()
        self.flag = 'pitch'
        self.tune = list([freq, tim])
        self.task.start()

    def stop(self):
        self.flag = 'stop'
        self.task.stop()
        self.out()

def unit_test():
    tmp = music()

    tmp.play(POWER_UP)
    sleep_ms(500)
    tmp.play(POWER_UP)
    sleep_ms(1000)
    tmp.play(POWER_DOWN)
    sleep_ms(500)
    tmp.play(POWER_DOWN)
    sleep_ms(1000)

    tmp.pitch(range(880, 1760, 16), 30)
    sleep_ms(50)
    tmp.pitch(range(1760, 880, -16), 30)
    sleep_ms(50)

    tmp.play(BIRTHDAY)
    sleep_ms(15000)
    tmp.play(NYAN)
    sleep_ms(10000)
    tmp.play(PRELUDE)
    sleep_ms(10000)
    tmp.play(PYTHON)
    sleep_ms(10000)

    tmp.__del__()

__music__ = music()

play = __music__.play

def old_pitch(self, freq, tim, pin=25):
    from machine import Pin, PWM
    from utime import sleep_ms

    try:
        pwm = PWM(Pin(pin))
        pwm.freq(freq)  # set frequency
        pwm.duty(tim)  # set duty cycle
        sleep_ms(tim)
    finally:
        pwm.deinit()

pitch = old_pitch

set_tempo = __music__.set_tempo
stop = __music__.stop

if __name__ == '__main__':
    unit_test()

    play(NYAN)
    sleep_ms(1000)

    pitch(range(880, 1760, 16), 30)
    sleep_ms(50)

