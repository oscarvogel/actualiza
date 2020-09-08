# coding=utf-8
import logging
import os
import shutil
import subprocess
import tempfile

from os.path import join

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from controladores.ControladorBase import ControladorBase
from libs.Formulario import Menu
from libs.Utiles import getFileProperties, inicializar_y_capturar_excepciones
from vistas.Main import MainView


class Main(ControladorBase):

    exeorigen = ""
    exedestino = ""
    carpetaorigen = ""
    carpetadestino = ""
    archivoini = ""
    exclude = []

    def __init__(self):
        super().__init__()
        self.view = MainView()
        self.conectarWidgets()

    def conectarWidgets(self):
        self.view.btnSalir.clicked.connect(self.SalirSistema)
        self.view.btnContable.clicked.connect(self.onClickBtnContable)
        self.view.btnHorarios.clicked.connect(self.onClickBtnHorarios)
        self.view.btnAberturas.clicked.connect(lambda: self.onClickBtn(self.view.btnAberturas))
        self.view.btnGraficos.clicked.connect(lambda : self.onClickBtn(self.view.btnGraficos))
        self.view.btnSistemaFasa.clicked.connect(lambda : self.onClickBtn(self.view.btnSistemaFasa))

    def SalirSistema(self):
        QApplication.exit(1)

    @inicializar_y_capturar_excepciones
    def onClickBtn(self, boton, *args, **kwargs):
        self.exeorigen = boton.exeorigen
        self.exedestino = boton.exedestino
        self.carpetaorigen = boton.carpetaorigen
        self.carpetadestino = boton.carpetadestino
        self.archivoini = boton.archivoini
        self.exclude = boton.exclude

        if self.Verifica():
            self.Copia()
        else:
            # os.system(self.exedestino)
            self.Ejecutar()

    @inicializar_y_capturar_excepciones
    def onClickBtnContable(self, *args, **kwargs):
        boton = self.view.btnContable
        self.exeorigen = boton.exeorigen
        self.exedestino = boton.exedestino
        self.carpetaorigen = boton.carpetaorigen
        self.carpetadestino = boton.carpetadestino

        if self.Verifica():
            self.Copia()
        else:
            menu = Menu(opciones=['FASA', 'Steffen Hnos', 'Transporte'],
                        valores=['contable.ini', 'contablesteffen.ini', 'contabletransporte.ini'])
            menu.exec_()
            self.archivoini = menu.valorSeleccionado
            self.Ejecutar()

    @inicializar_y_capturar_excepciones
    def onClickBtnHorarios(self, *args, **kwargs):
        boton = self.view.btnHorarios
        self.exeorigen = boton.exeorigen
        self.exedestino = boton.exedestino
        self.carpetaorigen = boton.carpetaorigen
        self.carpetadestino = boton.carpetadestino

        if self.Verifica():
            # self.Borra()
            self.Copia()
        else:
            menu = Menu(opciones=['FASA', 'Steffen Hnos', 'Transporte'],
                        valores=['fasa.ini', 'steffen.ini', 'transporte.ini'])
            menu.exec_()
            self.archivoini = menu.valorSeleccionado
            self.Ejecutar()

    #verifica que exista la carpeta y el exe destino, si no existe devuelve true para que se pueda copiar
    def Verifica(self):

        proporigen = getFileProperties(join(self.carpetaorigen, self.exeorigen))
        propdestino = getFileProperties(join(self.carpetadestino, self.exedestino))

        if not os.path.isdir(self.carpetadestino):
            os.mkdir(self.carpetadestino)

        if not propdestino['StringFileInfo']:
            return True

        self.versionlocal = propdestino['StringFileInfo']['FileVersion']
        self.versionservidor = proporigen['StringFileInfo']['FileVersion']

        if self.versionservidor != self.versionlocal:
            return True
        else:
            # self.Ejecutar()
            return False

    def Borra(self):
        shutil.rmtree(self.carpetadestino)

    # @inicializar_y_capturar_excepciones
    def Copia(self, *args, **kwargs):
        self.view.avance.setVisible(True)
        self.view.lblAvance.setVisible(True)
        self.view.lblAvance.setText("Actualizando sistema aguarde...")
        self.myLongTask = TaskThread()
        self.myLongTask.controlador = self
        self.myLongTask.carpetadestino = self.carpetadestino
        self.myLongTask.carpetaorigen = self.carpetaorigen
        self.myLongTask.archivoini = self.archivoini
        self.myLongTask.exclude = self.exclude
        self.myLongTask.taskFinished.connect(self.onFinished)
        self.view.avance.setRange(0, 0)
        QApplication.processEvents()
        self.myLongTask.start()

    def onFinished(self):
        self.view.avance.setVisible(False)
        self.view.lblAvance.setVisible(False)
        self.Ejecutar()

    def Ejecutar(self):
        print(self.carpetadestino, self.exedestino, self.carpetadestino, self.archivoini)
        # archivo_bat = tempfile.TemporaryFile().name + '.bat'
        # archivo_ini = f"{join(self.carpetadestino, self.archivoini)}"
        # f = open(archivo_bat, "w")
        # f.write(f"{join(self.carpetadestino, self.exedestino)} -i {self.carpetadestino} -a {archivo_ini}")
        # f.close()
        os.chdir(self.carpetadestino)
        # call([join(self.carpetadestino, self.exedestino)])
        subprocess.Popen([join(self.carpetadestino, self.exedestino),
                          "-i", self.carpetadestino, "-a", self.archivoini],)
        # subprocess.run(archivo_bat)


class TaskThread(QtCore.QThread):

    taskFinished = QtCore.pyqtSignal()
    carpetaorigen = ""
    carpetadestino = ""
    archivoini = ""
    controlador = None
    exclude = []

    def run(self):
        self.copia(self.carpetaorigen, self.carpetadestino)
        self.taskFinished.emit()

    def copia(self, carpetaorigen, carpetadestino):
        # shutil.rmtree(carpetadestino)
        # os.mkdir(carpetadestino)
        source = os.listdir(carpetaorigen)
        for file in source:
            self.controlador.view.lblAvance.setText(f"Copiando {carpetaorigen}\{file} a {carpetadestino}"[:80])
            if file not in self.exclude:
                try:
                    if os.path.isfile(join(carpetaorigen, file)):
                        if not file.endswith(".ini"):
                            try:
                                shutil.copy(join(carpetaorigen, file), join(carpetadestino, file))
                            except:
                                pass
                        else:
                            print("Copiando archivo ini de {} a {}".format(
                                join(carpetaorigen, file), join(carpetadestino, file)
                            ))
                            if not os.path.isfile(join(carpetadestino, file)):
                                shutil.copy(join(carpetaorigen, file), join(carpetadestino, file))
                    else:
                        if not os.path.exists(join(carpetadestino, file)):
                            os.mkdir(join(carpetadestino, file))
                        self.copia(join(carpetaorigen, file), join(carpetadestino, file))
                except:
                    logging.error(f"Error al copiar {carpetaorigen}{file} a {carpetadestino}")
                    print(f"Error al copiar {carpetaorigen}{file} a {carpetadestino}")

