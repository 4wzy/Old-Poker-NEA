import poker_game
import gui
import sys


def playBettingRound(game, current_player):
    while True:
        if current_player == game.last_player and game.are_bets_equal():
            break

        player = game.players_in_round[current_player]
        ui.pushButton.clicked.connect(lambda: game.check(player))
        ui.pushButton_2.clicked.connect(lambda: game.action_raise(player))
        ui.pushButton_3.clicked.connect(lambda: game.fold(player))
        ui.pushButton_4.clicked.connect(lambda: game.call(player))

    if game.action_done:
        ui.displayChips([player.chips for player in game.players])
        current_player = (current_player + 1) % len(game.players_in_round)
        game.action_done = False


def start_betting_round(game, round_type):
    # Handle the blinds
    # NOTE: Due to the way the blinds are handled at the start of the betting round, the blinds will move 4 times instead of 3.
    # A way to fix this is to have another round_type, "last", where the blinds are not handled.
    game.handle_blinds()

    ui.displayBlinds(game.big_blind_player_index,
                     game.small_blind_player_index, game.dealer_button_player_index)
    ui.displayChips([player.chips for player in game.players])

    if round_type == "pre-flop":
        current_player = (game.big_blind_player_index +
                          1) % len(game.players_in_round)
        game.last_player = (game.big_blind_player_index +
                            1) % len(game.players_in_round)

        # Add the small blinds and big blinds contributions to the player pot contributions
        game.player_bets[game.players[game.small_blind_player_index].name
                         ] = game.small_blind_value
        game.player_bets[game.players[game.big_blind_player_index].name
                         ] = game.big_blind_value

    elif round_type == "post-flop":

        current_player = game.small_blind_player_index
        game.last_player = (game.dealer_button_player_index +
                            1) % len(game.players_in_round)

        game.player_bets[game.players[game.small_blind_player_index].name
                         ] += game.small_blind_value
        game.player_bets[game.players[game.big_blind_player_index].name
                         ] += game.big_blind_value

    game.current_highest_bet += game.big_blind_value

    playBettingRound(game, current_player)


def start_poker_round(game):
    game.reset_bets()

    # The order of play is implemented from https://automaticpoker.com/poker-basics/texas-holdem-order-of-play/
    start_betting_round(game, "pre-flop")
    game.flop()
    ui.displayBoard(game.get_board_cards())
    start_betting_round(game, "post-flop")
    game.turn_river()
    ui.displayBoard(game.get_board_cards())
    start_betting_round(game, "post-flop")
    game.turn_river()
    ui.displayBoard(game.get_board_cards())
    start_betting_round(game, "post-flop")

    game.distribute_pot()


def start_poker(game):
    game.board = []

    # Deal cards to every player
    for player in game.players:
        game.deal_cards(2, player)

    current_cards = game.get_player_cards()
    ui.displayCards(current_cards)

    start_poker_round(game)


# Set up the Poker Game
game = poker_game.Game(["Justin", "Megan", "TestPlayer1",
                        "TestPlayer2", "TestPlayer3", "TestPlayer4"])

# Set up the GUI
app = gui.QtWidgets.QApplication(sys.argv)
gui.qdarktheme.setup_theme()
MainWindow = gui.QtWidgets.QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

# Run the first poker round
# Create the table's deck (community cards)

ui.displayNames([player.name for player in game.players])
start_poker(game)

# Handle exitting the GUI
sys.exit(app.exec_())
