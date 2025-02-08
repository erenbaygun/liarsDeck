# Liar's Deck

Liar's Deck is a card game that focuses on playing cards and deception. Players can play cards face down and are allowed to make false statements about the cards they've played. The core of the game lies in the psychological warfare between players and judging whether opponents are lying.

## Basic Setup of Liar's Deck:

- The deck consists of 20 cards: 6 Aces, 6 Kings, 6 Queens, and 2 Jokers
- Jokers can substitute for any card
- 2-4 players participate, each starting with 5 cards
- Each player holds a revolver with 1 bullet randomly loaded in one of - the 6 chambers
- Each player has a maximum of 30 seconds for thinking and decision-making

### Game Process of Liar's Deck:
1. At the beginning of each round, the system designates the "liar's card" type for this round (e.g., "Ace" or  "King").
2. Players take turns playing cards, 1-3 cards each time. For example, throw out 2 cards means the player claims to have played 2 "Aces".
3. The next player can choose to:
    - Believe the previous player's statement and play their own cards
    - Challenge the previous player's play (Call Liar!), indicating "I don't believe you just played 2 'Aces'". Then the system reveals the pile to verify.
        - If the previous player didn't play 2 cards (e.g., 0 "Aces"), the challenge is successful, and the previous player undergoes a death roulette judgment;
        - If the previous player indeed played 2 "Aces" (including Jokers), the challenge fails, and the challenging player undergoes a death roulette judgment;Gun
4. Death roulette judgment means firing the gun at oneself. If it's an empty chamber, the game proceeds to the next round; if successful, the player is eliminated, and the game continues to the next round
5. The game continues until only one player remains, who becomes the winner.

## Requirements

- Python 3.x  
- No additional libraries are required; the game uses standard Python libraries (`random`, `sys`, `time`, etc.) and ANSI escape codes for terminal styling.  
- Since ANSI color codes are used, if your terminal does not support them, it is recommended to download the [Windows Terminal](https://apps.microsoft.com/detail/9n0dx20hk701?hl=en-US&gl=TR://) application.

## Installation and Running the Game

1. Download the files.
2. Open your terminal and navigate to the project directory.
3. Run the game using the following command:

   ```bash
   python liars_deck.py
   