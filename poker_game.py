# Cards: https://opengameart.org/content/playing-cards-vector-png

from random import randint


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} {self.suit}"


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank)
                      for suit in ["Clubs", "Diamonds", "Spades", "Hearts"] for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]]

    def shuffle(self):
        for i in range(len(self.cards)):
            swap_number = randint(0, len(self.cards) - 1)
            self.cards[swap_number], self.cards[i] = self.cards[i], self.cards[swap_number]

    # The following function is for testing purposes only, remove at the end of project
    def print_cards(self):
        for card in self.cards:
            print(card)

    def deal_card(self):
        # This method deals a single card from the top of the deck
        return self.cards.pop()


class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = Hand([])

    def add_card(self, card):
        self.hand.cards.append(card)


class Game:
    def __init__(self, player_names, starting_chips=500):
        self.players = [Player(name, starting_chips) for name in player_names]
        self.big_blind_value = 4
        self.small_blind_value = 2
        self.big_blind_player_index = 0
        self.small_blind_player_index = randint(0, len(self.players) - 1)
        self.pot = Pot()
        self.board = []
        self.deck = Deck()
        self.deck.shuffle()
        self.minimum_raise_amount = self.big_blind_value * 2
        self.player_bets = {}

    def get_player_cards(self):
        # Create poker card images
        cards = []
        for player in self.players:
            for card in player.hand.cards:
                cards.append(f"{card.rank}_of_{card.suit}")

        # Show which player has the big blind and the small blind
        # print(self.small_blind_player_index,
        #       self.big_blind_player_index)

        return cards

    def get_board_cards(self):
        cards = []
        for card in self.board:
            cards.append(f"{card.rank}_of_{card.suit}")

        return cards

    def deal_cards(self, num_cards, player):
        for i in range(num_cards):
            card = self.deck.deal_card()
            player.add_card(card)

    def handle_blinds(self):
        amount_of_players = len(self.players)

        # Increment the small and big blind indexes by 1. Wraps around to the start if needed
        self.small_blind_player_index = (
            self.small_blind_player_index + 1) % amount_of_players
        self.big_blind_player_index = (
            self.small_blind_player_index + 1) % amount_of_players

        # Deducts the blind values from the appropriate player's chips and adds it to the pot
        self.players[self.big_blind_player_index].chips -= self.big_blind_value
        self.pot.add_chips(self.big_blind_value)

        self.players[self.small_blind_player_index].chips -= self.small_blind_value
        self.pot.add_chips(self.small_blind_value)

    def fold(self, player_index):
        self.players_in_round.pop(player_index)
        self.player_bets[self.players_in_round[player_index]] = -1

    def distribute_pot(self):
        pass

    def are_bets_equal(self):
        # Get a list of all unique bet amounts
        unique_bets = set(
            bet for bet in self.player_bets.values() if bet != -1)

        # If there's only one unique bet, then all players have the same bet amount
        return len(unique_bets) == 1

    def reset_bets(self):
        # Create variables to track each player's contribution to the pot and the current highest bet
        for player in self.players_in_round:
            self.player_bets[player.name] = 0

    def betting_round(self):
        self.reset_bets()

        # The first player to act is the player to the left of the big blind, and the play is clockwise
        self.players_in_round = self.players
        first_player = (self.small_blind_player_index +
                        1) % len(self.players)
        current_player = first_player

        while not self.are_bets_equal():
            player = self.players_in_round[current_player]

            # Add the small blinds and big blinds contributions to the player pot contributions
            self.player_bets[self.players[self.small_blind_player_index]
                             ] += self.small_blind_value
            self.player_bets[self.players[self.big_blind_player_index]
                             ] += self.big_blind_value
            current_highest_bet = self.big_blind_value

            # Get input from the user TEMPORARY
            choice = input("Choose: ")

            # If the current player chooses fold, then fold
            if choice == "fold":
                self.fold(current_player)

            # If the current player can check and they choose check, check
            elif choice == "check":

                # Check if the current player's contribution to the pot is equal to the previous player's contribution (check criteria)
                if self.player_bets[current_player] == current_highest_bet:
                    # Check by moving to the next player (do nothing as the current_player is incremented at the end)
                    pass

            # If the current player calls, call. The previous_bet is the amount to call.
            elif choice == "call":
                call_amount = current_highest_bet - \
                    self.player_bets[current_player]
                # If the player has enough chips to call, put the appropriate amount of chips in the pot
                if player.chips >= call_amount:
                    # Call
                    player.chips -= call_amount
                    self.pot.add_chips(call_amount)
                    self.player_bets[current_player] += call_amount
                else:
                    # If the player DOES NOT have enough chips to call, go all in
                    remaining_chips = player.chips
                    self.pot.add_chips(
                        remaining_chips)
                    player.chips = 0
                    self.player_bets[current_player] += remaining_chips

            # If the current player raises, raise
            elif choice == "raise":
                # If the player has enough money to raise, raise
                if player.chips > current_highest_bet - self.player_bets[current_player]:
                    # The player should only be able to raise up to the total amount of chips that they have.
                    # This could be implemented in the GUI as a slider, but for now
                    # I will implement a while loop that just asks the player for a raise_amount until it is valid.
                    raise_amount = player.chips + 1
                    while raise_amount > player.chips or raise_amount < self.minimum_raise_amount:
                        if raise_amount < self.minimum_raise_amount:
                            print(
                                f"Raise amount should be at least {self.minimum_raise_amount}")
                        raise_amount = int(input("Raise amount: "))

                    current_highest_bet += raise_amount
                    player.chips -= raise_amount
                    self.pot.add_chips(raise_amount)
                    self.player_bets[current_player] = current_highest_bet

                # Else if they don't have enough money to raise, tell them that they don't (this will cause the player's turn to be skipped,
                # so the option to raise must not be on the screen if the player does not have enough money to raise)
                print("You do not have enough money to raise.")

                # After they have made their choice, move to the next player to the left.
            current_player = (first_player + 1) % len(self.players)

        self.distribute_pot()

    def flop(self):
        for i in range(3):
            card = self.deck.deal_card()
            self.board.append(card)

    def turn_river(self):
        card = self.deck.deal_card()
        self.board.append(card)


class Pot:
    def __init__(self):
        self.chips = 0

    def add_chips(self, amount):
        self.chips += amount

    def subtract_chips(self, amount):
        self.chips -= amount

    def reset_pot(self):
        self.chips = 0


class Hand:
    def __init__(self, cards):
        self.cards = cards

    def evaluate_strength(self):
        pass
