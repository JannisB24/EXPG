import pandas as pd
from otree.api import *
from random import shuffle
import random



c = cu

doc = "We create matching markets based on the preferences of university modules"


###############################################################################
############################   Classes   ######################################
############################################################################### 
 


class C(BaseConstants):
    NAME_IN_URL = "module_matching"
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    BID_MIN = cu(0)
    BID_MAX = cu(100)
    INSTRUCTIONS_TEMPLATE = "module_matching/instructions.html"

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    import itertools
    treatments = itertools.cycle([True, False])
    for group in subsession.get_groups():
        group.treatment = next(treatments)
      
        
################################
######### Class Group ##########
################################

class Group(BaseGroup):
    prio_1_module_1  = models.IntegerField(doc="amount of participants who choose module 1 as priority 1", initial=0)
    prio_1_module_2  = models.IntegerField(doc="amount of participants who choose module 2 as priority 1", initial=0)
    prio_1_module_3  = models.IntegerField(doc="amount of participants who choose module 3 as priority 1", initial=0)
    prio_1_module_4  = models.IntegerField(doc="amount of participants who choose module 4 as priority 1", initial=0)
    treatment = models.BooleanField()
    

################################
######### Class Player #########
################################

class Player(BasePlayer):
    
    # Dropdown 1-4 Prios für beide Gruppen Nr. 1
    
    prio_module_1_1 = models.IntegerField(
        choices=[('1', 1),('2', 2),('3', 3),('4', 4),],
        verbose_name='Priorität Module 1'
    )
    prio_module_2_1 = models.IntegerField(
        choices=[('1', 1),('2', 2),('3', 3),('4', 4),],
        verbose_name='Priorität Module 2'
    )
    prio_module_3_1 = models.IntegerField(
        choices=[('1', 1),('2', 2),('3', 3),('4', 4),],
        verbose_name='Priorität Module 3'
    )
    prio_module_4_1 = models.IntegerField(
        choices=[('1', 1),('2', 2),('3', 3),('4', 4),],
        verbose_name='Priorität Module 4'
    )
    
    
    # Dropdown 1-4 Prios für beide Gruppen Nr. 2
    
    prio_module_1_2 = models.IntegerField(
        choices=[('1', 1),('2', 2),('3', 3),('4', 4),],
        verbose_name='Priorität Module 1'
    )
    prio_module_2_2 = models.IntegerField(
        choices=[('1', 1),('2', 2),('3', 3),('4', 4),],
        verbose_name='Priorität Module 2'
    )
    prio_module_3_2 = models.IntegerField(
        choices=[('1', 1),('2', 2),('3', 3),('4', 4),],
        verbose_name='Priorität Module 3'
    )
    prio_module_4_2 = models.IntegerField(
        choices=[('1', 1),('2', 2),('3', 3),('4', 4),],
        verbose_name='Priorität Module 4'
    )


    # Points
    module_1_points = models.CurrencyField(doc="Points for module 1", label="Points for module 1", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    module_2_points = models.CurrencyField(doc="Points for module 2", label="Points for module 2", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    module_3_points = models.CurrencyField(doc="Points for module 3", label="Points for module 3", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    module_4_points = models.CurrencyField(doc="Points for module 4", label="Points for module 4", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    
     
    # Results
    WPM1 = models.StringField()
    WPM2 = models.StringField()
    Favs = models.IntegerField()
    Happiness = models.IntegerField(choices=[('1', 1),('2', 2),('3', 3),('4', 4),('5', 5),('6', 6),('7', 7),('8', 8),('9', 9),('10', 10),],
    verbose_name='How satisfied are you with your Results?')
    Notes = models.TextField()

    

###############################################################################
############################   Functions   ####################################
############################################################################### 
    
    

# Altlast (haben noch keine Payoff Dynamik, diese basiert auf den Punkten)
def set_payoffs(group):
    for p in group.get_players():
        p.payoff = 100

# hier berechnen wir den Durchschnitt über alle Spieler (theoretisch müssten wir die aber über die anderen 3 Spieler berechnen)
def prio_1_modules(group: Group):
    players = group.get_players()
    
    for p in players:
        if p.prio_module_1_1 == 1:
            group.prio_1_module_1 += 1
        if p.prio_module_2_1 == 1:
            group.prio_1_module_2 += 1
        if p.prio_module_3_1 == 1:
            group.prio_1_module_3 += 1
        if p.prio_module_4_1 == 1:
            group.prio_1_module_4 += 1

def get_wpms(group: Group):

    ################################
    ##### Spieler Prio 1 in DF #####
    ################################
    player_prio_1_list = []
    for player in group.get_players():
        player_dict = {
            "module_1": player.prio_module_1_1,
            "module_2": player.prio_module_2_1,
            "module_3": player.prio_module_3_1,
            "module_4": player.prio_module_4_1,
            }
        player_prio_1_list.append(player_dict)
    df_prio_1 = pd.DataFrame(player_prio_1_list)
    
    # Neuen Index
    new_index = ["P1","P2","P3","P4"]

    # DataFrame Index mit Strings ersetzen
    df_prio_1.set_index(pd.Index(new_index), inplace=True)
    
    
    ################################
    ##### Spieler Prio 2 in DF #####
    ################################
    player_prio_2_list = []
    for player in group.get_players():
        player_dict = {
            "module_1": player.prio_module_1_2,
            "module_2": player.prio_module_2_2,
            "module_3": player.prio_module_3_2,
            "module_4": player.prio_module_4_2,
            }
        player_prio_2_list.append(player_dict)
    df_prio_2 = pd.DataFrame(player_prio_2_list)

    # DataFrame Index mit Strings ersetzen
    df_prio_2.set_index(pd.Index(new_index), inplace=True)


    ################################
    ##### Spieler Punkte in DF #####
    ################################    
    player_points_list = []
    for player in group.get_players():
        if player.group.treatment == True:
            player_dict = {
                "module_1": player.module_1_points,
                "module_2": player.module_2_points,
                "module_3": player.module_3_points,
                "module_4": player.module_4_points,
                }
        if player.group.treatment == False:
            player_dict = {
                "module_1": None,
                "module_2": None,
                "module_3": None,
                "module_4": None,
                }
            available_numbers = [1, 2, 3, 4]
            for key in player_dict.keys():
                random_number = random.choice(available_numbers)
                player_dict[key] = random_number
                available_numbers.remove(random_number)
        player_points_list.append(player_dict)
    df_points = pd.DataFrame(player_points_list)

    # DataFrame Index mit Strings ersetzen
    df_points.set_index(pd.Index(new_index), inplace=True)


    ################################
    ##### Output DF vorbereiten ####
    ################################  

    # Neuen DataFrame Output definieren
    df_output = pd.DataFrame({"P1":["",""],"P2":["",""],"P3":["",""],"P4":["",""]})

    # Zeilen- und Spaltenzähler initialisieren
    row_count = {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
    col_count = {"module_1": 0, "module_2": 0, "module_3": 0, "module_4": 0}

    # DataFrame sortieren
    df_sorted = df_prio_2.stack().sort_values(ascending=True).reset_index()
    
    
    # Punkte/Lotterie Wert zu DataFrame_Sorted hinzufügen        
    for i in df_sorted.index:
        print(i)
        df_sorted.loc[i,1] = df_points.loc[df_sorted.loc[i,"level_0"],df_sorted.loc[i,"level_1"]]

    df_sorted = df_sorted.sort_values(by=[0, 1], ascending=[True,False]).reset_index()
    

    # Füllung des Output DataFrames mit WPM1, WPM2 und Gesamtnutzen und Gebote/Lotterie
    for index, row in df_sorted.iterrows():
        if row_count[row["level_0"]] < 2 and col_count[row["level_1"]] < 2:
            print("Zeile:", row["level_0"], ", Spalte:", row["level_1"], ", Priorität:", row[0], "Punkte/Player_ID: ", row[1])
            print( row_count[row["level_0"]])
            
            if row["level_0"] == "P1":
                df_output["P1"].iloc[row_count[row["level_0"]]] = row["level_1"]
                
            if row["level_0"] == "P2":
                df_output["P2"].iloc[row_count[row["level_0"]]] = row["level_1"]

            if row["level_0"] == "P3":
                df_output["P3"].iloc[row_count[row["level_0"]]] = row["level_1"]

            if row["level_0"] == "P4":
                df_output["P4"].iloc[row_count[row["level_0"]]] = row["level_1"]

            row_count[row["level_0"]] += 1
            col_count[row["level_1"]] += 1
            
            
    # Daten zu Spielern hinzufügen
    player_count = 0
    
    for player in group.get_players():
        player.WPM1 = df_output.iloc[0, player_count]
        player.WPM2 = df_output.iloc[1, player_count]
        player_count += 1
        print(player_count)


    # Überprüfen ob WPMs unter Favoriten waren
    df_prio_1_sorted = df_prio_1.stack().sort_values(ascending=True).reset_index()
    row_count = {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
    df_output_1 = pd.DataFrame({"P1":["",""],"P2":["",""],"P3":["",""],"P4":["",""]})
    for index, row in df_sorted.iterrows():
        if row_count[row["level_0"]] < 2:
            print("Zeile:", row["level_0"], ", Spalte:", row["level_1"])
            print( row_count[row["level_0"]])
            
            if row["level_0"] == "P1":
                df_output_1["P1"].iloc[row_count[row["level_0"]]] = row["level_1"]
                
            if row["level_0"] == "P2":
                df_output_1["P2"].iloc[row_count[row["level_0"]]] = row["level_1"]

            if row["level_0"] == "P3":
                df_output_1["P3"].iloc[row_count[row["level_0"]]] = row["level_1"]

            if row["level_0"] == "P4":
                df_output_1["P4"].iloc[row_count[row["level_0"]]] = row["level_1"]

            row_count[row["level_0"]] += 1

    common_numbers = []
    for column in df_output.columns:
        common_numbers.append(df_output[column].isin(df_output_1[column]).sum())
        
    print(common_numbers)
    i = 0
    for player in group.get_players():
        player.Favs = int(common_numbers[i])
        i += 1


###############################################################################
############################   PAGES   ########################################
############################################################################### 





class Introduction(Page):
    form_model = "player"

class Preference_elicitation(Page):
    form_model = "player"
    form_fields = ["prio_module_1_1", "prio_module_2_1", "prio_module_3_1", "prio_module_4_1"]
    
    def error_message(player, values):
        # Fehlerüberprüfung 1 bis 4
        user_input = [values["prio_module_1_1"], values["prio_module_2_1"], values["prio_module_3_1"], values["prio_module_4_1"]]
        if set(user_input) != set(range(1, 5)):
            return "Bitte geben Sie jede Zahl von 1 bis 4 nur einmal ein."
    form_model = "player"
    form_fields = ["prio_module_1_1", "prio_module_2_1", "prio_module_3_1", "prio_module_4_1"]
    def error_message(player, values):
        user_input = [values["prio_module_1_1"], values["prio_module_2_1"], values["prio_module_3_1"], values["prio_module_4_1"]]
        if set(user_input) != set(range(1, 5)):
            return "Please select each priority only once"

class PreferenceWaitPage(WaitPage):
    after_all_players_arrive = prio_1_modules

class Bid(Page):
    form_model = "player"

    # Variabler Text für Gruppe 1 und 2
    def vars_for_template(player):
        if player.group.treatment == True:
            # Text für Gruppe mit Punkten
            my_text = "Now you're in competitition with your group members. <br>The bidding process works as follows: <br>- Initially, students are ordered by their preferences over the modules <br>- Only if there are more applicants than capacity for a module, the bidding comes into play <br>- Among people with the same priority, the highest bids win places in the module <br>- For the small probability that students have the same priority and equal bids, the winner is taken by chance"
        else:
            # Text für Gruppe mit Prioritäten
            my_text = "Now you have to decide which module you want to take. You can give each module a priority from 1 to 4, with 1 being the highest priority. Each elective module can have 2 participants and each participant gets into 2 elective modules. The higher the priority you give to a module, the higher the chance that you will be assigned to it."
    
        return {"my_text": my_text}
    
    # Formfields anhand von Gruppe anzeigen
    def get_form_fields(player):
        if player.group.treatment == True:
            return ["prio_module_1_2", "prio_module_2_2", "prio_module_3_2", "prio_module_4_2", "module_4_points", "module_3_points", "module_2_points", "module_1_points"]
        if player.group.treatment == False:
            return ["prio_module_1_2", "prio_module_2_2", "prio_module_3_2", "prio_module_4_2"]
        
    # Fehlerüberprüfung in Abhängigkeit von der Gruppe auf aufsummierte 100 oder 1 bis 4 Priorität 
    def error_message(player, values):
        # Fehlerüberprüfung 1 bis 4 und 100
        if player.group.treatment == True:
            # 100 
            if values["module_1_points"] + values["module_2_points"] + values["module_3_points"] + values["module_4_points"] != 100:
                return "The numbers must add up to 100"
            # 1 bis 4
            user_input = [values["prio_module_1_2"], values["prio_module_2_2"], values["prio_module_3_2"], values["prio_module_4_2"]]
            if set(user_input) != set(range(1, 5)):
                return "Bitte geben Sie jede Zahl von 1 bis 4 nur einmal ein."
        
        # Fehlerüberprüfung 1 bis 4
        if player.group.treatment == False:
            user_input = [values["prio_module_1_2"], values["prio_module_2_2"], values["prio_module_3_2"], values["prio_module_4_2"]]
            if set(user_input) != set(range(1, 5)):
                return "Bitte geben Sie jede Zahl von 1 bis 4 nur einmal ein."


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = get_wpms

class Results(Page):
    form_model = "player"
    form_fields = ["Happiness", "Notes"]
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

class End(Page):
    form_model = "player"
page_sequence = [Introduction, Preference_elicitation, PreferenceWaitPage, Bid, ResultsWaitPage, Results, End]