import sys
import os
import re
import imageio_ffmpeg as ffmpeg
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QProgressBar, QHBoxLayout, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QIcon
import yt_dlp

# FFmpeg yolunu ayarla
FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()

# İndirilecek dosyaların kaydedileceği klasör
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Desteklenen platformları sadece YouTube ile sınırlı tutalım
SUPPORTED_SITES = ["youtube.com", "youtu.be"]

def is_supported_url(url):
    return any(site in url for site in SUPPORTED_SITES)

class DownloaderThread(QThread):
    update_status = pyqtSignal(str)
    update_progress = pyqtSignal(int, str)
    show_progress_bar = pyqtSignal()
    download_finished = pyqtSignal()

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
            "ffmpeg_location": FFMPEG_PATH,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "progress_hooks": [self.progress_hook],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                title = info_dict.get("title", "Bilinmeyen Şarkı")
                self.update_status.emit(f"Şarkı: {title}")
                self.show_progress_bar.emit()
                ydl.download([self.url])
                self.update_status.emit("İndirme tamamlandı!")
                self.download_finished.emit()
        except Exception as e:
            self.update_status.emit(f"Hata: {str(e)}")
            self.download_finished.emit()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 1)
            percent = int((downloaded / total) * 100)
            eta = d.get('eta', 'Bilinmiyor')
            self.update_progress.emit(percent, f"Kalan Süre: {eta} sn")

class MusicDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    from PyQt6.QtGui import QIcon

class MusicDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Müzik İndirici")
        self.setGeometry(100, 100, 400, 250)

        # İkonu ayarla
        self.setWindowIcon(QIcon("icon.ico"))

        self.layout = QVBoxLayout()

        self.label = QLabel("YouTube URL'sini girin:")
        self.layout.addWidget(self.label)

        self.url_input = QLineEdit(self)
        self.layout.addWidget(self.url_input)

        self.download_button = QPushButton("İndir", self)
        self.download_button.clicked.connect(self.download_audio)
        self.layout.addWidget(self.download_button)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        self.progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setHidden(True)
        self.progress_layout.addWidget(self.progress_bar)

        self.eta_label = QLabel("")
        self.progress_layout.addWidget(self.eta_label)

        self.layout.addLayout(self.progress_layout)
        self.setLayout(self.layout)


    def download_audio(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("Lütfen bir URL girin!")
            return

        if not is_supported_url(url):
            self.status_label.setText("Bu link desteklenmiyor!")
            return

        self.status_label.setText("Bağlantı kontrol ediliyor...")
        self.progress_bar.setValue(0)
        self.progress_bar.setHidden(True)
        self.eta_label.setText("")
        self.download_button.setEnabled(False)

        self.thread = DownloaderThread(url)
        self.thread.update_status.connect(self.update_status)
        self.thread.update_progress.connect(self.update_progress)
        self.thread.show_progress_bar.connect(self.show_progress_bar)
        self.thread.download_finished.connect(self.download_completed)
        self.thread.start()

    def update_status(self, status):
        self.status_label.setText(status)

    def update_progress(self, percent, eta):
        self.progress_bar.setValue(percent)
        self.eta_label.setText(eta)

    def show_progress_bar(self):
        self.progress_bar.setHidden(False)

    def download_completed(self):
        QMessageBox.information(self, "İndirme Tamamlandı", "İndirme başarıyla tamamlandı!")
        self.download_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicDownloader()
    window.show()
    sys.exit(app.exec())
