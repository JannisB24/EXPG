import pandas as pd
from otree.api import *
import random
from django import forms
import matplotlib.pyplot as plt


choice1 = [(1,"Goethe"), (2,"Experiment")]
random.shuffle(choice1)
choice2 = [(1,"Goethe"), (2,"Experiment")]
random.shuffle(choice2)
choice3 = [(1,"Goethe"), (2,"Experiment")]
random.shuffle(choice1)
choice4 = [(1,"Goethe"), (2,"Experiment")]
random.shuffle(choice1)
choice5 = [(1,"Goethe"), (2,"Experiment")]
random.shuffle(choice2)

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
    prio_1_monetary_policy  = models.IntegerField(doc="amount of participants who choose Monetary policy as priority 1", initial=0)
    prio_1_brand_management  = models.IntegerField(doc="amount of participants who choose Brand management as priority 1", initial=0)
    prio_1_financial_analysis  = models.IntegerField(doc="amount of participants who choose Financial analysis as priority 1", initial=0)
    prio_1_history_of_economics_ethics  = models.IntegerField(doc="amount of participants who choose History of economic ethics as priority 1", initial=0)
    treatment = models.BooleanField()
     

################################
######### Class Player #########
################################

class Player(BasePlayer):
    
    # Dropdown 1-4 Prios für beide Gruppen Nr. 1
    
    prio_monetary_policy_1 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority monetary policy"
    )
    prio_brand_management_1 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority brand management"
    )
    prio_financial_analysis_1 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority financial analysis"
    )
    prio_history_of_economics_ethics_1 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority history of economic ethics"
    )
    
    
    # Dropdown 1-4 Prios für beide Gruppen Nr. 2
    
    prio_monetary_policy_2 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority monetary policy"
    )
    prio_brand_management_2 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority brand management"
    )
    prio_financial_analysis_2 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority financial analysis"
    )
    prio_history_of_economics_ethics_2 = models.IntegerField(
        choices=[("1", 1),("2", 2),("3", 3),("4", 4),],
        verbose_name="Priority history of economic ethics"
    )


    # Points
    monetary_policy_points = models.CurrencyField(doc="Points for monetary policy", label="Points for monetary policy", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    brand_management_points = models.CurrencyField(doc="Points for brand management", label="Points for brand management", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    financial_analysis_points = models.CurrencyField(doc="Points for financial analysis", label="Points for financial analysis", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    history_of_economics_ethics_points = models.CurrencyField(doc="Points for history of economic ethics", label="Points for history of economic ethics", initial=0, max=C.BID_MAX, min=C.BID_MIN)
    
     
    # Results
    
    WPM1 = models.StringField()
    WPM2 = models.StringField()
    Points = models.IntegerField(initial=0)
    Rank = models.IntegerField(initial=0)
    WhichIsBetter = models.IntegerField(label="Which of the mechanisms do you prefer?", widget=widgets.RadioSelect, choices=choice1)
    Control = models.IntegerField(label="In which mechanism do you feel like you have more control over your module choice?", widget=widgets.RadioSelect, choices=choice2)
    RandomChoice = models.IntegerField(label="Which mechanism exposes you to more randomness?", widget=widgets.RadioSelect, choices=choice3)
    Comfortable = models.IntegerField(label="Which mechanism are you more comfortable in?", widget=widgets.RadioSelect, choices=choice4)
    FinalChoice = models.IntegerField(label="Which mechanism should be implemented in the real world?", widget=widgets.RadioSelect, choices=choice5)
    Winner = models.IntegerField()
    

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
        if p.prio_monetary_policy_1 == 1:
            group.prio_1_monetary_policy += 1
        if p.prio_brand_management_1 == 1:
            group.prio_1_brand_management += 1
        if p.prio_financial_analysis_1 == 1:
            group.prio_1_financial_analysis += 1
        if p.prio_history_of_economics_ethics_1 == 1:
            group.prio_1_history_of_economics_ethics += 1


    #################################
    ## Hier Barplot Werte einfügen ##
    #################################
def create_barplot():
    labels = ['Monetary Policy', 'Brand Management', 'Financial Analysis', 'History of Economic Ethics']
    values = [30, 9, 30, 0]
    colors = ['#F9B5AC', '#F9D9AD', '#B5EAD7', '#C7CEEA']

    fig, ax = plt.subplots()

    bars = ax.bar(labels, values, color=colors)
    ax.set_xlabel('Courses')
    ax.set_ylabel('Points')
    ax.set_title('Barplot Diagram')
    ax.tick_params(axis='x',labelsize=7)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, str(height), ha='center', va='bottom')

    plt.savefig("_static/barplot.png")
    print("Barplot erstellt und abgespeichert")



def get_wpms(group: Group):

    ################################
    ##### Spieler Prio 1 in DF #####
    ################################
    player_prio_1_list = []
    for player in group.get_players():
        player_dict = {
            "monetary policy": player.prio_monetary_policy_1,
            "brand management": player.prio_brand_management_1,
            "financial analysis": player.prio_financial_analysis_1,
            "history of economic ethics": player.prio_history_of_economics_ethics_1,
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
            "monetary policy": player.prio_monetary_policy_2,
            "brand management": player.prio_brand_management_2,
            "financial analysis": player.prio_financial_analysis_2,
            "history of economic ethics": player.prio_history_of_economics_ethics_2,
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
                "monetary policy": player.monetary_policy_points,
                "brand management": player.brand_management_points,
                "financial analysis": player.financial_analysis_points,
                "history of economic ethics": player.history_of_economics_ethics_points,
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
 
        
    for player in group.get_players():
        if player.WPM1 == "monetary policy":
            player.Points += 5 - player.prio_monetary_policy_1
        if player.WPM1 == "brand management":
            player.Points += 5 - player.prio_brand_management_1
        if player.WPM1 == "financial analysis":
            player.Points +=  5 -player.prio_financial_analysis_1
        if player.WPM1 == "history of economic ethics":
            player.Points += 5 - player.prio_history_of_economics_ethics_1
        if player.WPM1 == None:
            player.Points += 0
            
        if player.WPM2 == "monetary policy":
            player.Points += 5 -player.prio_monetary_policy_1
        if player.WPM2 == "brand management":
            player.Points += 5 - player.prio_brand_management_1
        if player.WPM2 == "financial analysis":
            player.Points += 5 - player.prio_financial_analysis_1
        if player.WPM2 == "history of economic ethics":
            player.Points += 5 - player.prio_history_of_economics_ethics_1
        if player.WPM2 == None:
            player.Points += 0
                
    df_rank = {
        "PlayerID": [],
        "Points":   []
        }

    df_rank = pd.DataFrame(df_rank)

    i = 0
    
    for player in group.get_players():
        df_rank.loc[i,"PlayerID"] = player.id_in_group
        df_rank.loc[i,"Points"] = player.Points
        i += 1

    df_rank_sorted = df_rank.sort_values(by="Points", ascending=False)
    
    df_rank_sorted["Rank"] = 0

    current_rank = 1
    current_points = None
    rank_counter = 0

    for index, row in df_rank_sorted.iterrows():
        if row['Points'] != current_points:
            current_rank += rank_counter
            rank_counter = 1
        else:
            rank_counter += 1
        df_rank_sorted.at[index, 'Rank'] = current_rank
        current_points = row['Points']


    for player in group.get_players():
        player.Rank = int(df_rank_sorted.loc[df_rank_sorted["PlayerID"] == player.id_in_group, "Rank"].values[0])


    winner_list = [0,0,0,1]
    random.shuffle(winner_list)
    
    for player in group.get_players():
        player.Winner = winner_list.pop(0)


###############################################################################
############################   PAGES   ########################################
############################################################################### 





class Introduction(Page):
    form_model = "player"

class Preference_elicitation(Page):
    form_model = "player"
    form_fields = ["prio_monetary_policy_1", "prio_brand_management_1", "prio_financial_analysis_1", "prio_history_of_economics_ethics_1"]
    
    create_barplot()
    
    def error_message(player, values):
        # Fehlerüberprüfung 1 bis 4
        user_input = [values["prio_monetary_policy_1"], values["prio_brand_management_1"], values["prio_financial_analysis_1"], values["prio_history_of_economics_ethics_1"]]
        if set(user_input) != set(range(1, 5)):
            return "Bitte geben Sie jede Zahl von 1 bis 4 nur einmal ein."
    form_model = "player"
    form_fields = ["prio_monetary_policy_1", "prio_brand_management_1", "prio_financial_analysis_1", "prio_history_of_economics_ethics_1"]
    def error_message(player, values):
        user_input = [values["prio_monetary_policy_1"], values["prio_brand_management_1"], values["prio_financial_analysis_1"], values["prio_history_of_economics_ethics_1"]]
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
        form_fields = ["prio_monetary_policy_2", "prio_brand_management_2", "prio_financial_analysis_2", "prio_history_of_economics_ethics_2"]
        random.shuffle(form_fields)

        if player.group.treatment == True:
            more_form_fields = ["monetary_policy_points", "brand_management_points", "financial_analysis_points", "history_of_economics_ethics_points"]
            random.shuffle(more_form_fields)
            form_fields += more_form_fields

        return form_fields
    # Fehlerüberprüfung in Abhängigkeit von der Gruppe auf aufsummierte 100 oder 1 bis 4 Priorität 
    def error_message(player, values):
        # Fehlerüberprüfung 1 bis 4 und 100
        if player.group.treatment == True:
            # 100 
            if values["monetary_policy_points"] + values["brand_management_points"] + values["financial_analysis_points"] + values["history_of_economics_ethics_points"] != 100:
                return "The numbers must add up to 100"
            # 1 bis 4
            user_input = [values["prio_monetary_policy_2"], values["prio_brand_management_2"], values["prio_financial_analysis_2"], values["prio_history_of_economics_ethics_2"]]
            if set(user_input) != set(range(1, 5)):
                return "Bitte geben Sie jede Zahl von 1 bis 4 nur einmal ein."
        
        # Fehlerüberprüfung 1 bis 4
        if player.group.treatment == False:
            user_input = [values["prio_monetary_policy_2"], values["prio_brand_management_2"], values["prio_financial_analysis_2"], values["prio_history_of_economics_ethics_2"]]
            if set(user_input) != set(range(1, 5)):
                return "Bitte geben Sie jede Zahl von 1 bis 4 nur einmal ein."


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = get_wpms

class Results(Page):
    form_model = "player"
    
    def get_form_fields(player):
        if player.group.treatment == True:
            form_fields = ["WhichIsBetter", "Control", "RandomChoice", "Comfortable", "FinalChoice"]
        if player.group.treatment == False:
            form_fields = []
        return form_fields
    @staticmethod
    
    def vars_for_template(player: Player):
        group = player.group
    def clean(player):
        if player.WhichIsBetter is None:
            raise models.ValidationError('Please select a value')
        if player.Control is None:
            raise models.ValidationError('Please select a value')
        if player.RandomChoice is None:
            raise models.ValidationError('Please select a value')
        if player.Comfortable is None:
            raise models.ValidationError('Please select a value')
        if player.FinalChoice is None:
            raise models.ValidationError('Please select a value')

class End(Page):
    form_model = "player"
    def vars_for_template(player):
        if player.Winner == 0:
            winner_text = "No Haribo for you"
            
        if player.Winner == 1:
            winner_text = "Congrats you get some Haribos"
        return {"winner_text": winner_text}
         
            
page_sequence = [Introduction, Preference_elicitation, PreferenceWaitPage, Bid, ResultsWaitPage, Results, End]