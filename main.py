# coding=utf-8
import sys

from PyQt5.QtWidgets import QApplication

from controladores.Main import Main
from libs.Utiles import initialize_logger, LeerIni


def inicio():
    initialize_logger(LeerIni("iniciosistema"))
    sys.path.insert(0, LeerIni("iniciosistema"))
    # logging.basicConfig(filename=join(LeerIni("iniciosistema"), 'errors.log'), level=logging.DEBUG,
    #                     format='%(asctime)s %(message)s',
    #                     datefmt='%m/%d/%Y %I:%M:%S %p')
    args = []
    #args = ['', '-style', 'Cleanlooks']
    app = QApplication(args)
    ex = Main()
    ex.run()
    sys.exit(app.exec_())

if __name__ == "__main__":
    inicio()
