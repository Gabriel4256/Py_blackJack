suits = ('Heart', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
value = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
game = None

import random

class Game:
    def __init__(self):
        self.players = []
        self.dealer = Dealer(self)
        self.turn = 0
        self.deck = Deck()

    def reset(self):
        self.dealer = Dealer(self)
        self.turn = 0
        self.deck = Deck()

    def add_player(self, player):
        self.players.append(player)

    def start_game(self):
        self.deck.shuffle()

    def deal(self):
        participants = list(self.players)
        participants.append(self.dealer)
        self.deck.deal(participants)

    def end_turn(self):
        self.turn+=1     

    def find_winner_and_loser(self):
        if self.dealer.is_busted:
            print('everybody except who are busted are all winner!!!')
            for player in self.players:
                if player.is_busted:
                    self.lose(player)
                else:
                    self.win(player)
        else:
            dealer_sum = self.dealer.get_sum()
            for player in self.players:
                if player.is_busted:
                    self.lose(player)
                else:
                    if player.get_sum() > dealer_sum:
                        self.win(player)
                    elif player.get_sum() is dealer_sum:
                        self.draw(player)
                    else:
                        self.lose(player)  

    def win(self,player):
        player.adjust_chips(player.bet_money)
        print(f'player {player.name} won!!')

    def draw(self, player):
        print(f'player {player.name} drew!!')

    def lose(self, player):
        player.adjust_chips(-1* player.bet_money)
        print(f'player {player.name} lost!!')

class Participant:
    '''
    interface for player & dealer
    '''
    def __init__(self, game):
        self.game = game
        self.hand = Hand()
        self.is_busted = False

    def reset(self):
        self.hand = Hand()
        self.is_busted = False

    def get_sum(self):
        return self.hand.sum

    def bust(self):
        self.is_busted = True

    def show(self):
        raise NotImplementedError('subclass must implement this method')


class Player(Participant):
    def __init__(self, name, game):
        Participant.__init__(self, game)
        self.name = name
        self.chips = 100
        self.bet_money = 0

    def hit(self, deck):
        new_card = deck.draw()
        self.hand.add_card(new_card)
        print(f'{self.name} got {new_card} !!!')
        print(f'now sum is {self.hand.sum}')
        if self.hand.sum > 21:
            self.bust()

    def stand(self):
        self.game.end_turn()

    def show(self):
        print(f"player {self.name}'s cards: '")
        for card in self.hand.cards:
            print(f"{card}")

    def adjust_chips(self,amount):
        self.chips+=amount

    def bet(self,amount):
        self.bet_money = amount

class Dealer(Participant):
    def __init__(self, game):
        Participant.__init__(self, game)
        self.name = 'Dealer'

    def show(self):
        print(f'dealer\'s card: {self.hand.cards[0]}')

    def hit_until_objective(self, deck):
        while self.hand.sum < 17:
            new_card = deck.draw()
            self.hand.add_card(new_card)
            print(f'dealer got {new_card}')
            print(f'now sum is {self.hand.sum}')
            if self.hand.sum > 21:
                self.bust()
                print('dealer busted')

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop()

    def deal(self, participants):
        for participant in participants:
            for i in range(0,2):
                participant.hand.add_card(self.draw())

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.suit} {self.rank}'
  

class Hand:
    '''
    Store info about cards in the hand
    '''
    def __init__(self):
        self.cards = []
        self.sum = 0
        self.aces_of_11 = 0

    def add_card(self, card):
        self.cards.append(card)
        if card.rank is 'Ace':
            if self.sum > 10:
                self.sum += 1
            else:
                self.sum+=11
                self.aces_of_11 += 1
        else:
            self.sum+=value[card.rank]

        if self.sum > 21:
            if self.aces_of_11 > 0:
                self.sum-=10
                self.aces_of_11=0

def hit_or_stand(player):
    while True:
        res = input(f'what do you wanna do {player.name}?\nhit:type 1\nstand: type 2\n')
        if res is '1':
            player.hit(game.deck)
            if player.get_sum() > 21:
                print('you busted!!, you lose')
                player.bust()
                break
            
        elif res is '2':
            player.stand()
            print('You chose stand, turn ended')
            break

player1 = None
while True:
    print('Welcome to the BlackJack Table')

    if game is None:
        game = Game();
        player_num = int(input('How many players are there?'))
        for i in range(0, player_num):
            name = input(f'player{i+1}, what\'s your name?')
            game.add_player(Player(name, game))
    res = input('if you wanna play a game, type \'yes\' if not, type \'no\'\n')

    if res == 'yes':
        '''
        Let's start a game
        set deck
        '''

        game.reset()
        for player in game.players:
            player.reset()
            print(f'it\'s {player.name}\'s turn')
            print(f'you have {player.chips} chips')
            bet_money = int(input('how much do you wanna bet?'))
            player.bet(bet_money)

        game.start_game()
        game.deal()
        
        game.dealer.show()

        for player in game.players:
            player.show()

        while game.turn < len(game.players):
            print(f'player {game.players[game.turn].name}\'s turn!!')
            hit_or_stand(game.players[game.turn])
            game.end_turn()

        print('dealer\'s turn!!')
        print(f'now sum is {game.dealer.get_sum()}')
        game.dealer.hit_until_objective(game.deck)
        game.find_winner_and_loser()

    elif res is 'no':
        print('Game will be quited')
        break
    
    else: 
        print('Type valid answer!!')
            
        


    
