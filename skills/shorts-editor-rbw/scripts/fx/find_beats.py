# -*- coding: utf-8 -*-
# Do beat bai nhac -> in danh sach moc giay cac phach (de cat canh dung nhac)
import librosa

y, sr = librosa.load("nhac.mp3", duration=90, mono=True)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
try:
    tempo = float(tempo)
except TypeError:
    tempo = float(tempo[0])
print("TEMPO %.1f BPM" % tempo)
print(" ".join("%.3f" % b for b in beats))
