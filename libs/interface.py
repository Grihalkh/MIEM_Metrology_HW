# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QDesktopWidget,
                             QPushButton, QFileDialog, QMessageBox,
                             QTextEdit, QLabel, QTableWidget)
from PyQt5.QtGui import QIcon, QPalette, QColor

import libs.storage as strg
import libs.stats as stats

import os


class Ui(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 700, 400)

        geom = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        geom.moveCenter(cp)
        self.move(geom.topLeft())

        self.setWindowTitle('Отбор результатов по критерию Шарлье')

        icon = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.setWindowIcon(QIcon(icon + '/graphics/icon.png'))

        loadFromTextLbl = QLabel('Или же впишите путь вручную', self)

        loadFromTextEdit = QTextEdit(None, self)

        loadedLbl = QLabel('Данные не загружены', self)
        self.changeLabelColor(loadedLbl, 'red')

        loadFileBtn = QPushButton('Загрузить данные из файла', self)
        loadFileBtn.clicked.connect(lambda: self.loadFileBtnPush(loadFromTextEdit, loadedLbl))

        loadFromTextBtn = QPushButton('Загрузить', self)
        loadFromTextBtn.clicked.connect(lambda: self.loadFromTextBtnPush(loadFromTextEdit, loadedLbl))

        inputManLbl = QLabel('Можете вписать данные вручную', self)

        inputManEdit = QTextEdit(None, self)

        inputManBtn = QPushButton('Загрузить', self)
        inputManBtn.clicked.connect(lambda: self.inputManBtnPush(inputManEdit, loadedLbl))

        interLbl = QLabel('Промежуточные вычисления', self)

        interEdit = QTextEdit(None, self)
        interEdit.setReadOnly(True)

        clearedLbl = QLabel('Данные без промахов', self)

        clearedEdit = QTextEdit(None, self)
        clearedEdit.setReadOnly(True)

        clearedBtn = QPushButton('Экспортировать в файл', self)
        clearedBtn.clicked.connect(self.clearedBtnPush)

        mistakesLbl = QLabel('Промахи', self)

        mistakesEdit = QTextEdit(None, self)
        mistakesEdit.setReadOnly(True)

        mistakesBtn = QPushButton('Экспортировать в файл', self)
        mistakesBtn.clicked.connect(self.mistakesBtnPush)

        checkCriteriaBtn = QPushButton('Проверить критерий', self)
        checkCriteriaBtn.clicked.connect(lambda: self.checkCriteriaBtnPush(clearedEdit, mistakesEdit, interEdit))

        flushBtn = QPushButton('Сбросить', self)
        flushBtn.clicked.connect(lambda: self.flushBtnPush(loadedLbl, clearedEdit, mistakesEdit, interEdit))

        mainV = QVBoxLayout()

        lines = []
        lines.append(QHBoxLayout())
        lines[0].addWidget(loadFileBtn)
        lines[0].addWidget(loadFromTextLbl)
        lines[0].addWidget(loadFromTextEdit)
        lines[0].addWidget(loadFromTextBtn)

        lines.append(QHBoxLayout())
        lines[1].addWidget(inputManLbl)
        lines[1].addWidget(inputManEdit)
        lines[1].addWidget(inputManBtn)

        lines.append(QHBoxLayout())
        lines[2].addWidget(loadedLbl)
        lines[2].addWidget(flushBtn)

        lines.append(QHBoxLayout())
        lines[3].addWidget(QLabel('\n', self))

        lines.append(QHBoxLayout())
        lines[4].addWidget(checkCriteriaBtn)

        lines.append(QHBoxLayout())
        lines[5].addWidget(interLbl)
        lines[5].addWidget(interEdit)

        lines.append(QHBoxLayout())
        lines[6].addWidget(clearedLbl)
        lines[6].addWidget(clearedBtn)

        lines.append(QHBoxLayout())
        lines[7].addWidget(clearedEdit)

        lines.append(QHBoxLayout())
        lines[8].addWidget(mistakesLbl)
        lines[8].addWidget(mistakesBtn)

        lines.append(QHBoxLayout())
        lines[9].addWidget(mistakesEdit)

        lines.append(QHBoxLayout())
        lines[10].addWidget(QLabel('\n', self))

        for line in lines:
            mainV.addLayout(line)

        self.setLayout(mainV)
        self.show()

    def changeLabelColor(self, label, color):
        labelPal = label.palette()
        labelPal.setColor(QPalette.WindowText, QColor(color))
        label.setPalette(labelPal)

    def loadFileBtnPush(self, textEdit, loadedLbl):
        fname = QFileDialog.getOpenFileName(self, 'Открыть файл с данными', None, '*.txt')[0]

        textEdit.setText(fname)
        self.loadFromFile(fname, loadedLbl)

    def loadFromTextBtnPush(self, textEdit, loadedLbl):
        self.loadFromFile(textEdit.toPlainText(), loadedLbl)

    def loadFromFile(self, fname, loadedLbl):
        try:
            strg.data = []
            with open(fname, 'r') as f:
                data = ''.join(f.readlines())
                data = data.split()
                for i in data:
                    strg.data.append(float(i.replace(',', '.')))
            self.changeLabelColor(loadedLbl, 'green')
            loadedLbl.setText('Данные загружены')
        except:
            QMessageBox.warning(self, 'Ошибка', 'Произошла ошибка при чтении файла. Возможно, данные в нем некорректны')
            return
        self.checkLength(loadedLbl)

    def inputManBtnPush(self, inputManEdit, loadedLbl):
        try:
            written = inputManEdit.toPlainText().split()
            for i in written:
                strg.data.append(float(i.replace(',', '.')))
            self.changeLabelColor(loadedLbl, 'green')
            loadedLbl.setText('Данные загружены')
        except:
            QMessageBox.warning(self, 'Ошибка', 'В введенных данных ошибка.')
            return
        self.checkLength(loadedLbl)

    def flushBtnPush(self, loadedLbl, clearedEdit, mistakesEdit, interEdit):
        strg.data = []
        clearedEdit.setText('')
        mistakesEdit.setText('')
        interEdit.setText('')
        self.changeLabelColor(loadedLbl, 'red')
        loadedLbl.setText('Данные не загружены')

    def checkLength(self, loadedLbl):
        if len(strg.data) == 0:
            QMessageBox.warning(self, 'Ошибка', 'Введенные данные пусты')
            self.changeLabelColor(loadedLbl, 'red')
            loadedLbl.setText('Данные не загружены')
            strg.data = []
            return
        if len(strg.data) < 5:
            QMessageBox.warning(self, 'Ошибка', 'Данных слишком мало. Нужно как минимум 5 измерений')
            self.changeLabelColor(loadedLbl, 'red')
            loadedLbl.setText('Данные не загружены')
            strg.data = []
            return
        if len(strg.data) > 100:
            QMessageBox.warning(self, 'Ошибка', 'Количество измерений не может быть больше 100')
            self.changeLabelColor(loadedLbl, 'red')
            loadedLbl.setText('Данные не загружены')
            strg.data = []
            return

    def checkCriteriaBtnPush(self, clearedEdit, mistakesEdit, interEdit):
        if len(strg.data) == 0:
            QMessageBox.warning(self, 'Ошибка', 'Данные не загружены')
            return
        stats.process()
        clearedEdit.setText(strg.str_cleared_data)
        mistakesEdit.setText(strg.str_mistakes)
        interEdit.setText(strg.inter)

    def clearedBtnPush(self):
        if len(strg.str_cleared_data) == 0:
            QMessageBox.warning(self, 'Ошибка', 'Данные не обработаны')
            return
        self.exportData(strg.str_cleared_data)

    def mistakesBtnPush(self):
        if len(strg.str_mistakes) == 0:
            QMessageBox.warning(self, 'Ошибка', 'Данные не обработаны')
            return
        self.exportData(strg.str_mistakes)

    def exportData(self, data):
        fname = QFileDialog.getOpenFileName(self, 'Открыть файл для данных', None, '*.txt')[0]
        try:
            with open(fname, 'w') as f:
                f.write(data)
        except:
            QMessageBox.warning(self, 'Ошибка', 'Произошла ошибка при записи. Повторите запрос')
            return