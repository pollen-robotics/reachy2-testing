import os
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton,
    QLabel, QTextEdit, QWidget, QHBoxLayout, QGroupBox
)
from PySide6.QtCore import QProcess, Slot, Qt
from PySide6.QtGui import QIcon, QPixmap


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Production - Base Mobile")
        self.setGeometry(100, 100, 900, 700)

        # Styles
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                border: 2px solid #2c3e50;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
                background-color: #ecf0f1;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QTextEdit {
                background-color: #2c3e50;
                color: white;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
            }
            QLabel#status {
                font-size: 16px;
                color: #e74c3c;
            }
            QLabel#status[ok="true"] {
                color: #27ae60;
            }
        """)

        # Widgets
        self.usb_vesc_status = QLabel("USB VESC: Non vérifié")
        self.usb_vesc_status.setObjectName("status")
        self.usb_vesc_status.setProperty("ok", False)

        self.usb_lidar_status = QLabel("USB LIDAR: Non vérifié")
        self.usb_lidar_status.setObjectName("status")
        self.usb_lidar_status.setProperty("ok", False)

        self.logs = QTextEdit(readOnly=True)

        self.btn_check_usb = QPushButton("Vérifier les USB")
        self.btn_check_usb.setIcon(QIcon.fromTheme("dialog-ok"))

        self.btn_launch_lidar = QPushButton("Lancer le LIDAR")
        self.btn_launch_lidar.setIcon(QIcon.fromTheme("view-refresh"))
        self.btn_launch_lidar.setEnabled(False)

        self.btn_launch_main = QPushButton("Lancer le launch principal")
        self.btn_launch_main.setIcon(QIcon.fromTheme("system-run"))
        self.btn_launch_main.setEnabled(False)

        self.btn_teleop = QPushButton("Lancer la téléopération (joystick)")
        self.btn_teleop.setIcon(QIcon.fromTheme("input-gaming"))
        self.btn_teleop.setEnabled(False)

        # Layout
        usb_layout = QVBoxLayout()
        usb_layout.addWidget(QLabel("Statut des USB:"))
        usb_layout.addWidget(self.usb_vesc_status)
        usb_layout.addWidget(self.usb_lidar_status)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.btn_check_usb)
        buttons_layout.addWidget(self.btn_launch_lidar)
        buttons_layout.addWidget(self.btn_launch_main)
        buttons_layout.addWidget(self.btn_teleop)

        main_layout = QVBoxLayout()
        main_layout.addLayout(usb_layout)
        main_layout.addLayout(buttons_layout)

        logs_group = QGroupBox("Logs")
        logs_layout = QVBoxLayout()
        logs_layout.addWidget(self.logs)
        logs_group.setLayout(logs_layout)
        main_layout.addWidget(logs_group)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connexions
        self.btn_check_usb.clicked.connect(self.check_usb)
        self.btn_launch_lidar.clicked.connect(self.launch_lidar)
        self.btn_launch_main.clicked.connect(self.launch_main)
        self.btn_teleop.clicked.connect(self.launch_teleop)

        # Processus ROS2
        self.lidar_process = None
        self.main_process = None

    @Slot()
    def check_usb(self):
        wheels_ok = os.path.exists("/dev/vesc_wheels")
        lidar_ok = os.path.exists("/dev/rplidar_s2")

        self.usb_vesc_status.setText("USB VESC: OK" if wheels_ok else "USB VESC: Erreur")
        self.usb_vesc_status.setProperty("ok", wheels_ok)

        self.usb_lidar_status.setText("USB LIDAR: OK" if lidar_ok else "USB LIDAR: Erreur")
        self.usb_lidar_status.setProperty("ok", lidar_ok)

        if wheels_ok and lidar_ok:
            self.btn_launch_lidar.setEnabled(True)
            self.btn_launch_main.setEnabled(True)
        else:
            self.btn_launch_lidar.setEnabled(False)
            self.btn_launch_main.setEnabled(False)

        self.usb_vesc_status.style().unpolish(self.usb_vesc_status)
        self.usb_vesc_status.style().polish(self.usb_vesc_status)

        self.usb_lidar_status.style().unpolish(self.usb_lidar_status)
        self.usb_lidar_status.style().polish(self.usb_lidar_status) 

    @Slot()
    def launch_lidar(self):
        if self.main_process is not None:
            self.logs.append("Erreur: Le launch principal est déjà en cours.")
            return
        self.lidar_process = QProcess()
        self.lidar_process.readyReadStandardOutput.connect(
            lambda: self.logs.append(self.lidar_process.readAllStandardOutput().data().decode())
        )
        self.lidar_process.start("ros2", ["launch", "zuuu_description", "rviz_lidar_only.launch.py", "use_sim_time:=False"])
        self.btn_launch_lidar.setEnabled(False)
        self.btn_launch_main.setEnabled(False)

    @Slot()
    def launch_main(self):
        if self.lidar_process is not None:
            self.logs.append("Erreur: Le launch LIDAR est déjà en cours.")
            return
        self.main_process = QProcess()
        self.main_process.readyReadStandardOutput.connect(
            lambda: self.logs.append(self.main_process.readAllStandardOutput().data().decode())
        )
        self.main_process.start("ros2", ["launch", "ton_package", "main.launch.py"])
        self.btn_launch_lidar.setEnabled(False)
        self.btn_launch_main.setEnabled(False)
        self.btn_teleop.setEnabled(True)

    @Slot()
    def launch_teleop(self):
        if self.main_process is None or self.main_process.state() != QProcess.Running:
            self.logs.append("Erreur: Le launch principal n'est pas actif.")
            return
        teleop_process = QProcess()
        teleop_process.start("ros2", ["run", "ton_package", "teleop_node"])

if __name__ == "__main__":
    app = QApplication([])
    window = TestWindow()
    window.show()
    app.exec()
   
