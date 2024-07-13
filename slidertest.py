import numpy as np
import cv2,os,time
from hik_camera.hik_camera import HikCamera
import serial
import serial.tools.list_ports
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QMutex, QMutexLocker
from PyQt5.QtGui import QPixmap, QImage
import cv2

class Worker(QThread):
    image_signal = pyqtSignal(QImage)
    slider_value = 1

    def _init_(self, mutex):
        super()._init_()
        self.mutex = mutex
        self.running = True

        """initial_exposure = 1
        value_exp_time=10000
        value_exp_step=2500

        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "Uno" in port.description:
                arduino_light = serial.Serial(port.device, baudrate=9600, timeout=1) #port.device"""


    def run(self):

        value = None
        while self.running:

            with QMutexLocker(self.mutex):
                # İşlem yapmak için slider değerini kullanın (örn: görüntüyü ölçeklendirme)
                value = self.slider_value
                # Örneğin, burada görüntüyü ölçeklendirme işlemi yapılabilir
            
            exp_time=value
            a, b = take_frame_alfa_beta(exp_time)
            frame = fusion_alfa_beta(a, b)  
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.image_signal.emit(qt_image)


    def stop(self):
        with QMutexLocker(self.mutex):
            self.running = False
        self.wait()

    def set_slider_value(self, value):
        with QMutexLocker(self.mutex):
            self.slider_value = value
    def light_control(self, relay, command):
        # Komutu Arduino'ya gönder
        arduino_light.write((f"{relay}: {command}" + '\n').encode())
        while True:
            response = arduino_light.readline().decode().strip()
            print(response)
            if response == f"{relay}: {command}":
                return True
            else:
                return False
                
    def take_frame_alfa_beta(self,exp):
            ips = HikCamera.get_all_ips()

            print("All camera IP adresses:", ips)
            ip= ips[0]

            cam = HikCamera(ip=ip)
            with cam:
                cam["ExposureAuto"] = "Off"
                cam["ExposureTime"] = exp

                # alfa on , beta off
                light_control("alfa", "on")
                light_control("beta", "off")
                time.sleep(.2)
                
                alfa = cam.robust_get_frame()
                time.sleep(.5)
                                
                # alfa off , beta on
                light_control("alfa", "off")
                light_control("beta", "on")
                time.sleep(.2)

                beta = cam.robust_get_frame()
                time.sleep(.5)
                
            return alfa, beta

    def fusion_alfa_beta(self, alfa_test, beta_test):
        ab_dir = r"C:\Program Files (x86)\Microsoft\UGURLUGLASS\src\alfa_beta"

        alfa = cv2.imread(os.path.join(ab_dir , "alfa_mask.png"), cv2.IMREAD_GRAYSCALE)
        beta = cv2.imread(os.path.join(ab_dir , "beta_mask.png"), cv2.IMREAD_GRAYSCALE)

        # Orijinal görüntüler üzerinde maskeyi uygula
        result1 = cv2.bitwise_and(alfa_test, alfa_test, mask=alfa)
        result2 = cv2.bitwise_and(beta_test, beta_test, mask=beta)

        # Sonuçları birleştir
        combined_result = cv2.bitwise_or(result1, result2)

        return combined_result 


class VideoApp(QWidget):
    def _init_(self):
        super()._init_()

        self.init_ui()

        self.mutex = QMutex()
        self.worker = Worker(self.mutex)
        self.worker.image_signal.connect(self.update_image)
        self.worker.start()

    def init_ui(self):
        self.setWindowTitle('Video Capture with PyQt5')
        self.setGeometry(100, 100, 1800, 950)

        self.layout = QVBoxLayout()

        self.label = QLabel(self)
        self.label.setFixedSize(1800, 950)
        self.layout.addWidget(self.label)

        self.h_layout = QHBoxLayout()
        self.save_and_close = QPushButton("Kaydet ve Kapat")


        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(1, 100)
        self.slider.setValue(1)
        self.slider.valueChanged.connect(self.on_slider_change)
        self.h_layout.addWidget(self.slider)
        self.h_layout.addWidget(self.save_and_close)
        self.layout.addLayout(self.h_layout)

        self.setLayout(self.layout)

    def update_image(self, qt_image):
        pixmap = QPixmap.fromImage(qt_image)
        self.label.setPixmap(pixmap)

    def on_slider_change(self, value):
        self.worker.set_slider_value(value)

    def closeEvent(self, event):
        self.worker.stop()
        event.accept()


if _name_ == '_main_':
    app = QApplication(sys.argv)
    video_app = VideoApp()
    video_app.showFullScreen()
    sys.exit(app.exec_())