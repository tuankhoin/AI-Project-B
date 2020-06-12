# COMP30024 Project B: Expendibots by Boomers

This is the main repository to Project B of [COMP30024, Semester 1 2020](https://handbook.unimelb.edu.au/2020/subjects/comp30024).

## Author

This project is made by Boomers, which consists of 2 members: 
* Tuan Khoi Nguyen (Khoi): Expansion strategy and improvements.
* Nicholas Wong: In-course implementation.

## Rules and specs

* [Rules of Expendibots](https://github.com/tuankhoin/AI-Project-B/blob/master/Expendibots_Rules.pdf)
* [Project Requirements](https://github.com/tuankhoin/AI-Project-B/blob/master/Project_Spec.pdf)

## Strategy

Some of our expansion strategy includes, but not limited to:
* Transposition table and Zobrist Hashing.
* Inverted Quiesence Search, a custom improvement of Quiesence Search to fit the game of Expendibots.
* TDLeaf(Lambda) Learning.

Our full strategy evaluation can be found in [the project report](https://github.com/tuankhoin/AI-Project-B/blob/master/Boomers_ProjectB_Report.pdf).

## Setting up and run

* Clone the repo.
* Install numpy: `pip install numpy`.
* See custom help for the referee: `python -m referee --help`.
* Run the referee: `python -m referee <package1> <package2> <options>`.
* Choose your agent package:
  * `boomers`: Our main package.
  * `random_agent`: Agent that takes on a random move.
  * `greedy_agent`: Agent that takes on the most promising immediate move.
  
## Outcome

As mentioned above, this package serves as the main project to The University of Melbourne's COMP30024 - Artificial Intelligence, a 3rd year Subject.

Despite the fact that our strategist (Khoi) was only a 2nd year student at the time, the Boomers had received almost full marks for the creativity part, which very few groups was able to achieve. In the competitive side, the Boomers' Expendibots agent was able to made it into the upper division, beating many groups of 3rd year and Masters students.

The overall score our team received was 18. Despite being informed that Boomers went into upper division, the statistics for 2020 was not revealed, so the cohort's score distribution from 2016 is used to have an estimate of where we have reached (Source: Matt Farrugia's [AI project](https://github.com/matomatical/AI-projectB)):


     0 | 
    ...|
     7 | 
     8 | *
     9 | 
    10 | ***
    11 | ****
    12 | ********
    13 | *********
    14 | ***********
    15 | ********
    16 | *******
    17 | ***
    18 | **   <--- We are here
    19 | *
    20 | 
    21 | 
    22 | * 



## Usage

You can clone this repo and try running a game, or build up your own agent. Creating an agent for a customized game will focus a lot on the formulation from the core, which in turn can help improving your strategic thinking.

As a courtesy of Melbourne School of Computing and Information Systems, it is also notable that if you plan to use our code for your academic assignments, please be aware that you might get caught for Academic Misconduct.
