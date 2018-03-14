from Tkinter import *
import simpleguitk
import random
import sys
import time

CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simpleguitk.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simpleguitk.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

in_play = False
display_screen = ""
Total_Money = 1000
Buy_in = 100
cover = 1

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
    def get_rank(self):
        return self.rank
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    def get_suit(self):
        return self.suit

class Hand:

    def __init__(self):
        self.cards = []
    def __str__(self):
        s = "Cards in hand: "
        for i in self.cards:
            s = s + str(i) + " "
        return s
    def get_value(self):
        value = 0
        isAcePresent = False
        for i in self.cards:
            value = value + VALUES[i.get_rank()]
            if value == 1:
                isAcePresent = True
        if (isAcePresent) and ((value + 10) <= 21):
            value = value + 10
        return value
    def add_card(self, card):
        self.cards.append(card)
    def draw(self, canvas, pos):
        j = 0
        for i in self.cards:
            i.draw(canvas, [(pos[0] + (j * 80)), pos[1]])
            j = j + 1

class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
    def shuffle(self):
        random.shuffle(self.cards)
    def deal_card(self):
        return self.cards.pop()
    def __str__(self):
        s = "Cards in deck: "
        for i in self.cards:
            s = s + str(i) + " "
        return s

def deal():
    global display_screen, in_play, Buy_in, card, deck, hand, dealer, cover, Total_Money
    Buy_in = 100
    if in_play:
            in_play = False
            display_screen = "Surrender ..."
            cover = 0
            if Total_Money == 0:
                Buy_in = 0
                display_screen = "Chips over ...no more games now ... see ya next time "
            else:
                Total_Money = Total_Money - ( Buy_in / 2 )
    else:
            if Total_Money == 0:
                Buy_in = 0
                display_screen = "Chips over ...no more games now ... see ya next time "
            else:
                new_deck = Deck()
                new_hand = Hand()
                new_dealer = Hand()
                deck = new_deck
                hand = new_hand
                dealer = new_dealer
                deck.shuffle()
                hand.add_card(deck.deal_card())
                hand.add_card(deck.deal_card())
                dealer.add_card(deck.deal_card())
                dealer.add_card(deck.deal_card())
                cover = 1
                display_screen = "Go for HIT or STAND ???"
                in_play = True

def hit():
    global display_screen, in_play, Buy_in, card, deck, hand, dealer, cover, Total_Money
    if in_play:
        card = deck.deal_card()
        hand.add_card(card)
   
        if hand.get_value() > 21:
            in_play = False
            display_screen = "Busted ...!! you Lose.......New Game ????"
            cover = 0
            Total_Money = Total_Money - Buy_in
def stand():
    global display_screen, in_play, Buy_in, card, deck, hand, dealer, cover, Total_Money
    if in_play:
        cover = 0
        while dealer.get_value() < 17:
            card = deck.deal_card()
            dealer.add_card(card)
        if dealer.get_value() > 21:
            display_screen = "Yayyyy dealer busted !!! you Win !!! New Game ?!!!"
            in_play = False
            Total_Money = Total_Money + Buy_in
        else:
            if dealer.get_value() > hand.get_value():
                display_screen = "Lose.......New Game ????"
                in_play = False
                Total_Money = Total_Money - Buy_in
            elif dealer.get_value() == hand.get_value():
                display_screen = "its Draw...New Game ????"
                in_play = False
            else:
                display_screen = "Yayyyy !!! Win !!! New Game !!!"
                in_play = False
                Total_Money = Total_Money + Buy_in
def dd():
    global display_screen, in_play, Buy_in, card, deck, hand, dealer, cover, Total_Money
    if Buy_in > Total_Money:
            display_screen = "You can't do double down!!!"
            in_play = False
		
    else:
            Buy_in = Buy_in * 2
            hit()
            stand()
			
def draw(canvas):

    global display_screen, in_play, Buy_in, card, deck, hand, dealer, cover, Total_Money
    canvas.draw_text("Blackjack", (210, 70), 48, 'Black')
    canvas.draw_text("Chips: " + str(Buy_in), (50, 110), 32, 'Black')
    canvas.draw_text("Balance: " + str(Total_Money), (50, 155), 32, 'Black')
    canvas.draw_text("Dealer:", (250, 195), 32, 'Black')
    canvas.draw_text("Player:", (250, 390), 32, 'Black')
    dealer.draw(canvas, [100, 210])
    hand.draw(canvas, [100, 420])
    canvas.draw_text(display_screen, (150, 580), 32, 'Black')

    if cover == 1:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [136.5, 259], CARD_SIZE)
frame = simpleguitk.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Red")
card = Card("S", "A")
deck = Deck()
hand = Hand()
dealer = Hand()
frame.add_button("Deal / Surrender ", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Double Down", dd, 200)
frame.set_draw_handler(draw)
deal()
frame.start()