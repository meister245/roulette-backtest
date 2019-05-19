bruteforce
----------

Display usage
```
./bin/bruteforce -h
```

#### Description

Building on roulette backtesting, bruteforce is used to test all possible bet configurations

Processing all possible patterns multiplied by all possible bets, this is CPU bound process.
It is strongly recommended to restrict the number of patterns / bets to achieve optimal runs.

#### Example

```
./bin/bruteforce -s 500 -m backtest -pl even,odd,high,low,red,black,dozen_first,dozen_second,dozen_third -bl even,odd,high,low,red,black,dozen_first,dozen_second,dozen_third
```

```
roulette-backtest version: 1.0.0
--------------------------------
generating bet configurations
{'config': 'simple,dozen_third:dozen_second,1,dozen_second,1,1', 'avg_profit': 5.5}
{'config': 'simple,dozen_third:low,1,even,1,1', 'avg_profit': 5.125}
{'config': 'simple,high:low,1,even,1,1', 'avg_profit': 6.375}
{'config': 'simple,even:black,1,even,1,1', 'avg_profit': 5.375}
{'config': 'simple,dozen_second:black,1,even,1,1', 'avg_profit': 5.625}
{'config': 'simple,dozen_first:red,1,dozen_first,1,1', 'avg_profit': 5.0}
{'config': 'simple,dozen_first:dozen_second,1,dozen_first,1,1', 'avg_profit': 5.25}
{'config': 'simple,dozen_third:dozen_first,1,dozen_third,1,1', 'avg_profit': 6.125}
{'config': 'simple,high:dozen_first,1,dozen_third,1,1', 'avg_profit': 9.125}
{'config': 'simple,dozen_second:low,1,dozen_third,1,1', 'avg_profit': 7.75}
{'config': 'simple,high:low,1,dozen_third,1,1', 'avg_profit': 7.5}
{'config': 'simple,odd:even,1,dozen_third,1,1', 'avg_profit': 6.5}
{'config': 'simple,odd:dozen_first,1,dozen_third,1,1', 'avg_profit': 5.875}
{'config': 'simple,black:dozen_first,1,dozen_third,1,1', 'avg_profit': 6.0}
{'config': 'simple,black:even,1,dozen_third,1,1', 'avg_profit': 6.5}
{'config': 'simple,dozen_second:red,1,dozen_third,1,1', 'avg_profit': 5.375}
{'config': 'simple,black:red,1,dozen_third,1,1', 'avg_profit': 7.375}
{'config': 'simple,black:low,1,dozen_third,1,1', 'avg_profit': 10.25}
{'config': 'simple,red:dozen_second,1,low,1,1', 'avg_profit': 6.0}
{'config': 'simple,dozen_third:dozen_first,1,high,1,1', 'avg_profit': 5.125}
{'config': 'simple,high:dozen_first,1,high,1,1', 'avg_profit': 5.375}
{'config': 'simple,odd:high,1,high,1,1', 'avg_profit': 5.25}
{'config': 'simple,odd:even,1,high,1,1', 'avg_profit': 6.25}
{'config': 'simple,odd:black,1,high,1,1', 'avg_profit': 5.875}
{'config': 'simple,black:dozen_first,1,high,1,1', 'avg_profit': 7.5}
{'config': 'simple,black:even,1,high,1,1', 'avg_profit': 5.5}
{'config': 'simple,black:red,1,high,1,1', 'avg_profit': 7.25}
{'config': 'simple,black:low,1,high,1,1', 'avg_profit': 9.375}
```
