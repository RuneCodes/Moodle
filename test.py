import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from pydub import AudioSegment
#sound = AudioSegment.from_mp3("/media/mp3/file.mp3")
#sound.export("/media/wav/file.wav", format="wav")


IMG_OUTPUT_PATH = Path('img')
SAVE_PARAMS = {'dpi': 300, 'bbox_inches': 'tight', 'transparent': True}


def plot_signal(signal, time=None):
    plt.rcParams.update({'font.size': 20})
    COLOR = '#ef7600'

    samples_count = 100 #signal.shape[0]

    plt.figure(figsize=(12,6))
    if time is None:
        xlim = [0, samples_count]
        plt.plot(signal, COLOR, linewidth=3)
        plt.xlabel('samples')
    else:
        xlim = [0, time]
        plt.plot(time, signal, COLOR, linewidth=3)
        plt.xlabel('time [s]')
    plt.hlines(0, xlim[0], xlim[1], 'k')
    plt.ylabel('amplitude')
    plt.xlim(xlim)
    plt.yticks([-1, 0, 1])

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)


def plot_signal_and_save(signal, output_path, time=None):
    plot_signal(signal, time)
    # plt.show() # closes the figure
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, **SAVE_PARAMS)
    plt.close()

plot_signal_and_save(440, IMG_OUTPUT_PATH, 3)


def generate_sound(freq, amplitude):

    sound = Sound()
    sound.set_frequency(sound, freq)
    sound.set_volume(sound, amplitude)

    return sound

def play_sound(sound):

    sound.start()
    while button is True:
        sound.set_frequency(frequency)
        sound.set_volume(amplitude)

    return sound

'''
    time = np.arange(length_seconds * sample_rate) / sample_rate

    sine = np.sin(2 * np.pi * frequency * time) * amplitude
    plot_signal_and_save(sine[:1000], IMG_OUTPUT_PATH / 'sine_signal.png', time[:1000])
'''
class Sound:
    def __init__(self, sample_rate=44100):
        #default values
        self.sample_rate = sample_rate
        self.frequency = 440
        self.volume = .5
        self.is_playing = False

        # activate pyaudio

        def start(self):
            self.is_playing = True

        def stop(self):
            self.is_playing = False

        def set_frequency(self, freq):
            self.frequency = freq

        def set_volume(self, amplitude):
            self.volume = max(0, min(1, amplitude))



