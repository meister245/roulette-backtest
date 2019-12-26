bruteforce
----------

#### Description & Usage

`./bin/bruteforce -h`

Processing the cartesian product of possible combination of betting patterns and bet placements takes exponential time to finish.
It is strongly recommended to restrict the number of patterns and / or bet types to achieve optimal runs.

The following command will:

* Generate all possible betting patterns from the list of provided bet types. (combinations with replacement)
* Generate all possible unique bets from the list of provided bet types. (combinations with no replacement)
* Iterate through the cartesian product of the generated bet patterns and bet combinations and play a virtual match of 500 spins (or less if it goes bust sooner)
* Backtest using real casino numbers (alternatively random numbers)
* Display any resulting bet configuration, which resulted in greater profit than the defined threshold (default: 5.0)

Profit calculation:

* The simulation reads all data files in the `/resources/backtest/` folder
* Betting configurations are run for each data file and the resulting profit is stored
* Average is calculated on resulting profit numbers (6 data files -> average of 6 simulations)

#### Example

```
./bin/bruteforce -s 500 -pl even,odd,high,low,red,black -bl dozen_first,dozen_second,dozen_third --min-profit 5.0
```

* Total Bet Patterns: 6 + 21 + 56 + 126 + 252 + 462 = 923
* Total Bet Combinations: 3 + 3 + 1 = 7
* Total Bet Configurations: 923 * 7 = 6461

```
roulette-backtest - 2.1.0
-------------------------
generating bet configurations - strategy: simple - min profit: 5.0
{'config': 'simple,black,1,dozen_third,1,1', 'avg_profit': 5.125}
{'config': 'simple,high,1,dozen_third,1,1', 'avg_profit': 5.75}
{'config': 'simple,black:low,1,dozen_third,1,1', 'avg_profit': 5.75}
{'config': 'simple,black:even,1,dozen_third,1,1', 'avg_profit': 5.625}
{'config': 'simple,high,1,dozen_second:dozen_third,1,1', 'avg_profit': 5.375}
{'config': 'simple,black:even,1,dozen_second:dozen_third,1,1', 'avg_profit': 5.5}
processed 6461 combination
```