import pandas as pd
from otree.api import *
import random
from django import forms
import matplotlib.pyplot as plt




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
    MODULE_1 = "Monetary policy"
    MODULE_2 = "Brand management"
    MODULE_3 = "Financial analysis"
    MODULE_4 = "History of economic ethics"

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
    prio_1_module_1  = models.IntegerField(doc="amount of participants who choose Monetary policy as priority 1", initial=0)
    prio_1_module_2  = models.IntegerField(doc="amount of participants who choose Brand management as priority 1", initial=0)
    prio_1_module_3  = models.IntegerField(doc="amount of participants who choose Financial analysis as priority 1", initial=0)
    prio_1_module_4  = models.IntegerField(doc="amount of participants who choose History of economic ethics as priority 1", initial=0)
    treatment = models.BooleanField()
     

################################
######### Class Player #########
################################

class Player(BasePlayer):
    
    # Dropdown 1-4 Prios für beide Gruppen Nr. 1
    
    prio_module_1_1 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority monetary policy"
    )
    prio_module_2_1 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority brand management"
    )
    prio_module_3_1 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority financial analysis"
    )
    prio_module_4_1 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority history of economic ethics"
    )
    
    
    # Dropdown 1-4 Prios für beide Gruppen Nr. 2
    
    prio_module_1_2 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority monetary policy"
    )
    prio_module_2_2 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority brand management"
    )
    prio_module_3_2 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority financial analysis"
    )
    prio_module_4_2 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority history of economic ethics"
    )


    # Points
    module_1_points = models.CurrencyField(doc="Points for monetary policy", label="Points for monetary policy", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    module_2_points = models.CurrencyField(doc="Points for brand management", label="Points for brand management", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    module_3_points = models.CurrencyField(doc="Points for financial analysis", label="Points for financial analysis", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    module_4_points = models.CurrencyField(doc="Points for history of economic ethics", label="Points for history of economic ethics", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    
     
    # Results
    WPM1 = models.StringField()
    WPM2 = models.StringField()
    Favs = models.IntegerField()
    Rank = models.StringField()
    Happiness = models.IntegerField(label="How happy are you with your Results from 1-10 with 10 being the happiest:", widget=widgets.RadioSelect,choices=[(i, i) for i in range(1, 11)])
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


    #################################
    ## Hier Barplot Werte einfügen ##
    #################################
def create_barplot():
    labels = ['Monetary Policy', 'Brand Management', 'Financial Analysis', 'History of Economic Ethics']
    values = [50, 30, 15, 5]
    colors = ['#F9B5AC', '#F9D9AD', '#B5EAD7', '#C7CEEA']
    
    plt.bar(labels, values, color = colors)
    plt.xlabel('Courses')
    plt.ylabel('Points')
    plt.title('Barplot Diagram')
    plt.xticks(fontsize=7)
    plt.savefig("_static/barplot.png")
    print("Barplot erstellt und abgespeichert")



def get_wpms(group: Group):

    ################################
    ##### Spieler Prio 1 in DF #####
    ################################
    player_prio_1_list = []
    for player in group.get_players():
        player_dict = {
            "monetary policy": player.prio_module_1_1,
            "brand management": player.prio_module_2_1,
            "financial analysis": player.prio_module_3_1,
            "history of economic ethics": player.prio_module_4_1,
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
            "monetary policy": player.prio_module_1_2,
            "brand management": player.prio_module_2_2,
            "financial analysis": player.prio_module_3_2,
            "history of economic ethics": player.prio_module_4_2,
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
                "monetary policy": player.module_1_points,
                "brand management": player.module_2_points,
                "financial analysis": player.module_3_points,
                "history of economic ethics": player.module_4_points,
                }
        if player.group.treatment == False:
            player_dict = {
                "monetary policy": None,
                "brand management": None,
                "financial analysis": None,
                "history of economic ethics": None,
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
    col_count = {"monetary policy": 0, "brand management": 0, "financial analysis": 0, "history of economic ethics": 0}

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
        
        
    for player in group.get_players():
        if player.Favs == 2:
            player.Rank = "Congratulations, they got both of their desired modules. You have made it to the first place"
        if player.Favs == 1:
            player.Rank = "You have received one of your desired modules. With this you occupy the second place"
        if player.Favs == 0:
            player.Rank = "Unfortunately, you didn't get any of the modules you wanted. Unfortunately you occupy the last place"


###############################################################################
############################   PAGES   ########################################
############################################################################### 





class Introduction(Page):
    form_model = "player"

class Preference_elicitation(Page):
    form_model = "player"
    form_fields = ["prio_module_1_1", "prio_module_2_1", "prio_module_3_1", "prio_module_4_1"]
    
    create_barplot()
    
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
            my_text = "Now you're in competitition with your group members.<br>The goal is to enroll into your two favourite modules, while there are only two seats available per module (e.g. if everyone fancies the same module, only two are able to enroll). <br>Initially you ranked all modules from priority 1-4. You can see an overview of your choices in the box above. These preferences determine your payoff in the end of the experiment. <br> <br>Now you can again state priorities and also have 100 bidding points available, to get the modules you desire. <br> <br>The bidding process works as follows: <br>- Initially, students are ordered by their preferences over the modules <br>- Only if there are more applicants than capacity for a module, the bidding comes into play <br>- Among people with the same priority, the highest bids win seats in the module <br>- For the small probability that students have the same priority and equal bids, the winner is taken by chance<br> <br>In the textbox above there are assumptions for lowest bids that would have got you into these modules in prior years (market-clearing prices)."
        else:
            # Text für Gruppe mit Prioritäten
            my_text = "Now you have to decide which module you want to take. You can give each module a priority from 1 to 4, with 1 being the highest priority. Each elective module can have 2 participants and each participant gets into 2 elective modules. The higher the priority you give to a module, the higher the chance that you will be assigned to it."
    
        return {"my_text": my_text}
    
    # Formfields anhand von Gruppe anzeigen
    def get_form_fields(player):
        form_fields = ["prio_module_1_2", "prio_module_2_2", "prio_module_3_2", "prio_module_4_2"]
        random.shuffle(form_fields)

        if player.group.treatment == True:
            more_form_fields = ["module_1_points", "module_2_points", "module_3_points", "module_4_points"]
            random.shuffle(more_form_fields)
            form_fields += more_form_fields

        return form_fields
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
    def clean(player):
        if player.Happiness is None:
            raise models.ValidationError('Please select a value for Happiness.')

class End(Page):
    form_model = "player"
page_sequence = [Introduction, Preference_elicitation, PreferenceWaitPage, Bid, ResultsWaitPage, Results, End]