import sys
import qdarktheme
from PySide6.QtGui import QPixmap, QColor, QPen, QBrush
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem

from poker_game import game


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set main window properties
        self.setWindowTitle("Texas Hold'em Poker Game")
        self.setFixedSize(1000, 800)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Add poker table image to central widget
        poker_table_label = QLabel(central_widget)
        # Replace with path to your own image
        poker_table_label.setPixmap("poker_table.png")
        # Adjust positioning and size as necessary
        poker_table_label.setGeometry(200, 100, 600, 500)

        # Create function to load card image based on card string
        def load_card_image(card_str):
            card_rank = card_str[:-1]
            card_suit = card_str[-1]
            # Replace with path to your own image directory
            return QPixmap(f"{card_rank}_of_{card_suit}.png")

        # Create player widgets
        players_layout = QHBoxLayout()
        for i in range(8):
            player_group_box = QGroupBox(f"Player {i+1}")
            player_layout = QVBoxLayout()
            player_name_label = QLabel(f"Player {i+1}")
            player_icon_label = QLabel(central_widget)
            # Replace with path to your own image
            player_icon_label.setPixmap("player_icon.png")
            player_cards_layout = QHBoxLayout()
            card1_str = "AS"  # Replace with actual card string for this player's first card
            card2_str = "KD"  # Replace with actual card string for this player's second card
            card1_label = QLabel()
            card1_pixmap = load_card_image(card1_str)
            card1_label.setPixmap(card1_pixmap)
            card2_label = QLabel()
            card2_pixmap = load_card_image(card2_str)
            card2_label.setPixmap(card2_pixmap)
            player_cards_layout.addWidget(card1_label)
            player_cards_layout.addWidget(card2_label)
            player_layout.addWidget(player_name_label)
            player_layout.addWidget(player_icon_label)
            player_layout.addLayout(player_cards_layout)
            player_group_box.setLayout(player_layout)
            players_layout.addWidget(player_group_box)
        central_widget.setLayout(players_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
