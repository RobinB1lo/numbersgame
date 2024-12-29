from tkinter import *
import random

root = Tk()
root.title("BlackJack - Cards left: 52")  # Initial title with the full deck
root.geometry('900x700')  # Increased height for more space
root.configure(background="#145201")
root.resizable(False, False)  # Lock the window size

# Card class
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def get_rank(self):
        return self.rank
    
    def get_suit(self):
        return self.suit

    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

# Deck class
class Deck:
    ranks = {'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'}
    suits = {'♠', '♥', '♦', '♣'}

    def __init__(self):
        self.deck = [Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits]
        
    def get_deck(self):
        return self.deck
    
    def get_deck_ranks(self):
        self.ranks = []
        for card in self.deck:
            self.ranks.append(card.get_rank())
        return self.ranks
        
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __len__(self):
        return len(self.deck)

# Initialize Deck
d = Deck()
d.shuffle()

dealer_hand = []
player_hand = []
hidden_card = None

# Result Label
result_label = None

# Update the window title with the cards left
def update_title():
    """Updates the title of the window with the number of cards left."""
    root.title(f"BlackJack - Cards left: {len(d) + 1}")

# Draw card on a Canvas
def draw_card(canvas, card, x, y):
    canvas.create_rectangle(x, y, x+100, y+150, fill="white", outline="black", width=2)
    canvas.create_text(x+50, y+30, text=card.get_rank(), font=("Times New Roman", 18), fill="black")
    canvas.create_text(x+50, y+120, text=card.get_suit(), font=("Arial", 35), fill="red" if card.get_suit() in {'♥', '♦'} else "black")

def draw_hidden_card(canvas, x, y):
    canvas.create_rectangle(x, y, x+100, y+150, fill="black", outline="white", width=2)
    canvas.create_text(x+50, y+75, text="?", font=("Arial", 40), fill="white")

# Deal cards
def deal_cards():
    global dealer_hand, player_hand, hidden_card, result_label

    dealer_hand = [d.deal_card(), d.deal_card()]
    player_hand = [d.deal_card(), d.deal_card()]
    hidden_card = dealer_hand[1]

    # Draw dealer's first card and hidden card
    dealer_canvas.delete("all")
    draw_card(dealer_canvas, dealer_hand[0], 10, 10)
    draw_hidden_card(dealer_canvas, 120, 10)

    # Draw player's two cards
    player_canvas.delete("all")
    draw_card(player_canvas, player_hand[0], 10, 10)
    draw_card(player_canvas, player_hand[1], 120, 10)

    # Clear result
    result_label.config(text="")
    winning_probability_label.config(text="")
    update_title()  # Update the title

def hit():
    global player_hand

    # Add a card to the player's hand
    if len(player_hand) < 5:  # Limit player hand to 5 cards (optional for blackjack rules)
        new_card = d.deal_card()
        player_hand.append(new_card)

        # Clear the canvas and redraw all cards in the player's hand
        player_canvas.delete("all")
        for idx, card in enumerate(player_hand):
            draw_card(player_canvas, card, idx * 110, 10)  # Spacing of 110 pixels between cards

        # Check if player has busted
        if calculate_hand_value(player_hand) > 21:
            result_label.config(text="You Busted! Dealer Wins", font=("Times New Roman", 30), fg="red")
        update_title() # Update the title

def dealer_turn():
    global dealer_hand, hidden_card, result_label

    # Reveal the hidden card first
    dealer_canvas.delete("all")
    draw_card(dealer_canvas, dealer_hand[0], 10, 10)
    draw_card(dealer_canvas, hidden_card, 120, 10)

    # Dealer logic: Draw cards until the value of the hand is at least 17
    while calculate_hand_value(dealer_hand) < 17:
        new_card = d.deal_card()
        dealer_hand.append(new_card)

        # Redraw all cards, including the newly added one
        dealer_canvas.delete("all")
        for idx, card in enumerate(dealer_hand):
            draw_card(dealer_canvas, card, idx * 110, 10)  # Spacing of 110 pixels between cards
        update_title()  # Update the title

    # Determine the result
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if player_value > 21:
        result_label.config(text="You Busted! Dealer Wins", font=("Times New Roman", 30), fg="red")
    elif dealer_value > 21:
        result_label.config(text="Dealer Busted! You Win", font=("Times New Roman", 30), fg="green")
    elif player_value > dealer_value:
        result_label.config(text="You Win!", font=("Times New Roman", 30), fg="green")
    elif player_value < dealer_value:
        result_label.config(text="Dealer Wins", font=("Times New Roman", 30), fg="red")
    else:
        result_label.config(text="It's a Tie!", font=("Times New Roman", 30), fg="blue")

def stay():
    dealer_turn()

def calculate_hand_value(hand):
    """Calculate the value of a hand in Blackjack."""
    value = 0
    aces = 0

    for card in hand:
        if card.get_rank() in {'J', 'Q', 'K'}:
            value += 10
        elif card.get_rank() == 'A':
            value += 11
            aces += 1
        else:
            value += int(card.get_rank())

    # Adjust for aces if value exceeds 21
    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value

# Shuffle deck
def shuffle_deck():
    global d
    d = Deck()
    d.shuffle()
    dealer_canvas.delete("all")
    player_canvas.delete("all")
    result_label.config(text="")
    winning_probability_label.config(text="")
    update_title()  # Reset title to 52 cards

def calculate_winning_probability():
    """Calculate and display the probability of the player winning."""
    dealer_card_val = calculate_hand_value([dealer_hand[0]])
    player_hand_val = calculate_hand_value(player_hand)

    losing_count = 0
    for card in d.get_deck():
        if dealer_card_val + calculate_hand_value([card]) >= player_hand_val:
            losing_count += 1

    if dealer_card_val + calculate_hand_value([hidden_card]) >= player_hand_val:
        losing_count += 1
    
    win_prob = (1 - (losing_count / len(d))) * 100
    winning_probability_label.config(text=f"Winning Probability: {win_prob:.2f}%", font=("Times New Roman", 14), fg="white")

# Frames
my_frame = Frame(root, bg="#145201", bd=0)
my_frame.pack(pady=20)

dealer_frame = Frame(my_frame, bd=0, bg="#145201")
dealer_frame.pack(side=TOP, pady=10)

player_frame = Frame(my_frame, bd=0, bg="#145201")
player_frame.pack(side=TOP, pady=40)

# Canvases for cards
dealer_canvas = Canvas(dealer_frame, width=600, height=170, bg="#145201", highlightthickness=0)
dealer_canvas.pack(pady=20)

player_canvas = Canvas(player_frame, width=600, height=170, bg="#145201", highlightthickness=0)
player_canvas.pack(pady=20)

# Result Label
result_label = Label(root, text="", font=("Times New Roman", 16), bg="#145201", fg="white")
result_label.pack(pady=10)

# Winning Probability Label
winning_probability_label = Label(root, text="", font=("Times New Roman", 14), bg="#145201", fg="white")
winning_probability_label.pack(pady=10)

# Buttons
probability_button = Button(text="Winning Probability", font=("Times New Roman", 14), command=calculate_winning_probability)
probability_button.place(x=680, y=500)

shuffle_button = Button(text="Shuffle Deck", font=("Times New Roman", 14), command=shuffle_deck)
shuffle_button.place(x=650, y=600)

deal_button = Button(text="Deal", font=("Times New Roman", 14), command=deal_cards)
deal_button.place(x=650, y=550)

hit_button = Button(text="Hit", font=("Times New Roman", 14), command=hit)
hit_button.place(x=800, y=550)

stay_button = Button(text="Stay", font=("Times New Roman", 14), command=stay)
stay_button.place(x=800, y=600)

root.mainloop()
