import poker_game
import gui
import sys


def get_next_active_player(game, current_player):
    amount_of_players = len(game.players_in_round)
    current_player = (current_player + 1) % amount_of_players
    while game.players_in_round[current_player].has_folded:
        current_player = (current_player + 1) % amount_of_players

    return current_player


def start_betting_round(game, round_type):

    ui.displayBlinds(game.big_blind_player_index,
                     game.small_blind_player_index, game.dealer_button_player_index)
    ui.displayChips([player.chips for player in game.players])

    if round_type == "pre-flop":
        # This code is for cycling through players correctly
        for player in game.players_in_round:
            player.has_folded = False
            player.is_all_in = False
            player.has_acted = False

        # In a pre-flop round, the first player to act is the player after the big blind,
        # and the last player to act is the big blind player
        current_player = (game.big_blind_player_index +
                          1) % len(game.players_in_round)
        last_player = (game.big_blind_player_index +
                       1) % len(game.players_in_round)

        # Add the small blinds and big blinds contributions to the player pot contributions
        game.player_bets[game.players_in_round[game.small_blind_player_index].name
                         ] = game.small_blind_value
        game.player_bets[game.players_in_round[game.big_blind_player_index].name
                         ] = game.big_blind_value

        game.current_highest_bet = game.big_blind_value

    elif round_type == "post-flop":
        # This code is for cycling through players correctly
        for player in game.players_in_round:
            if player.has_folded or player.is_all_in:
                player.has_acted = True
            else:
                player.has_acted = False

        # In a post-flop round, the first player to act is the small blind player,
        # and the last player to act is the player with the dealer button
        current_player = game.small_blind_player_index
        last_player = (game.dealer_button_player_index +
                       1) % len(game.players_in_round)

    while game.players_in_round[current_player].has_folded:
        current_player = (current_player + 1) % len(game.players_in_round)

    while not game.is_betting_round_over(current_player, last_player):

        player = game.players_in_round[current_player]

        # If the next player after the last player has acted, make everyone NOT act
        # if game.players_in_round[last_player].has_acted and game.players_in_round[get_next_active_player(game, last_player)].has_acted:
        #     for p in game.players_in_round:
        #         p.has_acted = False

        # Get input from the user TEMPORARY
        print(f"{player.name}: {player.chips} chips")
        print(f"Cards: {player.hand.cards}")
        while True:
            choice = input("Choose: ")

            if choice == "fold":
                last_player = game.fold(current_player, last_player)
                # The current_player will be incremented by at the end of this, which will skip a player without the line of code below
                # new_player = (
                #     current_player - 1) % len(game.players_in_round)

                # if current_player == (last_player - 1) % len(game.players_in_round):
                #     last_player = new_player

                # current_player = new_player
                ui.displayFolded(game.players)
                break

            # IMPORTANT NOTE: The check button will be replaced will the call button if the user can not check.
            elif choice == "check":

                # Check if the current player's contribution to the pot is equal to the highest bet (check criteria)
                if game.player_bets[player.name] == game.current_highest_bet:
                    # Check by moving to the next player (do nothing as the current_player is incremented at the end)
                    break
                else:
                    continue

            elif choice == "call":
                call_amount = game.current_highest_bet - \
                    game.player_bets[player.name]
                # If the player has enough chips to call, put the appropriate amount of chips in the pot
                if player.chips > call_amount:
                    # Call
                    player.chips -= call_amount
                    game.pot.add_chips(call_amount)
                    game.player_bets[player.name] += call_amount
                else:
                    # If the player doesn't have enough chips to call or has exactly the amount of chips to call, go all in
                    remaining_chips = player.chips
                    game.pot.add_chips(
                        remaining_chips)
                    player.chips = 0
                    game.player_bets[player.name] += remaining_chips
                    player.is_all_in = True
                break

            elif choice == "raise":
                # If the player has enough money to raise, raise
                if player.chips > game.current_highest_bet - game.player_bets[player.name]:
                    # The player should only be able to raise up to the total amount of chips that they have.
                    # This could be implemented in the GUI as a slider, but for now
                    # I will implement a while loop that just asks the player for a raise_amount until it is valid.
                    raise_amount = player.chips + 1
                    while raise_amount > player.chips or raise_amount <= (game.current_highest_bet - game.player_bets[player.name]) or raise_amount < game.minimum_raise_amount:
                        if raise_amount < game.minimum_raise_amount:
                            print(
                                f"Raise amount should be at least {game.minimum_raise_amount}")
                        raise_amount = int(input("Raise amount: "))

                    game.current_highest_bet = raise_amount + \
                        game.player_bets[player.name]
                    player.chips -= raise_amount
                    game.pot.add_chips(raise_amount)
                    game.player_bets[player.name] = game.current_highest_bet

                # Else if they don't have enough money to raise, tell them that they don't (this will cause the player's turn to be skipped,
                # so the option to raise must not be on the screen if the player does not have enough money to raise)
                else:
                    print("You do not have enough money to raise.")
                    continue
                break

        # After they have made their choice, move to the next player to the left.
        print(f"NOW, {player.name}: {player.chips} chips")
        ui.displayChips([player.chips for player in game.players])
        player.has_acted = True
        current_player = (
            current_player + 1) % len(game.players_in_round)

        # The next player will be the next available player who hasn't yet folded
        while game.players_in_round[current_player].has_folded:
            # The method below is called to check if there is only 1 remaining player so that this loop does not infinitely go on
            if game.is_betting_round_over(current_player, last_player):
                break
            # If the current player is the last player, don't increment any further so that the round can be detected as over
            if current_player != last_player:
                current_player = (
                    current_player + 1) % len(game.players_in_round)


def start_poker_round(game):
    game.reset_bets()
    game.handle_blinds()

    # The order of play is implemented from https://automaticpoker.com/poker-basics/texas-holdem-order-of-play/
    start_betting_round(game, "pre-flop")
    game.flop()
    ui.displayBoard(game.get_board_cards())
    ui.displayFolded(game.players)
    start_betting_round(game, "post-flop")
    game.turn_river()
    ui.displayBoard(game.get_board_cards())
    ui.displayFolded(game.players)
    start_betting_round(game, "post-flop")
    game.turn_river()
    ui.displayBoard(game.get_board_cards())
    ui.displayFolded(game.players)
    start_betting_round(game, "post-flop")

    # I am displaying the folded players after displaying all of the players' cards - a cheeky way of implementing this.

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
