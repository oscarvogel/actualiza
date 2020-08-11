# coding=utf-8
import sys

from PyQt5.QtWidgets import QMessageBox


def showAlert(titulo, mensaje):

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(mensaje)
    msg.setWindowTitle(titulo)
    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec_()

    return retval

def showConfirmation(titulo, mensaje):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText(mensaje)
    msg.setWindowTitle(titulo)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    retval = msg.exec_()

    return retval

def showdialog():
    retval = showConfirmation("Sistema", "Desea imprimir el presupuesto?")
    if retval == QMessageBox.Ok:
        print("Valor de retorno {}".format(retval))

