import sys
import pyvda
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, qApp,
                             QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton, QFormLayout, QMessageBox, QDesktopWidget)
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from tendo import singleton
from screen_brightness_control import set_brightness
import time
import keyboard
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

me = singleton.SingleInstance()  # prevent duplicate
each_brightness = []
process = True
icon = './images/Bright.ico'
w, h = 450, 350


class BrightnessWorker(QThread):
    exit_signal = pyqtSignal()

    def __init__(self, num_desktops, each_brightness):
        super().__init__()
        self.num_desktops = num_desktops
        self.each_brightness = each_brightness
        self.process = True

    def run(self):
        keyboard.add_hotkey('alt + e', self.exit_app)
        oneTime = [True for _ in range(self.num_desktops)]
        while self.process:
            time.sleep(0.5)
            desk = pyvda.VirtualDesktop.current().number
            if oneTime[desk - 1]:
                set_brightness(self.each_brightness[desk - 1])
                oneTime = [True for _ in range(self.num_desktops)]
                oneTime[desk - 1] = False

    def exit_app(self):  # stop functionality
        with open('./cache.txt', 'w') as file:
            file.write(str(each_brightness))
        self.process = False
        self.exit_signal.emit()
        # QApplication.quit()  # Request the application to exit


class BrightnessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker_thread = None
        self.getCache()
        self.initUI()

    def getCache(self):
        global each_brightness
        self.num_desktops = len(pyvda.get_virtual_desktops())
        self.default_val = [50] * self.num_desktops
        if os.path.exists('./cache.txt'):
            with open('./cache.txt', 'r') as file:
                vals = file.readline()[1:-1]
                vals = vals.split(',')
                if len(vals) == self.num_desktops:
                    for i in range(len(vals)):
                        try:
                            self.default_val[i] = int(vals[i])
                        except:
                            pass
        else:
            # Create cache file
            with open('./cache.txt', 'w') as f:
                pass  # Creates an empty cache file
        each_brightness = self.default_val

    def initUI(self):
        # Lunch at center of the screen
        def center_window():
            qtRectangle = self.frameGeometry()
            centerPoint = QDesktopWidget().availableGeometry().center()
            qtRectangle.moveCenter(centerPoint)
            self.move(qtRectangle.topLeft())

        if not os.path.exists(icon):  # if icon not found
            QMessageBox.critical(None, 'error', 'Icon not founded!')
            sys.exit(0)

        self.setWindowIcon(QtGui.QIcon(icon))
        self.setWindowTitle('Brightness')
        self.setGeometry(300, 300, w, h)
        center_window()

        # Create a rounded region mask to apply rounded corners
        # self.set_rounded_corners(20)

        # Disable the maximize button by modifying the window flags
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        # Optional: Disable resizing the window
        # Note: better to be flexible
        # self.setFixedSize(self.size())

        # Create the main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Form layout for brightness inputs
        form_layout = QFormLayout()

        self.brightness_inputs = []

        for i in range(self.num_desktops):
            label = QLabel(f'Desktop {i + 1} Brightness :')
            label.setStyleSheet("font-weight: bold; font-size: 18px")
            spin_box = QSpinBox()
            spin_box.setStyleSheet("font-weight: bold; font-size: 18px")
            spin_box.setRange(1, 99)
            spin_box.setValue(self.default_val[i])  # Default value
            self.brightness_inputs.append(spin_box)
            form_layout.addRow(label, spin_box)

        layout.addLayout(form_layout)

        # Button for starting/stopping the application
        self.start_stop_button = QPushButton('Start')
        self.start_stop_button.setStyleSheet(
            "background-color: #4CAF50; color: white; border: none; padding: 10px 20px; font-size: 16px;")
        self.start_stop_button.clicked.connect(self.toggle_start_stop)
        layout.addWidget(self.start_stop_button)

        # Apply dark theme and modern design
        self.apply_dark_theme()

        # Set up the system tray icon
        self.setup_tray_icon()

    # def set_rounded_corners(self, radius):
    #     rect_f = QRectF(self.rect())
    #     path = QPainterPath()
    #     path.addRoundedRect(rect_f, radius, radius)

    #     # Apply a region mask for rounded corners
    #     region = QRegion(path.toFillPolygon().toPolygon())
    #     self.setMask(region)

    #     # Optional: Add a drop shadow effect
    #     shadow = QGraphicsDropShadowEffect(self)
    #     shadow.setBlurRadius(15)
    #     shadow.setXOffset(0)
    #     shadow.setYOffset(0)
    #     shadow.setColor(QColor(0, 0, 0, 180))  # semi-transparent black shadow
    #     self.setGraphicsEffect(shadow)

    def apply_dark_theme(self):
        # Set a dark stylesheet
        dark_stylesheet = """
        QMainWindow {
            background-color: #16161a;
        }
        QLabel {
            color: #efefef;
            font-size: 14px;
        }
        QSpinBox {
            background-color: #373445;
            color: #efefef;
            border: 1px solid #373445;
            border-radius: 5px;
            padding: 5px;
            
        }
        QPushButton {
            background-color: #157518;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #46a949;
        }
        QFormLayout {
            margin: 20px;
        }
        """
        self.setStyleSheet(dark_stylesheet)

    def toggle_start_stop(self):
        global each_brightness, process
        if self.start_stop_button.text() == 'Start':
            process = True
            self.hide()
            self.start_stop_button.setText('Stop')
            self.start_stop_button.setStyleSheet(
                "background-color: #f44336; color: white; border: none; padding: 10px 20px; font-size: 16px;")
            each_brightness = [spin_box.value()
                               for spin_box in self.brightness_inputs]

            # Start the worker thread
            self.worker_thread = BrightnessWorker(
                self.num_desktops, each_brightness)
            self.worker_thread.exit_signal.connect(self.on_worker_exit)
            self.worker_thread.start()

        else:
            self.start_stop_button.setText('Start')
            self.start_stop_button.setStyleSheet(
                "background-color: #4CAF50; color: white; border: none; padding: 10px 20px; font-size: 16px;")
            if self.worker_thread:
                self.worker_thread.exit_app()

    def setup_tray_icon(self):
        tray_icon_path = icon  # icon path

        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "System Tray",
                                 "No system tray found on this system.")
            sys.exit(1)

        self.tray_icon = QSystemTrayIcon(self)

        # Use a default icon if your icon is missing
        if not QIcon(tray_icon_path).isNull():
            self.tray_icon.setIcon(QIcon(tray_icon_path))
        else:
            self.tray_icon.setIcon(
                self.style().standardIcon(QStyle.SP_ComputerIcon))  # type: ignore

        # Add a context menu to the tray icon
        tray_menu = QMenu(self)

        restore_action = QAction('Restore', self)
        restore_action.triggered.connect(self.restore_window)
        tray_menu.addAction(restore_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(qApp.quit)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)

        # Connect the signal for clicking the tray icon
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Show the tray icon
        self.tray_icon.show()

    def closeEvent(self, event):
        if self.worker_thread:
            self.worker_thread.exit_app()  # Stop the worker thread safely
            self.worker_thread.wait()

        with open('./cache.txt', 'w') as file:
            file.write(str(each_brightness))

        QApplication.quit()  # Request the application to exit
        event.accept()  # Let the application close gracefully

    def changeEvent(self, event):
        if event.type() == event.WindowStateChange and self.windowState() & Qt.WindowMinimized:
            # Hide the window and show the tray icon when minimized
            self.hide()
            self.tray_icon.show()
        super().changeEvent(event)

    def show_tray_icon(self):
        self.tray_icon.show()
        self.hide()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.restore_window()

    def restore_window(self):
        self.show()
        self.setWindowState(self.windowState() & ~
                            Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()

    def on_worker_exit(self):
        self.worker_thread = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = BrightnessWindow()
    window.show()

    sys.exit(app.exec_())
