# ScorePredictionRep

## Synopsis

This project is targeting on how to predict European league football match results based on the history data of teams,matches,bet-odds by using machine learning algorithms

## Motivation

**We've been really involved in this project, starting from understanding the basis of "stream" application, to those techniques to mining data.**


## Code  
### src
#### application 
>Code for crawling the data , pre-process and algorithms

    Crawl:  
        One of the most important part for this project is collecting data from different websites and formalize
        Code for crawling the website information,Collect data for teams, players,leageues,matches and bet-odds
            enetscores
                crawling from http://football-data.mx-api.enetscores.com
            football_data
                crawling from http://www.odds.football-data.co.uk
            sofifa
                crawling from http://sofifa.com
    Domain:
        Code for Dedicated methods for different types of data
            
    Exception:
        Code for Customizing the exceptions for this application
    MachineLearning:
        Another most important part for this project is :
        Code for using the different algorithm for calculating the predictions
            experiments
            input_train
            my_possion
            my_sklearn
            prediction_accuracy
    
### gui
>Code for User interactive interface, implements easy instruction for customized the input parameters 
### test
>Test code for without GUI part ,calling /src/application/MachineLearning/experiments to test different combinations of inputs and algorithms
### util
>Code for all the common functions
### main.py 
>Entry for the whole application.

#### Demostration for main.py
#####./ScorePredictionRep/src/main.py --no-crawl --no-index -v

--no-crawl :  for not crawling the website and update the SQLLite

--no-index :  for indexing the Italy league

-v        :  for the debug 

    python ./ScorePredictionRep/src/main.py
    > Initialization DB
    > Indexing...
         ...finished in 181.01 seconds
    > Init crawling: started
    ****************************************************************************************************
    *********************************** ScorePrediction application ***********************************
    ****************************************************************************************************
    Browse the application to discover different data
        - 1 : Players
        - 2 : Matches
        - 3 : Leagues
        - 4 : Countries
        - 5 : Teams
        - 6 : Crawling
        - 7 : Prediction
        - 8 : Bet odds
    Browse the application to discover different data
        - 1 : Players
        - 2 : Matches
        - 3 : Leagues
        - 4 : Countries
        - 5 : Teams
        - 6 : Crawling
        - 7 : Prediction
        - 8 : Bet odds
    Select an item: 1
    [INFO: Opening --> Players]
    
    Players menu:
        - 1 : Find by Name
        - 2 : Find by Team
        - gb : Go back
    
    Select an item: 1
    [INFO: Machine Learning Framework --> 1]
    [INFO: Machine Learning Algorithm --> 2]
    [INFO: Machine Learning Input --> 1]
    [INFO: Machine Learning Input representation --> 2]
    [INFO: Machine Learning Training Size --> 20]
    [INFO: Setting --> predictor]
    [ANSWER of List --> Frameworks (String)]
        1) Sklearn
        2) my_poisson
    [ANSWER of List --> Algorithms (String)]
        1) SVM
        2) KNN
        3) RandomForest
    [ANSWER of List --> Machine learning input (Id)]
        1) team form
            Representations: [1, 2, 3, 4]
        2) team home away form
            Representations: [1, 2, 3, 4]
        3) match statistics
            Representations: []
        4) Kekko input
            Representations: []
        5) Poisson inpunt
            Representations: []
    [INSTRUCTION: list of parameter --> framework(str) algorithm(str) input(int) representation(int) training(int)]
    [INSTRUCTION: Use . for --> default]
    
    Type your representation: Sklearn KNN 1 2 20
    ****************************************************************************************************
    Predictions Menu:
        - 1 : Set Current Predictor
        - 2 : Show Current Predictor
        - 3 : Check setting current predictor
        - 4 : Predict matches by date
        - gb : Go back
    
    Select an item: 2
    [INFO: Show --> Current Predictor]
    [INFO: Machine Learning Framework --> Sklearn]
    [INFO: Machine Learning Algorithm --> KNN]
    [INFO: Machine Learning Input --> 1]
    [INFO: Machine Learning Input representation --> 2]
    [INFO: Machine Learning Training Size --> 20]
    ****************************************************************************************************
    Predictions Menu:
        - 1 : Set Current Predictor
        - 2 : Show Current Predictor
        - 3 : Check setting current predictor
        - 4 : Predict matches by date
        - gb : Go back
    
    Select an item: 4
    [INFO: Predict matches by --> date]
    Insert a date (YYYY-MM-DD) or an integer (the day passed from today --> 0 is today): -4
    [ANSWER of Prediction by date --> 2017-03-18]
        1) SD Eibar vs RCD Espanyol
            1	(57.14%)
        2) Aberdeen vs Heart of Midlothian|Hearts
            1	(100.0%)
        3) West Bromwich Albion vs Arsenal
            1	(58.06%)
        4) VfL Wolfsburg vs SV Darmstadt 98
            1	(44.44%)
        5) 1. FC Köln vs Hertha BSC Berlin
            1	(66.67%)
        6) FC Augsburg vs SC Freiburg
            1	(66.67%)
        7) SV Werder Bremen vs RB Leipzig
            2	(55.56%)
        8) TSG 1899 Hoffenheim vs Bayer 04 Leverkusen
            1	(66.67%)
        9) Piast Gliwice vs Arka Gdynia
            2	(66.67%)
        10) Crystal Palace vs Watford
            2	(45.16%)
        11) Everton vs Hull City
            1	(58.06%)
        12) Stoke City vs Chelsea
            1	(38.71%)
        13) Sunderland vs Burnley
            2	(45.16%)
        14) West Ham United vs Leicester City
            1	(58.06%)
        15) Inverness Caledonian Thistle vs Ross County FC
            0	(40.0%)
        16) Kilmarnock vs Partick Thistle F.C.
            1	(80.0%)
        17) Motherwell vs St. Johnstone FC|St Johnstone
            1	(60.0%)
        18) Rangers vs Hamilton Academical FC
            1	(60.0%)
        19) Athletic Club de Bilbao|Athletic Bilbao vs Real Madrid CF
            2	(47.62%)
        20) FC Nantes vs OGC Nice
            2	(71.43%)
        21) CF Os Belenenses vs SC Braga|Sporting de Braga
            1	(60.0%)
        22) Moreirense FC vs Tondela
            0	(33.33%)
        23) FC Luzern vs FC Sion
            1	(46.15%)
        24) Torino vs Inter|Internazionale
            2	(41.94%)
        25) Zagłębie Lubin|Zaglebie Lubin vs Ruch Chorzów|Ruch Chorzow
            1	(58.06%)
        26) Alaves|Deportivo Alaves vs Real Sociedad
            2	(47.62%)
        27) Bournemouth|AFC Bournemouth vs Swansea City
            2	(45.16%)
        28) Eintracht Frankfurt vs Hamburger SV
            1	(66.67%)
        29) FC Groningen vs Willem II
            1	(48.39%)
        30) Sporting CP vs CD Nacional|Nacional da Madeira
            1	(66.67%)
        31) N.E.C.|NEC vs FC Utrecht
            1	(48.39%)
        32) PSV|PSV Eindhoven vs Vitesse
            1	(74.19%)
        33) AS Nancy-Lorraine vs FC Lorient
            1	(66.67%)
        34) Girondins de Bordeaux vs Montpellier Hérault SC|Montpellier HSC
            0	(38.1%)
        35) Toulouse FC vs Stade Rennais FC
            1	(38.1%)
        36) Angers SCO vs En Avant de Guingamp|En Avant Guingamp
            0	(38.1%)
        37) FC Basel vs Grasshopper Club Zürich
            1	(84.62%)
        38) Pogoń Szczecin|Pogon Szczecin vs Jagiellonia Białystok|Jagiellonia Bialystok
            1	(58.06%)
        39) Real Betis Balompié vs CA Osasuna
            1	(52.38%)
        40) Milan|AC Milan vs Genoa
            1	(61.29%)
        41) Sparta Rotterdam vs Heracles Almelo
            1	(41.94%)
        42) FC Paços de Ferreira vs SL Benfica
            2	(60.0%)
    ****************************************************************************************************




## API Reference

[Scikit-learn](http://scikit-learn.org/stable/modules/classes.html)

###Test for algorithm
####Input

**Team Form**: combination of points gathered by the teams 

**Team Home Away Form**: combination of points gathered by the teams, considering matches played at home and away. 

**Match Statistics**: combination of previous match statistics performed by teams. 

**Kekko input**: features an human uses to gather information before placing a bet. 

**Poisson input**: home strength and away strength (average goal a team will score)

#### Data representation :
The representations of the Team Forms are:
1. **Representation 1 (r1)**: This represents the numeric values of the team forms, normalized to interval [0,3].
2. **Representation 2 (r2)**: This represents the discretized value of the team forms. We had reason to believe that the classifiers do not distinguish between values well enough while using r1, so we discretized r1 
3. **Representation 3 (r3)**: This represents the subtracted value between the home team form and away team form. This subtracted value is normalized to the interval [-3,3]; a negative value means away team superiority and a positive value means home team superiority while zero means an equal advantage.
4. **Representation 4 (r4)**: This represents the discretized values of r3. This representation will be discretized by equal frequency into three bins.

#### ALgorithms: 
[K-NearestNeighbourhood](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)

[SVM-MultiClassifier](https://en.wikipedia.org/wiki/Support_vector_machine)

[RandomForest](https://en.wikipedia.org/wiki/Random_forest)

[Possion](https://en.wikipedia.org/wiki/Poisson_distribution)

#### Test Window Size

Number of past stages to consider in training: depending on the league, every stage has different number of matches (e.g., Italy has 10 matches in a stage, while Germany just 9 matches).

Windows tested:
[ 9, 11, 19, 35, 71, 105, 141]

### Test for different betting methods on different league and diffent seasons 
1) Flat Bet: for all predictions, bet 1€
2) Smart Bet: for all prediction bet if and only if 𝑝>_1_𝑥_ (probability > 1/bet-odd)
3) Most accurate teams bet: bet only on that teams that seems to be most accurate in predictions
4) Combination of 2 and 3



## Contributors
Simone Caldaro caldaro.1324152@studenti.uniroma1.it

Leonardo Martini martini.1722989@studenti.uniroma1.it 

Na Zhu zhu.1706409@studenti.uniroma1.it

## Instructors:  

Aris Anagnostopoulos

Ioannis Chatzigiannakis

# Reference
## Papers
[A Comparison of Methods for Predicting Football Matches, David B. Ekefre ](http://liacs.leidenuniv.nl/assets/Masterscripties/ICTiB/2015-2016/Ekefre-non-confidential.pdf)

[Predicting Soccer Match Results in the English Premier League, Ben Ulmer, Matthew Fernandez](http://cs229.stanford.edu/proj2014/Ben%20Ulmer,%20Matt%20Fernandez,%20Predicting%20Soccer%20Results%20in%20the%20English%20Premier%20League.pdf)

[Modelling Association Footbal Scores and Inefficiencies in the Football Betting Market, Dixon and Coles](http://www.math.ku.dk/~rolf/teaching/thesis/DixonColes.pdf)

## Code Structure 

    ├── data
    │   ├── db
    │   │   └── database.sqlite
    │   ├── experiments
    │   ├── log
    │   │   ├── crawl_log.txt
    │   │   └── logging.txt
    │   │ 
    └── src
        ├── __init__.py
        ├── __pycache__
        ├── application
        │   ├── Crawl
        │   │   ├── Crawl.py
        │   │   ├── __init__.py
        │   │   ├── __pycache__
        │   │   ├── enetscores
        │   │   │   ├── CrawlMatch.py
        │   │   │   ├── Crawler.py
        │   │   │   ├── CrawlerIncidents.py
        │   │   │   ├── CrawlerLeague.py
        │   │   │   ├── CrawlerLineup.py
        │   │   │   ├── CrawlerTeam.py
        │   │   │   ├── __init__.py
        │   │   │   └── __pycache__
        │   │   ├── football_data
        │   │   │   ├── Crawler.py
        │   │   │   ├── CrawlerEvent.py
        │   │   │   ├── CrawlerLeague.py
        │   │   │   ├── CrawlerMatch.py
        │   │   │   ├── __init__.py
        │   │   │   └── __pycache__
        │   │   └── sofifa
        │   │       ├── Crawler.py
        │   │       ├── CrawlerLeague.py
        │   │       ├── CrawlerPlayer.py
        │   │       ├── CrawlerTeam.py
        │   │       ├── __init__.py
        │   │       └── __pycache__
        │   ├── Domain
        │   │   ├── Bet_Event.py
        │   │   ├── Country.py
        │   │   ├── Event.py
        │   │   ├── League.py
        │   │   ├── Match.py
        │   │   ├── MatchEvent.py
        │   │   ├── Player.py
        │   │   ├── Player_Attributes.py
        │   │   ├── Shot.py
        │   │   ├── Team.py
        │   │   ├── Team_Attributes.py
        │   │   ├── __init__.py
        │   │   └── __pycache__
        │   ├── Exception
        │   │   ├── CrawlException.py
        │   │   ├── MLException.py
        │   │   ├── TeamException.py
        │   │   ├── __init__.py
        │   │   └── __pycache__
        │   ├── MachineLearning
        │   │   ├── MachineLearningAlgorithm.py
        │   │   ├── MachineLearningInput.py
        │   │   ├── Plot_graph.py
        │   │   ├── __init__.py
        │   │   ├── __pycache__
        │   │   ├── experiment
        │   │   │   ├── __init__.py
        │   │   │   ├── __pycache__
        │   │   │   ├── experiment.py
        │   │   │   ├── experiment_1.py
        │   │   │   ├── experiment_2.py
        │   │   │   ├── experiment_3.py
        │   │   │   └── experiment_plot.py
        │   │   ├── input_train
        │   │   │   ├── __init__.py
        │   │   │   ├── __pycache__
        │   │   │   ├── kekko_input.py
        │   │   │   ├── match_statistics.py
        │   │   │   ├── poisson.py
        │   │   │   ├── team_form.py
        │   │   │   └── team_home_away_form.py
        │   │   ├── my_poisson
        │   │   │   ├── __init__.py
        │   │   │   ├── __pycache__
        │   │   │   └── poisson.py
        │   │   ├── my_sklearn
        │   │   │   ├── Sklearn.py
        │   │   │   ├── __init__.py
        │   │   │   └── __pycache__
        │   │   ├── my_tensor_flow
        │   │   │   ├── KNNAlgorithm.py
        │   │   │   ├── MultiLayerPerceptron.py
        │   │   │   ├── MulticlassSVM.py
        │   │   │   ├── SVM.py
        │   │   │   ├── __init__.py
        │   │   │   └── __pycache__
        │   │   └── prediction_accuracy
        │   │       ├── __init__.py
        │   │       ├── __pycache__
        │   │       └── prediction_accuracy.py
        │   ├── __init__.py
        │   └── __pycache__
        ├── gui
        │   ├── BetOddsGui.py
        │   ├── CountryGui.py
        │   ├── CrawlGui.py
        │   ├── LeaguesGui.py
        │   ├── MainGui.py
        │   ├── MatchGui.py
        │   ├── PlayerGui.py
        │   ├── PredictionGui.py
        │   ├── TeamGui.py
        │   ├── __init__.py
        │   └── __pycache__
        ├── main.py
        ├── test
        │   ├── TensorFlow.py
        │   ├── Test.py
        │   └── __init__.py
        └── util
            ├── CSV_Reader.py
            ├── Cache.py
            ├── GuiUtil.py
            ├── MLUtil.py
            ├── SQLLite.ini
            ├── SQLLite.py
            ├── __init__.py
            ├── __pycache__
            └── util.py
    
    
   User interactive interface 
   
   Crawl the website information
   
   Collect data for teams, players,leageues,matches and bet-odds
   
   Use the different algorithm for calculating the predictions

Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.
