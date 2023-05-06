from otree.api import *
c = cu

doc = '\nIn a common value auction game, players simultaneously bid on the item being\nauctioned.<br/>\nPrior to bidding, they are given an estimate of the actual value of the item.\nThis actual value is revealed after the bidding.<br/>\nBids are private. The player with the highest bid wins the auction, but\npayoff depends on the bid amount and the actual value.<br/>\n'

class C(BaseConstants):
    NAME_IN_URL = 'common_value_auction'
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

def generate_value_estimate(group: Group):
    import random
    group.item_value = 1
    estimate = group.item_value + random.uniform(
        -C.BID_NOISE, C.BID_NOISE
    )
    estimate = round(estimate, 1)
    if estimate < C.BID_MIN:
        estimate = C.BID_MIN
    if estimate > C.BID_MAX:
        estimate = C.BID_MAX
    return estimate

def set_winner(group: Group):
    import random
    
    players = group.get_players()
    group.highest_bid = max([p.bid_amount for p in players])
    players_with_highest_bid = [p for p in players if p.bid_amount == group.highest_bid]
    winner = random.choice(
        players_with_highest_bid
    )  # if tie, winner is chosen at random
    winner.is_winner = True
    for p in players:
        set_payoff(p)

class Player(BasePlayer):
    item_value_estimate = models.CurrencyField(doc='Estimate of the common value may be different for each player')
    bid_amount = models.CurrencyField(doc='Amount bidded by the player', label='Bid amount', max=C.BID_MAX, min=C.BID_MIN)
    module_1_amount = models.CurrencyField(doc="Preference of module 1 in points", label="module 1 amount")
    module_2_amount = models.CurrencyField(doc="Preference of module 2 in points", label="module 2 amount")
    module_3_amount = models.CurrencyField(doc="Preference of module 3 in points", label="module 3 amount")
    module_4_amount = models.CurrencyField(doc="Preference of module 4 in points", label="module 4 amount")

def set_payoff(player: Player):
    group = player.group
    if player.is_winner:
        player.payoff = group.item_value - player.bid_amount
        if player.payoff < 0:
            player.payoff = 0
    else:
        player.payoff = 0

class Introduction(Page):
    form_model = 'player'
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group
        player.item_value_estimate = generate_value_estimate(group)

class Preference_elicitation(Page):
    form_model = 'player'
    form_fields = ["module_1_amount", "module_2_amount", "module_3_amount", "module_4_amount"]

class PreferenceWaitPage(WaitPage):
    after_all_players_arrive = set_winner

class Analysis(Page):
    form_model = "player"

class Bid(Page):
    form_model = "player"

class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(is_greedy=group.item_value - player.bid_amount < 0)

page_sequence = [Introduction, Preference_elicitation, PreferenceWaitPage, Analysis, Bid, Results]