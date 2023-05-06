from otree.api import *
c = cu

doc = '\nIn a common value auction game, players simultaneously bid on the item being\nauctioned.<br/>\nPrior to bidding, they are given an estimate of the actual value of the item.\nThis actual value is revealed after the bidding.<br/>\nBids are private. The player with the highest bid wins the auction, but\npayoff depends on the bid amount and the actual value.<br/>\n'

class C(BaseConstants):
    NAME_IN_URL = 'common_value_auction'
    PLAYERS = 4
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    BID_MIN = cu(0)
    BID_MAX = cu(100)
    BID_NOISE = cu(0)
    INSTRUCTIONS_TEMPLATE = 'common_value_auction/instructions.html'

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    session = subsession.session
    for g in subsession.get_groups():
        import random

class Group(BaseGroup):
    item_value = models.CurrencyField(doc='Common value of the item to be auctioned random for treatment')
    highest_bid = models.CurrencyField()

def set_payoffs(group):
    for p in group.get_players():
        p.payoff = 100

class Player(BasePlayer):
    module_1_amount = models.CurrencyField(doc="Preference of module 1 in points", label="module 1 amount")
    module_2_amount = models.CurrencyField(doc="Preference of module 2 in points", label="module 2 amount")
    module_3_amount = models.CurrencyField(doc="Preference of module 3 in points", label="module 3 amount")
    module_4_amount = models.CurrencyField(doc="Preference of module 4 in points", label="module 4 amount")
    #hier fehlt die Kontrolle ob die vollen 100 Punkte verteilt wurden (nicht mehr und nicht weniger)

class Introduction(Page):
    form_model = 'player'

class Preference_elicitation(Page):
    form_model = 'player'
    form_fields = ["module_1_amount", "module_2_amount", "module_3_amount", "module_4_amount"]

    @staticmethod
    def error_message(player, values):
        print('values is', values)
        if values['module_1_amount'] + values['module_2_amount'] + values['module_3_amount'] + values["module_4_amount"] != 100:
            return 'The numbers must add up to 100'

class PreferenceWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class Analysis(Page):
    def calculating_avg(subsession):
        players = subsession.get_others_in_subsession()
        avg_module_1 = [p.module_1_amount for p in players]
        print(avg_module_1)

class Bid(Page):
    form_model = "player"

class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(is_greedy=group.item_value - player.bid_amount < 0)

page_sequence = [Introduction, Preference_elicitation, PreferenceWaitPage, Analysis, Bid, Results]