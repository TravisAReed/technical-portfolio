'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

import random
import math
import eval7

class Player(Bot):    
    '''
    A pokerbot.
    '''

                



    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        self.previous_state = 0
        self.pot_beginning_street = 0

        pass

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        self.previous_state = 0
        self.pot_beginning_street = 0
        #my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        #game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        #round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        #my_cards = round_state.hands[active]  # your cards
        #big_blind = bool(active)  # True if you are the big blind
        pass

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        #my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        #street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        #my_cards = previous_state.hands[active]  # your cards
        #opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
        pass

    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot

        ## my work
        if(self.previous_state != street):
            self.pot_beginning_street = my_contribution + opp_contribution

        self.previous_state = street
        

        




        #to check if can see cards in fold
        # return FoldAction()

        # p = 0.7
        p = get_hand_strength(my_cards,board_cards)
        # print()
        # print("P =", p)
        # print("Bot cards", my_cards)
        # print()

        with open('BotHand.txt','w') as file:
            # file.write('\n')
            file.write(f'P = {p}\nBot cards: {my_cards}\nBoard cards: {board_cards}\n')
            file.write('')
            # file.write('\n')


        # if p > 0.5:
        
        
        






        if RaiseAction in legal_actions:
           min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
           min_cost = min_raise - my_pip  # the cost of a minimum bet/raise
           max_cost = max_raise - my_pip  # the cost of a maximum bet/raise
        if RaiseAction in legal_actions:
            if p > 0.5:
                desired_change_in_pot_from_last_street = int(math.ceil(1000*(p-0.5)**2))
                raise_since_beginning_street = my_contribution + opp_contribution - self.pot_beginning_street
                bet = desired_change_in_pot_from_last_street-raise_since_beginning_street

                if bet < 0 and CallAction in legal_actions:
                    return CallAction()
                if bet > max_raise:
                    bet = max_raise
                return RaiseAction(bet)
            else:
                return CheckAction()

                
        if CallAction in legal_actions:
            if random.random() < p and p > 0.5:
                return CallAction()
            elif continue_cost==0:
                return CallAction()
            else:
                return FoldAction()
        
        return CallAction()  # If we can't raise, call if possible

#Alex's p calculation
def get_random_card():
    number = random.choice(["2s","2h","2d","2c","3s","3h","3d","3c","4s","4h","4d","4c","5s","5h","5d","5c","6s","6h","6d","6c","7s","7h","7d","7c","8s","8h","8d","8c","9s","9h","9d","9c","Ts","Th","Tc","Td","Js","Jh","Jd","Jc","Qs","Qh","Qd","Qc","Ks","Kh","Kd","Kc","As","Ah","Ad","Ac"])
    #number = random.choice(["As","Ah","Ad","Ac"])
    return number




def get_hand_strength(handCards,boardCards):
    #new stuff
    wins=0
    loses=0
    for i in range(10):
        netHand = handCards + boardCards

        randomRemainingCenter = []

        #creates random center cards
        for i in range(7-len(netHand)):
            card = get_random_card()
            #checks if card is already in play
            while card in netHand or card in randomRemainingCenter:
                card = get_random_card()
                
            randomRemainingCenter.append(card)
        #randomRemainingCenter now has random cards to top off to 7
        
        netHand = netHand + randomRemainingCenter
        
        
        #netHand now has 7 cards
        
        
        evalNetHand = [eval7.Card(netHand[i]) for i in range(len(netHand))]
        #for i in range(len(netHand)):
        #    evalNetHand.append(eval7.Card(netHand[i]))
        
        for i in range(10):

            randomHand = []
            for i in range(len(handCards)):
                card = get_random_card()
                #checks if card is already in play
                while card in netHand or card in randomHand:
                    card = get_random_card()
                randomHand.append(card)
            randomHand = randomHand + boardCards + randomRemainingCenter

            evalRandomHand = [eval7.Card(randomHand[i]) for i in range(len(randomHand))]

            scorePlayer=1
            scoreOpponent=1
            
            scorePlayer = eval7.evaluate(evalNetHand)
            scoreOpponent = eval7.evaluate(evalRandomHand)
            
            if(scorePlayer > scoreOpponent):
                wins += 1
            else:
                loses += 1


    #end new stuff
    """

    wins=0
    loses=0

    netHand = handCards + boardCards

    randomRemainingCenter = []

    #creates random center cards
    for i in range(7-len(netHand)):
        card = get_random_card()
        #checks if card is already in play
        while card in netHand or card in randomRemainingCenter:
            card = get_random_card()
            
        randomRemainingCenter.append(card)
    #randomRemainingCenter now has random cards to top off to 7
    
    netHand = netHand + randomRemainingCenter
    
    
    #netHand now has 7 cards
    
    
    evalNetHand = [eval7.Card(netHand[i]) for i in range(len(netHand))]
    #for i in range(len(netHand)):
    #    evalNetHand.append(eval7.Card(netHand[i]))
    
    for i in range(100):

        randomHand = []
        for i in range(len(handCards)):
            card = get_random_card()
            #checks if card is already in play
            while card in netHand or card in randomHand:
                card = get_random_card()
            randomHand.append(card)
        randomHand = randomHand + boardCards + randomRemainingCenter

        evalRandomHand = [eval7.Card(randomHand[i]) for i in range(len(randomHand))]

        scorePlayer=1
        scoreOpponent=1
        
        scorePlayer = eval7.evaluate(evalNetHand)
        scoreOpponent = eval7.evaluate(evalRandomHand)
        
        if(scorePlayer > scoreOpponent):
            wins += 1
        else:
            loses += 1

    if(loses ==0):
        loses = 1
    """
    return wins/(loses+wins)








if __name__ == '__main__':
    run_bot(Player(), parse_args())
