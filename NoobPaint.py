# By Anna Zazulya
# Dec 2018
# made with love
# 2nd year YandexLiceum

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,\
    QWidget, QSlider, QAction

from PyQt5.QtGui import QPen, QIcon, QImage, QPainter
from PyQt5.QtCore import QPoint, Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(500, 500, 900, 700)
        self.setWindowTitle('NoobPaint')
        self.show()

        mainMenu = self.menuBar() #Создаю меню
        fileMenu = mainMenu.addMenu(" File")
        brushSizeMenu = mainMenu.addMenu(" Brush Size")
        brushColorMenu = mainMenu.addMenu(" Brush Colour")
        EraserMenu = mainMenu.addMenu(" Eraser")
        shapeOption = mainMenu.addMenu(" Shape")
        penOption = mainMenu.addMenu(" Pen")


        # Стили кистей

        flatshape = QAction("Flat", self)
        shapeOption.addAction(flatshape)
        flatshape.triggered.connect(self.flatCap)

        squareshape = QAction("Square", self)
        shapeOption.addAction(squareshape)
        squareshape.triggered.connect(self.squareCap)

        roundshape = QAction("Round", self)
        shapeOption.addAction(roundshape)
        roundshape.triggered.connect(self.roundCap)


        #Стили линий

        solidLine = QAction(QIcon("./icons/qpen-solid"), "Solid Line", self)
        penOption.addAction(solidLine)
        solidLine.triggered.connect(self.solidLine)

        dashLine = QAction(QIcon("./icons/qpen-dash"), "Dash Line", self)
        penOption.addAction(dashLine)
        dashLine.triggered.connect(self.dashLine)

        dotLine = QAction(QIcon("./icons/qpen-dot"), "Dot Line", self)
        penOption.addAction(dotLine)
        dotLine.triggered.connect(self.dotLine)

        dashDotLine = QAction(QIcon("./icons/qpen-dashdot"), "Dash Dot Line", self)
        penOption.addAction(dashDotLine)
        dashDotLine.triggered.connect(self.dashDotLine)

        dashDotDotLine = QAction(QIcon("./icons/qpen-dashdotdot"), "Dash Dot Dot Line", self)
        penOption.addAction(dashDotDotLine)
        dashDotDotLine.triggered.connect(self.dashDotDotLine)


        # Сохранение

        saveAction = QAction(QIcon("./icons/save.png"), "Save", self)
        saveAction.setShortcut("Ctrl+S") # быстрая клавиша
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)  # вызов меню Сохранить


        # Очистка

        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear) #Заливка белым


        # Размеры кистей

        threepxAction = QAction(QIcon("./icons/threepx.png"), "3px", self)
        brushSizeMenu.addAction(threepxAction)
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/fivepx.png"), "5px", self)
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/sevenpx.png"), "7px", self)
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/ninepx.png"), "9px", self)
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)


        # Цвета кистей

        blackAction = QAction(QIcon("./icons/black.png"), "Black", self)
        brushColorMenu.addAction(blackAction)
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon("./icons/red.png"), "Red", self)
        brushColorMenu.addAction(redAction)
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon("./icons/green.png"), "Green", self)
        brushColorMenu.addAction(greenAction)
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("./icons/yellow.png"), "Yellow", self)
        brushColorMenu.addAction(yellowAction)
        yellowAction.triggered.connect(self.yellow)

        blueAction = QAction(QIcon("./icons/blue.png"), "Blue", self)
        brushColorMenu.addAction(blueAction)
        blueAction.triggered.connect(self.blue)

        whiteAction = QAction(QIcon("./icons/white.png"), "Eraser", self) # Ластик
        EraserMenu.addAction(whiteAction)
        whiteAction.triggered.connect(self.white)


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        # Настройки картинки

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)


        # Нрастройки начальныных параметров инструментов

        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.black
        self.penStyle = Qt.SolidLine
        self.capStyle = Qt.RoundCap

        # ссылка на последнюю позицию мыши
        self.lastPoint = QPoint()


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        # Изменение размера кисти колесиком мышки

        self.penWidth = QSlider(Qt.Horizontal)
        self.penWidth.setMinimum(2)
        self.penWidth.setMaximum(35)
        self.penWidth.setTickInterval(2)
        self.penWidth.setValue(3)
        self.penWidth.setTickPosition(QSlider.TicksBelow)
        self.penWidth.setFixedWidth(120)

        self.penWidth.valueChanged.connect(self.slider_change)
        #Скролинг работает только если навестись на линейку


        centralWidget = QWidget()

        toolBar = self.addToolBar("My Toolbar")
        toolBar.setAllowedAreas(Qt.LeftToolBarArea)
        toolBar.allowedAreas()

        toolBar.addWidget(self.penWidth)
        toolBar.addSeparator()

        self.setCentralWidget(centralWidget)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    # обработчик событий (нажатие)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True  # теперь мы входим в режим рисования
            self.lastPoint = event.pos()  # новая точка сохраняется как последняя точка
            print(self.lastPoint)


    # обработчик событий (продолжаем нажимать)
    def mouseMoveEvent(self, event):
        if (event.buttons() and Qt.LeftButton) and self.drawing:
            painter = QPainter(self.image)  #позволяет рисовать на холсте
            painter.setPen(QPen(self.brushColor, self.brushSize, self.penStyle, self.capStyle))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()


    # обработчик событий (прекращение нажатия)
    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



    # Слоты сохранения, путь
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()# Заполняет холст белым

    def threepx(self):
        self.brushSize = 3

    def fivepx(self):
        self.brushSize = 5

    def sevenpx(self):
        self.brushSize = 7

    def ninepx(self):
        self.brushSize = 9

    def black(self):
        self.brushColor = Qt.black

    def red(self):
        self.brushColor = Qt.red

    def green(self):
        self.brushColor = Qt.green

    def yellow(self):
        self.brushColor = Qt.yellow

    def white(self):
        self.brushColor = Qt.white

    def blue(self):
        self.brushColor = Qt.blue


    def slider_change(self):
        print(str(self.penWidth.value()))
        self.brushSize = int(str(self.penWidth.value()))


    def flatCap(self):
        self.capStyle = Qt.FlatCap

    def squareCap(self):
        self.capStyle = Qt.SquareCap

    def roundCap(self):
        self.capStyle = Qt.RoundCap


    def solidLine(self):
        self.penStyle = Qt.SolidLine

    def dashLine(self):
        self.penStyle = Qt.DashLine


    def dotLine(self):
        self.penStyle = Qt.DotLine

    def dashDotLine(self):
        self.penStyle = Qt.DashDotLine

    def dashDotDotLine(self):
        self.penStyle = Qt.DashDotDotLine

        #Вызов всех инструментов


app = QApplication(sys.argv)
assignment = Window()

sys.exit(app.exec_())


# http://doc.qt.io/qt-5/qpen.html
# про все фишки QPen
