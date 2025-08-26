import os
import subprocess
import pygame
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

        self.btn_launch_lidar = QPushButton("Visualiser le LIDAR")
        self.btn_launch_lidar.setIcon(QIcon.fromTheme("view-refresh"))
        self.btn_launch_lidar.setEnabled(False)
        self.btn_launch_lidar.setToolTip("Assurez-vous que la HAL est active avant de lancer le LIDAR.")

        self.btn_launch_hal = QPushButton("Lancer la HAL")
        self.btn_launch_hal.setIcon(QIcon.fromTheme("system-run"))
        self.btn_launch_hal.setEnabled(False)

        self.btn_teleop = QPushButton("Lancer la téléopération (joystick)")
        self.btn_teleop.setIcon(QIcon.fromTheme("input-gaming"))
        self.btn_teleop.setEnabled(False)
        self.btn_teleop.setToolTip("Assurez-vous que la HAL est active avant de lancer la téléopération.")

        # Layout
        usb_layout = QVBoxLayout()
        usb_layout.addWidget(QLabel("Statut des USB:"))
        usb_layout.addWidget(self.usb_vesc_status)
        usb_layout.addWidget(self.usb_lidar_status)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.btn_check_usb)
        buttons_layout.addWidget(self.btn_launch_lidar)
        buttons_layout.addWidget(self.btn_launch_hal)
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

        self.btn_check_usb.clicked.connect(self.check_usb)
        self.btn_launch_lidar.clicked.connect(self.launch_lidar)
        self.btn_launch_hal.clicked.connect(self.launch_hal)
        self.btn_teleop.clicked.connect(self.launch_teleop)

        self.lidar_process = None
        self.hal_process = None
        self.teleop_process = None

    def kill_processes_by_name(self, pattern):
        """Tue tous les processus dont la commande contient `pattern`."""
        try:
            ps_output = subprocess.check_output(["ps", "ax"], universal_newlines=True)
            lines = ps_output.splitlines()

            pids_to_kill = []
            for line in lines:
                if pattern in line:
                    pid = int(line.split()[0])
                    pids_to_kill.append(pid)

            for pid in pids_to_kill:
                try:
                    os.kill(pid, 9)  # SIGKILL
                    self.logs.append(f"Processus {pid} tué.")
                except ProcessLookupError:
                    pass

        except subprocess.CalledProcessError:
            print(f"Aucun processus trouvé pour le motif : {pattern}")

    def kill_processes(self):
        """Tue tous les processus ROS liés à l'application."""
        self.kill_processes_by_name("lidar")
        self.kill_processes_by_name("zuuu")
        self.kill_processes_by_name("teleop_joy")

        self.lidar_process = None
        self.hal_process = None
        self.teleop_process = None

    def closeEvent(self, event):
        self.kill_processes()
        event.accept()

    @Slot()
    def check_usb(self):
        wheels_ok = os.path.exists("/dev/vesc_wheels")
        lidar_ok = os.path.exists("/dev/rplidar_s2")

        self.usb_vesc_status.setText("USB VESC: OK" if wheels_ok else "USB VESC: Erreur - non détecté")
        self.usb_vesc_status.setProperty("ok", wheels_ok)

        self.usb_lidar_status.setText("USB LIDAR: OK" if lidar_ok else "USB LIDAR: Erreur - non détecté")
        self.usb_lidar_status.setProperty("ok", lidar_ok)

        if wheels_ok and lidar_ok:
            self.btn_launch_hal.setEnabled(True)
        else:
            self.btn_launch_hal.setEnabled(False)

        self.usb_vesc_status.style().unpolish(self.usb_vesc_status)
        self.usb_vesc_status.style().polish(self.usb_vesc_status)

        self.usb_lidar_status.style().unpolish(self.usb_lidar_status)
        self.usb_lidar_status.style().polish(self.usb_lidar_status) 

    @Slot()
    def launch_lidar(self):
        if self.hal_process is None or self.hal_process.state() != QProcess.Running:
            print("Erreur: Le launch principal n'est pas actif.")
            return
        self.lidar_process = QProcess()
        self.lidar_process.readyReadStandardOutput.connect(
            lambda: self.logs.append(self.lidar_process.readAllStandardOutput().data().decode())
        )
        self.lidar_process.start("ros2", ["launch", "zuuu_description", "rviz_lidar_only.launch.py", "use_sim_time:=False"])
        self.btn_launch_lidar.setToolTip("Le LIDAR est en cours d'exécution.")
        self.btn_launch_lidar.setEnabled(False)

    @Slot()
    def launch_hal(self):
        if self.lidar_process is not None:
            print("Erreur: Le launch LIDAR est déjà en cours.")
            return
        self.hal_process = QProcess()
        self.hal_process.readyReadStandardOutput.connect(
            lambda: self.logs.append(self.hal_process.readAllStandardOutput().data().decode())
        )
        self.hal_process.start("ros2", ["launch", "zuuu_hal", "hal.launch.py"])
        self.btn_launch_lidar.setEnabled(True)
        self.btn_launch_hal.setEnabled(False)
        self.btn_teleop.setEnabled(True)

    @Slot()
    def launch_teleop(self):
        if self.hal_process is None or self.hal_process.state() != QProcess.Running:
            print("Erreur: Le launch principal n'est pas actif.")
            return
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            self.logs.append("Erreur: Aucun joystick détecté.")
            self.btn_teleop.setToolTip("Aucun joystick détecté. Veuillez connecter un joystick.")
            pygame.joystick.quit()
            return

        self.logs.append("Lancement de la téléopération...")
        self.teleop_process = QProcess()
        self.teleop_process.start("ros2", ["run", "zuuu_hal", "teleop_joy"])
        self.logs.append("Téléopération lancée.")
        self.btn_teleop.setToolTip("La téléopération est en cours d'exécution.")
        self.btn_teleop.setEnabled(False)

if __name__ == "__main__":
    app = QApplication([])
    window = TestWindow()
    window.show()
    app.exec()
   
