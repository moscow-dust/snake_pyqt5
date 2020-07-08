import sys
import random

from PyQt5 import ( QtCore, QtWidgets, QtGui)
from PyQt5.QtWidgets import QPushButton, QMessageBox
import pyqtgraph as pg

class Snake(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.bool_moving = False

        super().__init__(parent)
        self.setWindowTitle("snake")
        self.setMinimumSize(600, 600)
        self.field_size = 100

        self.score = 0
        #ways to move: 1 - up, 2 - right, 3 - down, 4 - left
        self.way_to_move = 1
        self.snake_loc_x = list([1, 1])
        self.snake_loc_y = list([2, 1])
        self.snake_tail = list([0, 0])
        self.is_moving = True

        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.lay = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.lay)

        self.btn_restart = QPushButton("перезапуск", self)
        self.btn_pause = QPushButton("пауза", self)
        self.btn_exit = QPushButton("выход", self)
        
        self.btn_exit.clicked.connect(self.buttonExitClicked)
        self.btn_pause.clicked.connect(self.buttonPauseClicked)
        self.btn_restart.clicked.connect(self.buttonRestartClicked)


        # Холст с графиками (2D pyqtgraph)
        self.vlay = QtWidgets.QVBoxLayout()
        self.lay.addLayout(self.vlay)
        self.__init_plots()

        self.pg_view = pg.GraphicsObject()
        self.lay.addWidget(self.main_plot)
        self.lay.addWidget(self.btn_exit)
        self.lay.addWidget(self.btn_pause)
        self.lay.addWidget(self.btn_restart)
        self.statusBar().showMessage("Current Score = %d" % self.score)
        
        self.counter = 0
        self.timer_id = self.startTimer(100)
        if self.timer_id == -1:
            self.buttonExitClicked()


    def __init_plots(self):
        self.main_plot = pg.PlotWidget()
        self.main_plot.setXRange(0, self.field_size + 1)
        self.main_plot.setYRange(0, self.field_size + 1)
        self.plot_item = self.main_plot.getPlotItem()
        #hide axis's and all buttons , create visual field
        self.plot_item.showAxis('left', show=False)
        self.plot_item.showAxis('bottom', show=False)
        self.plot_item.hideButtons()
        self.plot_item.addLine(x = 0)
        self.plot_item.addLine(y = 0)
        self.plot_item.addLine(y = self.field_size + 1)
        self.plot_item.addLine(x = self.field_size + 1)

        self.apple = self.plot_item.plot()
        self.apple.setSymbol('o')
        self.apple.setSymbolSize(8)
        self.apple.setSymbolBrush(pg.mkBrush(color=(255, 0, 0)))

        self.genApple()

        self.curve = self.plot_item.plot()
        self.curve.setSymbol('d')
        self.curve.setData(self.snake_loc_x, self.snake_loc_y)


    def genApple(self):
        self.apple_posx = random.randint(1, self.field_size - 1)
        self.apple_posy = random.randint(1, self.field_size - 1)
        while self.isAppleInSnake():
            self.apple_posx = random.randint(1, self.field_size)
            self.apple_posy = random.randint(1, self.field_size)
        self.apple.setData(list([self.apple_posx]), list([self.apple_posy]))

    def isAppleInSnake(self):
        if self.apple_posx in self.snake_loc_x:
            return True
        elif self.apple_posy in self.snake_loc_y:
            return True
        else:
            return False

    def isEatenApple(self):
        if (self.snake_loc_x[0] == self.apple_posx) and \
          (self.snake_loc_y[0] == self.apple_posy):
            self.score += 1
            self.statusBar().showMessage("Current Score = %d" % self.score)
            self.genApple()
            self.snake_loc_x.append(self.snake_tail[0])
            self.snake_loc_y.append(self.snake_tail[1])


    def timerEvent(self, event):
        if self.is_moving == True:
            self.counter += 1

            self.snake_tail[0], self.snake_tail[1] \
                = self.snake_loc_x.pop(), self.snake_loc_y.pop()

            #moving up
            if self.way_to_move == 1:
                self.snake_loc_y.insert(0, self.snake_loc_y[0] + 1)
                self.snake_loc_x.insert(0, self.snake_loc_x[0])
                if (self.field_size in self.snake_loc_y) or (0 in self.snake_loc_y):
                    if self.failureMsgBox() == 1:
                        return 
            #moving right
            elif self.way_to_move == 2:
                self.snake_loc_x.insert(0, self.snake_loc_x[0] + 1)
                self.snake_loc_y.insert(0, self.snake_loc_y[0])
                if (self.field_size in self.snake_loc_x) or (0 in self.snake_loc_x):
                    if self.failureMsgBox() == 1:
                        return 
            #moving down
            elif self.way_to_move == 3:
                self.snake_loc_y.insert(0, self.snake_loc_y[0] - 1)
                self.snake_loc_x.insert(0, self.snake_loc_x[0])
                if (self.field_size in self.snake_loc_y) or (0 in self.snake_loc_y):
                    if self.failureMsgBox() == 1:
                        return 
            #moving left
            elif self.way_to_move == 4:
                self.snake_loc_x.insert(0, self.snake_loc_x[0] - 1)
                self.snake_loc_y.insert(0, self.snake_loc_y[0])
                if (self.field_size in self.snake_loc_x) or (0 in self.snake_loc_x):
                    if self.failureMsgBox() == 1:
                        return 
            #ну, а вдруг :D
            elif self.failureMsgBox() == 1:
                return 
            #проверка на столкновение змеи с самой собой
            for i in range(1, len(self.snake_loc_x)):
                if (self.snake_loc_x[0] == self.snake_loc_x[i]) and \
                  (self.snake_loc_y[0] == self.snake_loc_y[i]):
                    if self.failureMsgBox() == 1:
                        return 

            self.isEatenApple()

            self.curve.clear()
            self.curve.setData(self.snake_loc_x, self.snake_loc_y)
        
    def failureMsgBox(self):
        Mbox = QMessageBox()
        Mbox.setIcon(QMessageBox.Warning)
        Mbox.setText("You lost")
        ExitButton = Mbox.addButton('EXIT', QMessageBox.AcceptRole)
        Mbox.addButton('Restart', QMessageBox.RejectRole)
        Mbox.setModal(True)
        Mbox.exec()
        if Mbox.clickedButton() == ExitButton:
            self.buttonExitClicked()
            return 0
        else:
            self.buttonRestartClicked()
            return 1

    def buttonExitClicked(self):
        QtCore.QCoreApplication.quit()

    def buttonRestartClicked(self):
        self.score = 0
        #ways to move: 1 - up, 2 - right, 3 - down, 4 - left
        self.way_to_move = 1
        self.snake_loc_x = list([1, 1])
        self.snake_loc_y = list([2, 1])

    def buttonPauseClicked(self):
        self.is_moving = False
        Mbox = QMessageBox()
        Mbox.setIcon(QMessageBox.Information)
        Mbox.setText("PAUSE")
        quitButton = Mbox.addButton('Quit from pause', QMessageBox.AcceptRole)
        Mbox.exec()
        if Mbox.clickedButton() == quitButton:
            self.is_moving = True

    def keyPressEvent(self, event):
        key_value = event.key()

        if key_value  in [QtCore.Qt.Key_Up, QtCore.Qt.Key_W]:
            if self.way_to_move != 3:
                self.way_to_move = 1
            return
        elif key_value  in [QtCore.Qt.Key_Down, QtCore.Qt.Key_S]:
            if self.way_to_move != 1:
                self.way_to_move = 3
            return
        elif key_value  in [QtCore.Qt.Key_Right, QtCore.Qt.Key_D]:
            if self.way_to_move != 4:
                self.way_to_move = 2
            return
        elif key_value  in [QtCore.Qt.Key_Left, QtCore.Qt.Key_A]:
            if self.way_to_move != 2:
                self.way_to_move = 4
            return

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window=Snake()
    window.setWindowTitle("Snake")
    window.show()
    sys.exit(app.exec_())
