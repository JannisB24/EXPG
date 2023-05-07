from otree.api import *
c = cu

doc = "We create matching markets based on the preferences of university modules"

class C(BaseConstants):
    NAME_IN_URL = "module_matching"
    PLAYERS_PER_GROUP = 4
    PLAYERS = 4
    NUM_ROUNDS = 1
    BID_MIN = cu(0)
    BID_MAX = cu(100)
    BID_NOISE = cu(0)
    INSTRUCTIONS_TEMPLATE = "module_matching/instructions.html"

class Subsession(BaseSubsession):
    pass

#def creating_session(subsession: Subsession):
#    session = subsession.sessionplayer
#    for g in subsession.get_groups():
#        import random

class Group(BaseGroup):
    avg_module_1  = models.CurrencyField(doc="total points allocated to module 1")
    avg_module_2  = models.CurrencyField(doc="total points allocated to module 2")
    avg_module_3  = models.CurrencyField(doc="total points allocated to module 3")
    avg_module_4  = models.CurrencyField(doc="total points allocated to module 4")

class Player(BasePlayer):
    module_1_amount = models.CurrencyField(doc="Preference of module 1 in points", label="module 1 amount")
    module_2_amount = models.CurrencyField(doc="Preference of module 2 in points", label="module 2 amount")
    module_3_amount = models.CurrencyField(doc="Preference of module 3 in points", label="module 3 amount")
    module_4_amount = models.CurrencyField(doc="Preference of module 4 in points", label="module 4 amount")

# Altlast (haben noch keine Payoff Dynamik, diese basiert auf den Punkten)
def set_payoffs(group):
    for p in group.get_players():
        p.payoff = 100

# hier berechnen wir den Durchschnitt über alle Spieler (theoretisch müssten wir die aber über die anderen 3 Spieler berechnen)
def avg_modules(group: Group):
    players = group.get_players()
    module_1_allocations = [p.module_1_amount for p in players]
    group.avg_module_1 = sum(module_1_allocations) / 4
    module_2_allocations = [p.module_2_amount for p in players]
    group.avg_module_2 = sum(module_2_allocations) / 4
    module_3_allocations = [p.module_3_amount for p in players]
    group.avg_module_3 = sum(module_3_allocations) / 4
    module_4_allocations = [p.module_4_amount for p in players]
    group.avg_module_4 = sum(module_4_allocations) / 4
        
class Introduction(Page):
    form_model = "player"

class Preference_elicitation(Page):
    form_model = "player"
    form_fields = ["module_1_amount", "module_2_amount", "module_3_amount", "module_4_amount"]

    # field validation
    @staticmethod
    def error_message(player, values):
        print("values is", values)
        if values["module_1_amount"] + values["module_2_amount"] + values["module_3_amount"] + values["module_4_amount"] != 100:
            return "The numbers must add up to 100"

class PreferenceWaitPage(WaitPage):
    after_all_players_arrive = avg_modules

class Analysis(Page):
    def calculating_avg(subsession):
        players = subsession.get_others_in_subsession()
        avg_module_1 = [p.module_1_amount for p in players]
        print(avg_module_1)

class Bid(Page):
    form_model = "player"

class Results(Page):
    form_model = "player"

page_sequence = [Introduction, Preference_elicitation, PreferenceWaitPage, Analysis, Bid, Results]