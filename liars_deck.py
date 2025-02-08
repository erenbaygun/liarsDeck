import random
import sys
import time

# ANSI color codes
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
BRIGHT_BLUE = "\033[94m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
BRIGHT_CYAN = "\033[96m"
WHITE = "\033[37m"

# ANSI style codes
BOLD = "\033[1m"
RESET = "\033[0m"

# Game deck 
DECK = ['A'] * 6 + ['K'] * 6 + ['Q'] * 6 + ['J'] * 2


def fire_revolver(player): #uses revolver to the player
    print(f"{RED}- {player.name} pulls the trigger...", end=" ")
    time.sleep(3)
    if random.randint(1, 6) == 1:
        print(f"{RED}BANG! {BOLD}{player.name}{RESET}{RED} has been eliminated!")
        player.alive = False
        return True
    else:
        print(f"{GREEN}click. (Empty)")
        time.sleep(3)
        return False

def validate_move(cards_played, liars_card):
    for card in cards_played:
        if card != liars_card and card != 'J': # if the card is not the liars card or joker
            return False
    return True



class Player:
    def __init__(self, name, is_human=True):
        self.name = name
        self.hand = [] # players card hand
        self.is_human = is_human
        self.alive = True
        self.shots = 6 # how much revolver shots left

    def draw_cards(self, deck):
        while len(self.hand) < 5 and deck: # deals 5 cards to player
            self.hand.append(deck.pop())

    def show_hand(self):
        return "  ".join(f"[{i+1}:{card}]" for i, card in enumerate(self.hand))

    def choose_move(self, liars_card):
        if self.is_human: # if player is controlled
            print(f"\n{BLUE}{BOLD}It's your turn, {self.name}!{RESET}")
            time.sleep(1)
            print(f"{BLUE}Your hand: {CYAN}{self.show_hand()}{RESET}")
            print(f"{BLUE}1- If you want to play a card type in index number of the card.")
            print(f"{BLUE}2- Type {BOLD}'liar'{RESET}{BLUE} to call liar.{RESET}")
            choice = input(f"{BRIGHT_CYAN}Your choice: {YELLOW}").strip().lower()
            if choice == 'liar':
                return 'liar', []
            else:
                indices = choice.split()
                if not indices:
                    print(f"{BLUE}You did not specify a card. Randomly selecting 1 of your cards.")
                    indices = ['1']
                if len(indices) > 3:
                    indices = indices[:3]
                try:
                    selected = []
                    unique_indices = []
                    for token in indices:
                        idx = int(token) - 1
                        if idx < 0 or idx >= len(self.hand):
                            print(f"{BLUE}You entered an invalid index, selecting your first card.")
                            idx = 0
                        if idx not in unique_indices:
                            unique_indices.append(idx)
                    unique_indices.sort()
                    for idx in unique_indices:
                        selected.append(self.hand[idx])
                    return 'play', selected
                except ValueError:
                    print(f"{BLUE}Invalid input, randomly selecting 1 of your cards.")
                    return 'play', [self.hand[0]]
        else: # if player is not human decides random
            liar_cards = [card for card in self.hand if card == liars_card or card == 'J']
            non_liar_cards = [card for card in self.hand if card != liars_card and card != 'J']

            # try to play a card
            if liar_cards and random.random() < 0.5:
                num = random.randint(1, min(3, len(liar_cards)))
                selected = random.sample(liar_cards, num)
                return 'play', selected
            else:
                if non_liar_cards:
                    num = random.randint(1, min(3, len(non_liar_cards)))
                    selected = random.sample(non_liar_cards, num)
                    return 'play', selected
                else:
                    num = random.randint(1, min(3, len(liar_cards)))
                    selected = random.sample(liar_cards, num)
                    return 'play', selected

class Table:
    def __init__(self, players):
        self.players = players  # liste, canlı oyuncular
        self.deck = DECK.copy()
        random.shuffle(self.deck)
        self.liars_card = None
        self.prev_move = None     # önceki hamlede oynanan kartlar
        self.prev_player = None   # hamleyi yapan oyuncu

    def deal_initial_cards(self):
        for player in self.players:
            for _ in range(5): # deals 5 cards to players
                if self.deck:
                    player.hand.append(self.deck.pop())

    def select_liars_card(self): # selects the liar card
        possible = [card for card in self.deck if card != 'J']
        if not possible:
            possible = ['A', 'K', 'Q']
        self.liars_card = random.choice(possible)
        return self.liars_card

    def next_turn(self, current_player):
        idx = self.players.index(current_player)
        next_idx = (idx + 1) % len(self.players)
        return self.players[next_idx]

    def remove_cards_from_player(self, player, cards):
        for card in cards:
            try:
                player.hand.remove(card)
            except ValueError:
                pass

    def check_game_over(self):
        if len(self.players) == 1:
            return True, f"{PURPLE}{BOLD}{self.players[0].name}{GREEN} is the last standing player and the winner!"
        return False, ""

    def check_round_over(self):
        for player in self.players:
            if len(player.hand) == 0: # if player has no cards left end round
                return True, player
        return False, None

    def replenish_hands(self):
        for player in self.players:
            player.draw_cards(self.deck)

def main():
    print(f"{BOLD}{RED}------ Welcome to Liar's Deck ------{RESET}")
    while True:
        try:
            player_count = int(input(f"{BLUE}- How many players are playing (2-4): {YELLOW}"))
            if player_count < 2 or player_count > 4:
                print(f"{RED}Enter a integer value between 2 and 4.{RESET}")
                continue
            break
        except ValueError:
            print(f"{RED}Invalid input, enter a integer.{RESET}")


    human_name = input(f"{BLUE}- Enter your name: {PURPLE}") # set real player
    players = [Player(human_name, is_human=True)]

    for i in range(player_count - 1):
        players.append(Player(f"Player_{i+1}", is_human=False)) # set bot players

    table = Table(players)
    table.deal_initial_cards()
    liars_card = table.select_liars_card()
    print(f"{BLUE}- Liar's Card for this round: {BOLD}{RED}{liars_card}{RESET}")
    time.sleep(0.3)

    
    current_player = random.choice(table.players)
    print(f"{PURPLE}{BOLD}{current_player.name}{RESET}{CYAN} starts the game!{RESET}")
    time.sleep(0.7)

    round_number = 1

    
    while True:
        print("\n" + f"{RED}="*40)
        print(f"{BOLD}{BLUE}Round {round_number}{RESET}")
        print(f"{BLUE}- Liar's Card: {RED}{liars_card}{RESET}")
        print(f"{BLUE}- Turn: {PURPLE}{current_player.name}'s{RESET}{BLUE} turn.")
        time.sleep(3)


        if table.prev_move is not None and current_player.alive: # if its not the first move player can call liar
            if current_player.is_human:
                decision = input(f"{BLUE}- Do you want to call {BOLD}LIAR{RESET}{BLUE} to {PURPLE}{table.prev_player.name}{RESET}{BLUE}? (y/n): {YELLOW}").strip().lower()
                challenge = (decision == 'y' or decision == 'yes')
            else: 
                challenge = (random.random() < 0.4)

            if challenge:
                print(f"{BLUE}- {PURPLE}{current_player.name} {BLUE}called {BOLD}LIAR!{RESET}")
                time.sleep(1)
                print(f"{BLUE}- {PURPLE}{table.prev_player.name} {BLUE}played {len(table.prev_move)} cards.{RESET}")
                print(f"{BLUE}- Previous cards: {', '.join(table.prev_move)}")
                if validate_move(table.prev_move, liars_card):
                    print(f"{RED}- Call wasn't correct. {PURPLE}{current_player.name}{RED} has to shoot!{RESET}")
                    time.sleep(2)
                    if fire_revolver(current_player):
                        
                        table.players.remove(current_player) # if player dies remove from table

                        over, message = table.check_game_over() # is game ended
                        if over:
                            print(f"{BOLD}{GREEN}{message}{RESET}")
                            sys.exit() # ends game
                    else:
                        current_player.shots -= 1
                else:
                    print(f"{GREEN}- Call was correct. {PURPLE}{table.prev_player.name}{GREEN} has to shoot!{RESET}")
                    time.sleep(2)
                    if fire_revolver(table.prev_player):

                        table.players.remove(table.prev_player) # if player dies remove from table

                        over, message = table.check_game_over() # is game ended
                        if over:
                            print(f"{BOLD}{GREEN}{message}{RESET}")
                            sys.exit() # ends game
                    else:
                        table.prev_player.shots -= 1
                
                round_winner = current_player
                if len(table.prev_player.hand) == 0:
                    round_winner = table.prev_player
                table.prev_move = None
                table.prev_player = None
                print(f"{YELLOW}- {PURPLE}{round_winner.name}'s{YELLOW} hand is empty. Round is over! Next round starting with {PURPLE}{round_winner.name}'s {YELLOW}move.{RESET}")
                time.sleep(0.3)
                
                table.replenish_hands()
                
                liars_card = table.select_liars_card()
                print(f"{BLUE}- Next rounds Liar's Card: {BOLD}{RED}{liars_card}{RESET}")
                time.sleep(0.3)
                current_player = round_winner
                round_number += 1
                time.sleep(4)
                continue

        move_type, selected_cards = current_player.choose_move(liars_card) # get move from player
        if move_type == 'liar':
            if table.prev_move is None: # if player is making the first move
                print(f"{YELLOW}- There is no card on table. Play a card!{RESET}")
                current_player = table.next_turn(current_player)
                time.sleep(4)
                continue
            else:
                continue
        elif move_type == 'play':
            cards_to_play = selected_cards
            claim_count = len(cards_to_play)
            print(f"{BLUE}- {PURPLE}{current_player.name}{BLUE} says '{BOLD}I throw {claim_count} {liars_card}'{RESET}")
            time.sleep(0.3)
            table.remove_cards_from_player(current_player, cards_to_play)
            table.prev_move = cards_to_play
            table.prev_player = current_player

        
        current_player = table.next_turn(current_player) # next player turn

        
        round_over, round_winner = table.check_round_over()
        if round_over:
            print(f"{YELLOW}- {PURPLE}{round_winner.name}'s{YELLOW} hand is empty. Round is over! Next round starting with {PURPLE}{round_winner.name}'s {YELLOW}move.{RESET}")
            time.sleep(0.3)
            table.replenish_hands()
            liars_card = table.select_liars_card()
            print(f"{BLUE}- Next rounds Liar's Card: {BOLD}{RED}{liars_card}{RESET}")
            time.sleep(0.3)
            current_player = round_winner
            round_number += 1

        over, message = table.check_game_over() # check if game ended
        if over:
            print(f"{BOLD}{GREEN}{message}{RESET}")
            break

        time.sleep(4)

    print(f"{BOLD}{RED}Game ended!{RESET}")

main()
