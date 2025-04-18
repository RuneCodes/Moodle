import matplotlib
matplotlib.use('Agg')
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
import wave
from werkzeug.utils import secure_filename
from flask_session import Session
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from io import BytesIO
from matplotlib.figure import Figure

# Configure application
app = Flask(__name__)

#Constants
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'media')
ALLOWED_FILETYPES = set(['mp3', 'wav'])
OUTPUT_FOLDER = '/workspaces/144957609//project/media/'
SAVE_PARAMS = {'dpi': 300, 'bbox_inches': 'tight', 'transparent': True}

# Configure app
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Moodle homepage
@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template('index.html')

#checks if file type is allowed (i.e. mp3 or wav)
def allowed_filetypes(filename):
    if filename.rsplit('.', 1)[1].lower() in ALLOWED_FILETYPES:
        return True
    return False

#checks if uploaded file is of type wav
def check_wav(filename):
    if filename.rsplit('.', 1)[1].lower == 'wav':
        return True
    return False

#facilitates the uploading the audio files
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file in request')
            return render_template('upload.html')
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return render_template('upload.html')

        if file and allowed_filetypes(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if not check_wav(filename):
                wav_handle = filename.rsplit('.',1)[0] + '.wav'
                wav_path = os.path.join(app.config['UPLOAD_FOLDER'], wav_handle)
                AudioSegment.from_mp3(file_path).export(wav_path, format="wav")
                os.remove(file_path)
                file_path = wav_path
                session["audio_file_path"] = file_path
                flash('File succesfully converted to WAV and uploaded!')
            else:
                flash('WAV file upload Successful!')
        else:
            flash('Invalid File Type. Only mp3 and wav files are supported')
            return render_template('upload.html')

        return redirect('/visualizer')
    else:
        return render_template('upload.html')

#saves visual from matplotlib to file in /project/media
def save_visual(graph_name):
    plt.savefig(os.path.join(OUTPUT_FOLDER, graph_name))
    plt.close()

#facilitates the visualization of the audio using matplotlib
@app.route('/visualizer', methods=['GET', 'POST'])
def visualizer():
    if request.method == 'GET':
        #important values
        audio_file_path = '/workspaces/144957609/project/media/018002_grandfather-clock-at-12-o39clock-54919.wav' #session["audio_file_path"]
        wav = wave.open(audio_file_path, 'rb')
        sample_frequency = wav.getframerate() # # of samples per second
        n_samples = wav.getnframes() # # of total samples
        duration = n_samples / sample_frequency
        wav_amplitudes = wav.readframes(n_samples) # reads amp for frames in all samples in file
        amp_array = np.frombuffer(wav_amplitudes, dtype=np.int16) # amp array for both channels
        channel_count = wav.getnchannels()
        channels = [amp_array[0::2], amp_array[1::2]]
        channel_color = ['rebeccapurple', 'cornflowerblue']
        channel_directions = ['Left', 'Right']
        timestamps = np.linspace(0, n_samples/sample_frequency, num=n_samples)

        plt.rcParams.update({'font.size':20})

        # left and right channels
        for x, channel in enumerate(channels):
            plt.figure(figsize=(16,6))
            plt.plot(timestamps, channel, channel_color[x])
            plt.title(f'{channel_directions[x]} Channels')
            plt.ylabel('Amplitude')
            plt.xlabel('Time (s)')
            plt.xlim(0, duration)
            save_visual(f'{channel_directions[x]}Amplitude.png')

        # relative difference between l and right channel
        max_amp = np.iinfo(np.int16).max
        channel_difference = np.abs(abs(amp_array[0::2].astype(np.float32)) - abs(amp_array[1::2].astype(np.float32))) / max_amp
        plt.figure(figsize=(16,6))
        plt.plot(timestamps, channel_difference, 'olivedrab')
        plt.title('Channel Amplitude Difference')
        plt.ylabel('Amplitude')
        plt.xlabel('Time (s)')
        plt.xlim(0, duration)
        save_visual('AmplitudeDifference.png')

        #spectogram
        plt.figure(figsize=(16,6))
        plt.specgram(channels[0], Fs=sample_frequency, vmin=-20, vmax=50)
        plt.title("Left Frequency Spectrogram")
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')
        plt.xlim(0, duration)
        plt.colorbar()
        save_visual('spectogram.png')
    return render_template('visualizer.html')


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app)


#facilitates the visualization of the audio using matplotlib
@app.route('/live_visualizer', methods=['GET', 'POST'])
def liveVisualizer():

    #important values
    audio_file_path = '/workspaces/144957609/project/media/018002_grandfather-clock-at-12-o39clock-54919.wav' #session["audio_file_path"]
    wav = wave.open(audio_file_path, 'rb')
    sample_frequency = wav.getframerate() # # of samples per second
    n_samples = wav.getnframes() # # of total samples
    duration = n_samples / sample_frequency
    wav_amplitudes = wav.readframes(n_samples) # reads amp for frames in all samples in file
    amp_array = np.frombuffer(wav_amplitudes, dtype=np.int16) # amp array for both channels
    channel_count = wav.getnchannels()
    channels = [amp_array[0::2], amp_array[1::2]]
    channel_color = ['rebeccapurple', 'cornflowerblue']
    channel_directions = ['Left', 'Right']
    timestamps = np.linspace(0, n_samples/sample_frequency, num=n_samples)

    fig = Figure()
    fig.figsize(16,6)
    amplitude = fig.subplots()
    ax.plot([time])
