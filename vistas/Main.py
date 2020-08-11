# coding=utf-8
from os.path import join

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QMainWindow, QWidget

from libs.BarraProgreso import Avance
from libs.Botones import BotonMain, BotonCopiaExe
from libs.Etiquetas import EtiquetaTitulo, Etiqueta
from libs.Utiles import LeerIni, DeCodifica, imagen, icono_sistema


class MainView(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()

    def initUi(self):
        self.setWindowIcon(icono_sistema())
        self.setGeometry(150, 150, 500, 150)
        self.setWindowTitle('Aplicaciones')
        layoutPpal = QVBoxLayout(self)
        self.lblTitulo = EtiquetaTitulo(texto="{}-{}".format(
            LeerIni(clave="nombre_sistema"), DeCodifica(LeerIni(clave='EMPRESA', key='FACTURA'))))
        layoutPpal.addWidget(self.lblTitulo)

        self.lblAvance = Etiqueta()
        self.lblAvance.setVisible(False)
        layoutPpal.addWidget(self.lblAvance)
        self.avance = Avance()
        self.avance.setVisible(False)
        layoutPpal.addWidget(self.avance)

        self.layoutBotones = QHBoxLayout()

        self.btnContable = BotonCopiaExe(texto='&Contabilidad', imagen=imagen('iconfinder_calculator-pencil_532650.png'))
        self.btnContable.exeorigen = "contable.exe"
        self.btnContable.exedestino = "contable.exe"
        self.btnContable.carpetadestino = join("c:\\", "contable")
        self.btnContable.carpetaorigen = join("z:\\", "fasapython", "contable")
        self.btnContable.archivoini = "contable.ini"
        self.layoutBotones.addWidget(self.btnContable)

        self.btnSistemaFasa = BotonCopiaExe(texto='&FASA', imagen=imagen('logo_fasa.png'))
        self.btnSistemaFasa.exeorigen = "main.exe"
        self.btnSistemaFasa.exedestino = "main.exe"
        self.btnSistemaFasa.carpetadestino = join("c:\\", "fasa")
        self.btnSistemaFasa.carpetaorigen = join("z:\\", "fasapython", "sistema")
        self.btnSistemaFasa.archivoini = "fasa.ini"
        self.layoutBotones.addWidget(self.btnSistemaFasa)

        self.btnAberturas = BotonCopiaExe(texto='&Aberturas', imagen=imagen('aberturas.png'))
        self.btnAberturas.exeorigen = "aberturas.exe"
        self.btnAberturas.exedestino = "aberturas.exe"
        self.btnAberturas.carpetadestino = join("c:\\", "aberturas")
        self.btnAberturas.carpetaorigen = join("z:\\", "steffenpython", "aberturas")
        self.btnAberturas.archivoini = "aberturas.ini"
        self.layoutBotones.addWidget(self.btnAberturas)

        self.btnTransporte = BotonCopiaExe(texto='&Transporte', imagen=imagen('truck.png'))
        self.btnTransporte.exeorigen = "sistema.exe"
        self.btnTransporte.exedestino = "sistema.exe"
        self.btnTransporte.carpetadestino = join("c:\\", "transporte")
        self.btnTransporte.carpetaorigen = join("z:\\", "transpython", "sistema")
        self.btnTransporte.archivoini = "transporte.ini"
        self.layoutBotones.addWidget(self.btnTransporte)

        self.btnGraficos = BotonCopiaExe(texto='&Graficos', imagen=imagen('icon_chart.png'))
        self.btnGraficos.exeorigen = "main.exe"
        self.btnGraficos.exedestino = "main.exe"
        self.btnGraficos.carpetadestino = join("c:\\", "graficos")
        self.btnGraficos.carpetaorigen = join("z:\\", "fasapython", "graficos")
        self.btnGraficos.archivoini = "sistema.ini"
        self.layoutBotones.addWidget(self.btnGraficos)

        self.btnHorarios = BotonCopiaExe(texto="Horario", imagen=imagen('iconfinder_calendar-clock_299096.png'))
        self.btnHorarios.exeorigen = "horas.exe"
        self.btnHorarios.exedestino = "horas.exe"
        self.btnHorarios.carpetadestino = join("c:\\", "horarios")
        self.btnHorarios.carpetaorigen = join("z:\\", "fasapython", "horarios")
        self.btnHorarios.archivoini = "fasa.ini"
        self.layoutBotones.addWidget(self.btnHorarios)

        self.btnSalir = BotonMain(texto='&Salir', imagen=imagen('if_Log Out_27856.png'))
        self.layoutBotones.addWidget(self.btnSalir)

        layoutPpal.addLayout(self.layoutBotones)