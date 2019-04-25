roulette-simulator
------------------

Command line tool used to backtest roulette strategies against
real casino roulette spin data, random generated numbers or user provided data

#### Setup & Usage

Python 3.5.2 or greater required

Clone repository and install all dependencies
```
pip install -r ./requirements.txt 
```

Run simulation and display usage
```
./bin/roulette -h
```

#### Betting configuration

The simulation is based around betting configurations, that define the following:

* Strategy used for betting *(progressive, flat)*
* When to start betting, how much to bet and what to bet on
* Should betting stop after a certain number of losses *(optional)*
* Should betting stop after a certain number of wins *(optional)*

```
martingale,black:red:red,2,black,3,1
```

Place 2 units with martingale strategy, if the last numbers were red, red and black.
Stop betting if the bet wins. If the bet loses, double the bet on each lost bet.
If losing 3 times in a row, stop betting.

The above configuration follows the generic format
```
<strategy>,<trigger_pattern>,<wager>,<bet type>,<loss_limit>,<win_limit>
```

#### Backtesting

By default the simulation is using number generated numbers. You can bring real casino data
to backtest your strategy. There are a number of real data included in the `./resources/backtest` folder.
Place your file in the folder and provide the filename as a parameter.

```
./bin/roulette -b martingale,even:odd:odd,2,even,3,1 --backtest spielbank-wiesbaden.de_t1_190424.txt
```

#### Single simulation

```
./bin/roulette -b martingale,even:odd:odd,2,even,3,1 -b martingale,odd:even:even,1,odd,3,1 -s 8 -m single
```

```
  Total Spins  Balance (S/C)      Total Profit    Profit Ratio (%)
-------------  ---------------  --------------  ------------------
            8  100.0 / 103.0                 3                   3

+-----------+----------------+--------------+----------+----------+----------+
|   Balance | Bets           | Bet Amount   |   Number | Status   |   Profit |
+===========+================+==============+==========+==========+==========+
|       100 | ---            | ---          |        4 | ---      |        0 |
+-----------+----------------+--------------+----------+----------+----------+
|       100 | ---            | ---          |       21 | ---      |        0 |
+-----------+----------------+--------------+----------+----------+----------+
|       100 | ---            | ---          |        5 | ---      |        0 |
+-----------+----------------+--------------+----------+----------+----------+
|       102 | W - 2.0 - even | 2.0          |       14 | W        |        2 |
+-----------+----------------+--------------+----------+----------+----------+
|       102 | ---            | ---          |       12 | ---      |        0 |
+-----------+----------------+--------------+----------+----------+----------+
|       101 | L - 1.0 - odd  | 1.0          |       26 | L        |       -1 |
+-----------+----------------+--------------+----------+----------+----------+
|        99 | L - 2.0 - odd  | 2.0          |        8 | L        |       -2 |
+-----------+----------------+--------------+----------+----------+----------+
|       103 | W - 4.0 - odd  | 4.0          |        3 | W        |        4 |
+-----------+----------------+--------------+----------+----------+----------+
```

#### Aggregate simulation

```
./bin/roulette -b martingale,even:odd:odd,2,even,3,1 -b martingale,odd:even:even,1,odd,3,1 -s 100 -c 500 -m aggregate
```

```
  Total Games    Avg. Win Ratio (%)    Avg. Profit Total    Avg. Profit Ratio (%)    Avg. Spin Count
-------------  --------------------  -------------------  -----------------------  -----------------
          500                48.416                -2.93                   -2.934                100
```

