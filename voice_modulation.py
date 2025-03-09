import pyttsx3
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from scipy import signal
import librosa
import googletrans
from googletrans import Translator

class VoiceModulation:
    def __init__(self, language='es'):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1)
        self.pitch = 1.0
        self.translator = Translator()
        self.language = language

    def set_tone(self, pitch):
        self.pitch = pitch

    def set_speed(self, speed):
        self.engine.setProperty('rate', speed)

    def apply_audio_effect(self, effect_type, input_audio, output_audio):
        sample_rate, audio_data = librosa.load(input_audio, sr=None)
        if effect_type == 'echo':
            echo = np.zeros_like(audio_data)
            echo[1000:] = audio_data[:-1000]
            audio_data = audio_data + 0.6 * echo
        elif effect_type == 'distortion':
            audio_data = np.clip(audio_data * 2, -1, 1)
        write(output_audio, sample_rate, np.int16(audio_data * 32767))

    def text_to_speech(self, text, lang=None):
        if lang and lang != self.language:
            text = self.translator.translate(text, src=lang, dest=self.language).text
        self.engine.say(text)
        self.engine.runAndWait()

    def real_time_voice_modulation(self, duration=5, effect=None):
        sample_rate = 44100
        print("Recording...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
        sd.wait()
        if effect == 'reverb':
            recording = signal.convolve(recording, np.ones((1000,)) / 1000, mode='same')
        write('output.wav', sample_rate, recording)
        print("Recording saved as output.wav")

    def translate_and_speak(self, text, target_language='en'):
        translated_text = self.translator.translate(text, src=self.language, dest=target_language).text
        print(f'Translated Text: {translated_text}')
        self.text_to_speech(translated_text, lang=target_language)

    def voice_cloning(self, reference_audio, text):
        print("Voice cloning feature is not yet implemented.")

    def pitch_shift(self, input_audio, output_audio, shift_steps=2):
        y, sr = librosa.load(input_audio)
        y_shifted = librosa.effects.pitch_shift(y, sr, shift_steps)
        write(output_audio, sr, np.int16(y_shifted * 32767))

    def apply_advanced_effects(self, input_audio, output_audio, effect_type='robotic'):
        sample_rate, audio_data = librosa.load(input_audio, sr=None)
        if effect_type == 'robotic':
            audio_data = np.sign(audio_data) * np.sqrt(np.abs(audio_data))
        write(output_audio, sample_rate, np.int16(audio_data * 32767))

# Ejemplo de uso
voice_mod = VoiceModulation()
voice_mod.set_tone(1.2)
voice_mod.set_speed(120)
voice_mod.text_to_speech("Hola, soy la IA Leila")
voice_mod.apply_audio_effect('echo', 'input.wav', 'output.wav')
voice_mod.real_time_voice_modulation(duration=5, effect='reverb')
voice_mod.translate_and_speak("Hola, ¿cómo estás?", 'en')
voice_mod.pitch_shift('input.wav', 'output_shifted.wav', shift_steps=3)
voice_mod.apply_advanced_effects('input.wav', 'output_advanced.wav', effect_type='robotic')
