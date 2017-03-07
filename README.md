# ScorePredictionRep

## Synopsis

This project is targetting on how to predict European league football match results based on the history data of teams,matches,bet-odds by using machine learning algorithms

## Code Structure 
  
    ├── data
    │   ├── db
    │   │   └── database.sqlite
    │   ├── experiments
    │   │   ├── 20170303103119_4
    │   │   ├── 20170303120918_1
    │   │   └── 20170303121756_1
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
        │   │   ├── enetscores
        │   │   │   ├── CrawlMatch.py
        │   │   │   ├── Crawler.py
        │   │   │   ├── CrawlerIncidents.py
        │   │   │   ├── CrawlerLeague.py
        │   │   │   ├── CrawlerLineup.py
        │   │   │   ├── CrawlerTeam.py
        │   │   │   └── __init__.py
        │   │   ├── football_data
        │   │   │   ├── Crawler.py
        │   │   │   ├── CrawlerEvent.py
        │   │   │   ├── CrawlerLeague.py
        │   │   │   ├── CrawlerMatch.py
        │   │   │   └── __init__.py
        │   │   └── sofifa
        │   │       ├── Crawler.py
        │   │       ├── CrawlerLeague.py
        │   │       ├── CrawlerPlayer.py
        │   │       ├── CrawlerTeam.py
        │   │       └── __init__.py
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
        │   └── __init__.py
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

## Motivation

A short description of the motivation behind the creation and maintenance of the project. This should explain **why** the project exists.

## Installation

Provide code examples and explanations of how to get the project.

## API Reference

Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.

## Tests

Describe and show how to run the tests with code examples.

## Contributors
Simone Caldaro : caldaro.1324152@studenti.uniroma1.it

Leonardo Martini : martini.1722989@studenti.uniroma1.it 

Na Zhu : nana.zhu@hotmail.com

Instructors:  

Aris Anagnostopoulos

Ioannis Chatzigiannakis

# Reference : 
[A Comparison of Methods for Predicting Football Matches ,David B. Ekefre ](http://liacs.leidenuniv.nl/assets/Masterscripties/ICTiB/2015-2016/Ekefre-non-confidential.pdf)
