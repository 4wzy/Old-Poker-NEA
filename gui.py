import sys
import qdarktheme
from PySide6.QtGui import QPixmap, QColor, QPen, QBrush
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem

from poker_game import game


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Texas Hold'Em Poker")

        # Create poker card images
        cards = []
        for player in game.players:
            for card in player.hand.cards:
                cards.append(f"{card.rank}_of_{card.suit}")

        self.labels = []
        for card in cards:
            pixmap = QPixmap(f"images/cards/{card}")
            # Sets the width=100 and height=140
            pixmap = pixmap.scaled(100, 140)
            label = QLabel()
            label.setPixmap(pixmap)
            self.labels.append(label)

        # create buttons and labels
        self.checkButton = QPushButton("Check")
        self.foldButton = QPushButton("Fold")
        self.raiseButton = QPushButton("Raise")
        self.betButton = QPushButton("Bet")

        self.label1 = QLabel("Player 1:")

        self.label2 = QLabel("Player 2:")

        # create vertical and horizontal layouts
        vLayout1 = QVBoxLayout()
        vLayout2 = QVBoxLayout()
        hLayout = QHBoxLayout()

        # add buttons and labels to the layouts
        vLayout1.addWidget(self.label1)
        vLayout1.addWidget(self.checkButton)
        vLayout1.addWidget(self.foldButton)
        for label in self.labels[:2]:
            vLayout1.addWidget(label)

        vLayout2.addWidget(self.label2)
        vLayout2.addWidget(self.raiseButton)
        vLayout2.addWidget(self.betButton)
        for label in self.labels[2:]:
            vLayout2.addWidget(label)

        # create a QGraphicsView widget and set its scene to a new QGraphicsScene
        view = QGraphicsView()
        self.scene = QGraphicsScene()
        view.setScene(self.scene)

        # add the poker table to the scene
        table_radius = 200
        table_pen_width = 5
        table_brush_color = QColor(0, 255, 0)
        table_pen_color = QColor(0, 0, 0)

        table = QGraphicsEllipseItem(-table_radius, -
                                     table_radius, 2*table_radius, 2*table_radius)
        pen = QPen(table_pen_color)
        pen.setWidth(table_pen_width)
        brush = QBrush(table_brush_color)
        table.setPen(pen)
        table.setBrush(brush)
        self.scene.addItem(table)

        # --- Testing
        for p in game.players:
            for c in p.hand.cards:
                print(c)

        hLayout.addLayout(vLayout1)
        hLayout.addWidget(view)
        hLayout.addLayout(vLayout2)

        # set the main widget
        centralWidget = QWidget()
        centralWidget.setLayout(hLayout)
        self.setCentralWidget(centralWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
