import pandas as pd
from otree.api import *
from random import shuffle

c = cu

doc = "We create matching markets based on the preferences of university modules"

class C(BaseConstants):
    NAME_IN_URL = "module_matching"
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    NUM_QUESTIONS = 2
    BID_MIN = cu(0)
    BID_MAX = cu(100)
    PRIO_MIN = cu(1)
    PRIO_MAX = cu(4)
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
    # Preferences
    module_1_amount = models.CurrencyField(doc="Preference of module 1 in points", label="module 1 amount")
    module_2_amount = models.CurrencyField(doc="Preference of module 2 in points", label="module 2 amount")
    module_3_amount = models.CurrencyField(doc="Preference of module 3 in points", label="module 3 amount")
    module_4_amount = models.CurrencyField(doc="Preference of module 4 in points", label="module 4 amount")
    # Points
    module_1_value = models.CurrencyField(label="module_1 Value",initial=0, max=C.BID_MAX, min=C.BID_MIN)
    module_2_value = models.CurrencyField(label="module_2 Value",initial=0, max=C.BID_MAX, min=C.BID_MIN)
    module_3_value = models.CurrencyField(label="module_3 Value",initial=0, max=C.BID_MAX, min=C.BID_MIN)
    module_4_value = models.CurrencyField(label="module_4 Value",initial=0, max=C.BID_MAX, min=C.BID_MIN)
    # Priorities
    module_1_priority = models.CurrencyField(label="module_1 Priority",initial=0, max=C.PRIO_MAX, min=C.PRIO_MIN)
    module_2_priority = models.CurrencyField(label="module_2 Priority",initial=0, max=C.PRIO_MAX, min=C.PRIO_MIN)
    module_3_priority = models.CurrencyField(label="module_3 Priority",initial=0, max=C.PRIO_MAX, min=C.PRIO_MIN)
    module_4_priority = models.CurrencyField(label="module_4 Priority",initial=0, max=C.PRIO_MAX, min=C.PRIO_MIN)
    # Results
    WPM1 = models.StringField()
    WPM2 = models.StringField()
    value = models.CurrencyField()
    bid = models.CurrencyField()

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

def get_wpms(group: Group):

    # Spielerpräferenzen in DataFrame umwandeln
    player_value_list = []
    for player in group.get_players():
        player_dict = {
            "module_1": player.module_1_amount,
            "module_2": player.module_2_amount,
            "module_3": player.module_3_amount,
            "module_4": player.module_4_amount,
            }
        player_value_list.append(player_dict)
    df_value = pd.DataFrame(player_value_list)
    
    # Neuen Index
    new_index = ["P1","P2","P3","P4"]

    # DataFrame Index mit Strings ersetzen
    df_value.set_index(pd.Index(new_index), inplace=True)
    
    # Spielergebote/prioritäten in DataFrame umwandeln
    player_list = []
    if group.treatment == True:
        for player in group.get_players():
            player_dict = {
                "module_1": player.module_1_value,
                "module_2": player.module_2_value,
                "module_3": player.module_3_value,
                "module_4": player.module_4_value,
                }
            player_list.append(player_dict)
    if group.treatment == False:
        for player in group.get_players():
            player_dict = {
                "module_1": player.module_1_priority,
                "module_2": player.module_2_priority,
                "module_3": player.module_3_priority,
                "module_4": player.module_4_priority,
                }
            player_list.append(player_dict)
            
    df = pd.DataFrame(player_list)
    
    # DataFrame Index mit Strings ersetzen
    df.set_index(pd.Index(new_index), inplace=True)

    # Neuen DataFrame Output definieren
    df_output = pd.DataFrame({"P1":["","",0,0],"P2":["","",0,0],"P3":["","",0,0],"P4":["","",0,0]})

    # Zeilen- und Spaltenzähler initialisieren
    row_count = {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
    col_count = {"module_1": 0, "module_2": 0, "module_3": 0, "module_4": 0}

    # DataFrame sortieren
    df_sorted = df.stack().sort_values(ascending=False).reset_index()
    
    
    # Präferenzen Wert zu DataFrame_Sorted hinzufügen        
    for i in df_sorted.index:
        print(i)
        df_sorted.loc[i,1] = df_value.loc[df_sorted.loc[i,"level_0"],df_sorted.loc[i,"level_1"]]


    # Füllung des Output DataFrames mit WPM1, WPM2 und Gesamtnutzen und Gebote/Prioritäten
    for index, row in df_sorted.iterrows():
        if row_count[row["level_0"]] < 2 and col_count[row["level_1"]] < 2:
            print("Zeile:", row["level_0"], ", Spalte:", row["level_1"], ", Wert:", row[0], "Nutzen: ", row[1])
            print( row_count[row["level_0"]])
            
            if row["level_0"] == "P1":
                df_output["P1"].iloc[row_count[row["level_0"]]] = row["level_1"]
                df_output["P1"].iloc[2] += row[0]
                df_output["P1"].iloc[3] += row[1]
                
            if row["level_0"] == "P2":
                df_output["P2"].iloc[row_count[row["level_0"]]] = row["level_1"]
                df_output["P2"].iloc[2] += row[0]
                df_output["P2"].iloc[3] += row[1]

            if row["level_0"] == "P3":
                df_output["P3"].iloc[row_count[row["level_0"]]] = row["level_1"]
                df_output["P3"].iloc[2] += row[0]
                df_output["P3"].iloc[3] += row[1]

            if row["level_0"] == "P4":
                df_output["P4"].iloc[row_count[row["level_0"]]] = row["level_1"]
                df_output["P4"].iloc[2] += row[0]
                df_output["P4"].iloc[3] += row[1]

            row_count[row["level_0"]] += 1
            col_count[row["level_1"]] += 1
            
            
    
    # Daten zu Spielern hinzufügen
    player_count = 0
    
    for player in group.get_players():
        player.WPM1 = df_output.iloc[0, player_count]
        player.WPM2 = df_output.iloc[1, player_count]
        player.bid = df_output.iloc[2, player_count]
        player.value = df_output.iloc[3, player_count]
        player_count += 1
        print(player_count)

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

    # Variabler Text für Gruppe 1 und 2
    def vars_for_template(player):
        if player.group.treatment == True:
            # Text für Gruppe mit Punkten
            my_text = "Now you have to decide which module you want to take. You can distribute 100 points between the modules. Each elective module can have 2 participants and each participant gets into 2 elective modules. The more points you give to a module, the higher the chance that you will be assigned to it."
        else:
            # Text für Gruppe mit Prioritäten
            my_text = "Now you have to decide which module you want to take. You can give each module a priority from 1 to 4, with 4 being the highest priority. Each elective module can have 2 participants and each participant gets into 2 elective modules. The higher the priority you give to a module, the higher the chance that you will be assigned to it."
    
        return {"my_text": my_text}
    
    # Formfields anhand von Gruppe anzeigen
    def get_form_fields(player):
        if player.group.treatment == True:
            return ["module_1_value", "module_2_value", "module_3_value", "module_4_value"]
        if player.group.treatment == False:
            return ["module_1_priority", "module_2_priority", "module_3_priority", "module_4_priority"]
        
    # Fehlerüberprüfung in Abhängigkeit von der Gruppe auf aufsummierte 100 oder 1 bis 4 Priorität 
    def error_message(player, values):
        # Fehlerüberprüfung 100
        if player.group.treatment == True:
            if values["module_1_value"] + values["module_2_value"] + values["module_3_value"] + values["module_4_value"] != 100:
                return "The numbers must add up to 100"
        # Fehlerüberprüfung 1 bis 4
        if player.group.treatment == False:
            # Eingabe des Spielers in Liste umwandeln
            user_input = [values["module_1_priority"], values["module_2_priority"], values["module_3_priority"], values["module_4_priority"]]
            # Überprüfen ob alle Zahlen von 1 bis 4 enthalten sind
            if set(user_input) != set(range(1, 5)):
                return "Bitte geben Sie jede Zahl von 1 bis 4 nur einmal ein."

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = get_wpms

class Results(Page):
    form_model = "player"
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

page_sequence = [Introduction, Preference_elicitation, PreferenceWaitPage, Analysis, Bid, ResultsWaitPage, Results]