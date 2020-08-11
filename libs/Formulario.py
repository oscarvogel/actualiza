# -*- coding: utf-8 -*-
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QHBoxLayout, QVBoxLayout

from libs.Botones import Boton
from libs.EntradaTexto import EntradaTexto
from libs.Etiquetas import Etiqueta
from libs.Utiles import icono_sistema


class Formulario(QDialog):

    lblStatusBar = None

    controles = {}

    def __init__(self, parent=None):
        QDialog.__init__(self, parent=None)
        self.Exception = self.Traceback = ""
        self.LanzarExcepciones = False
        self.setWindowIcon(icono_sistema())
        self.setWindowModality(Qt.ApplicationModal)

    def Cerrar(self):
        self.close()

    def exec_(self):
        self.Center()
        QDialog.exec_(self)

    def Center(self):
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def resizeEvent(self, QResizeEvent):
        self.Center()
        QDialog.resizeEvent(self, QResizeEvent)

    def addStatusBar(self, layout=None):
        if layout:
            self.lblStatusBar = Etiqueta()
            layout.addWidget(self.lblStatusBar)

    def setTextStatusBar(self, text=''):
        if self.lblStatusBar:
            self.lblStatusBar.setText(text)

    def ArmaEntrada(self, nombre="", boxlayout=None, texto='', *args, **kwargs):
        if not boxlayout:
            boxlayout = QHBoxLayout()
            lAgrega = True
        else:
            lAgrega = False

        if not texto:
            texto = nombre.capitalize()

        labelNombre = Etiqueta(texto=texto)
        labelNombre.setObjectName("labelNombre")
        boxlayout.addWidget(labelNombre)

        if 'control' in kwargs:
            lineEditNombre = kwargs['control']
        else:
            lineEditNombre = EntradaTexto()

        if 'relleno' in kwargs:
            lineEditNombre.relleno = kwargs['relleno']

        lineEditNombre.setObjectName(nombre)
        boxlayout.addWidget(lineEditNombre)
        if 'enabled' in kwargs:
            lineEditNombre.setEnabled(kwargs['enabled'])

        self.controles[nombre] = lineEditNombre

        if lAgrega:
            self.verticalLayoutDatos.addLayout(boxlayout)
        return boxlayout

    def setupUi(self, Form):
        pass

    def ConectarWidgets(self):
        pass

class Menu(Formulario):

    opciones = []
    nRetorno = 0
    parent = None
    botones = {}
    valoresRetorno = []
    valorSeleccionado = None

    def __init__(self, *args, **kwargs):
        Formulario.__init__(self)

        self.opciones = kwargs['opciones']
        if 'valores' in kwargs:
            self.valoresRetorno = kwargs['valores']

        self.setupUi(self)
        self.Center()

    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Opciones de menu")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        i = 0
        for x in self.opciones:
            self.botones[str(i)] = Boton(Dialog, texto=x)
            self.botones[str(i)].setObjectName(x)
            self.botones[str(i)].clicked.connect(partial(self.onClicked, i))
            self.botones[str(i)].setMinimumHeight(50)
            self.botones[str(i)].setMinimumWidth(200)
            self.verticalLayout.addWidget(self.botones[str(i)])
            i += 1
        print(self.botones)

    def onClicked(self, n):
        self.nRetorno = n
        if self.valoresRetorno:
            self.valorSeleccionado = self.valoresRetorno[n]
        self.Cerrar()
