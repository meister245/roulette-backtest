roulette
--------

#### Description & Usage

```
./bin/roulette -h
```

Testing is based around betting configurations, that define the following:

1. Strategy used for betting
2. When to start betting, defining a pattern when betting should initiate
3. How much units to wager in the bet
4. Where should the bets be placed
5. Should betting stop after a certain number of losses *(optional, for progressive strategies)*
6. Should betting stop after a certain number of wins *(optional, for progressive strategies)*

**Example configuration**
```
martingale,red:red:black,2,black,3,1
```

Place 2 units with martingale strategy on black, if the last numbers were red, red and black
Stop betting if the bet loses 3 time(s) in a row or wins 1 time(s)
If the bet loses, re-bet the original wager multiplied by 2

**Generic configuration format**
```
<strategy>,<pattern:pattern...>,<wager>,<bet_type:bet_type...>,<loss_limit>,<win_limit>
```

**Supported strategies**
```
simple (no progression)
martingale (multiply wager after losing)
paroli (multiply wager after winning)
```

**Valid bet types**
```
red, black, even, odd, low, high, zero, four
column_bottom, column_center, column_top, dozen_first, dozen_second, dozen_third
straight_0, straight_1, straight_2, straight_3, straight_4, straight_5, straight_6, straight_7, straight_8, straight_9, straight_10, straight_11, straight_12, straight_13, straight_14, straight_15, straight_16, straight_17, straight_18, straight_19, straight_20, straight_21, straight_22, straight_23, straight_24, straight_25, straight_26, straight_27, straight_28, straight_29, straight_30, straight_31, straight_32, straight_33, straight_34, straight_35, straight_36
split_1_2, split_2_3, split_4_5, split_5_6, split_7_8, split_8_9, split_10_11, split_11_12, split_13_14, split_14_15, split_16_17, split_17_18, split_19_20, split_20_21, split_22_23, split_23_24, split_25_26, split_26_27, split_28_29, split_29_30, split_31_32, split_32_33, split_34_35, split_35_36, split_1_4, split_2_5, split_3_6, split_4_7, split_5_8, split_6_9, split_7_10, split_8_11, split_9_12, split_10_13, split_11_14, split_12_15, split_13_16, split_14_17, split_15_18, split_16_19, split_17_20, split_18_21, split_19_22, split_20_23, split_21_24, split_22_25, split_23_26, split_24_27, split_25_28, split_26_29, split_27_30, split_28_31, split_29_32, split_30_33, split_31_34, split_32_35, split_33_36
street_1_2_3, street_4_5_6, street_7_8_9, street_10_11_12, street_13_14_15, street_16_17_18, street_19_20_21, street_22_23_24, street_25_26_27, street_28_29_30, street_31_32_33, street_34_35_36
corner_1_2_4_5, corner_2_3_5_6, corner_4_5_7_8, corner_5_6_8_9, corner_7_8_10_11, corner_8_9_11_12, corner_10_11_13_14, corner_11_12_14_15, corner_13_14_16_17, corner_14_15_17_18, corner_16_17_19_20, corner_17_18_20_21, corner_19_20_22_23, corner_20_21_23_24, corner_22_23_25_26, corner_23_24_26_27, corner_25_26_28_29, corner_26_27_29_30, corner_28_29_31_32, corner_29_30_32_33, corner_31_32_34_35, corner_32_33_35_36
line_1_2_3_4_5_6, line_4_5_6_7_8_9, line_7_8_9_10_11_12, line_10_11_12_13_14_15, line_13_14_15_16_17_18, line_16_17_18_19_20_21, line_19_20_21_22_23_24, line_22_23_24_25_26_27, line_25_26_27_28_29_30, line_28_29_30_31_32_33, line_31_32_33_34_35_36
```

#### RNG testing

Test your strategy against a random number generator

```
./bin/roulette martingale,odd:odd:even,2,even,3,1 martingale,even:even:odd,1,odd,3,1 -s 8
```

```
  Total Spins  Balance (S/C)      Total Profit    Profit Ratio (%)
-------------  ---------------  --------------  ------------------
            8  100.0 / 103.0                 3                   3

+-----------+----------------+--------------+----------+----------+----------+
|   Balance | Bets           | Bet Amount   |   Number | Status   |   Profit |
+===========+================+==============+==========+==========+==========+
|       100 | ---            | ---          |       10 | ---      |        0 |
+-----------+----------------+--------------+----------+----------+----------+
|       100 | ---            | ---          |        9 | ---      |        0 |
+-----------+----------------+--------------+----------+----------+----------+
|       100 | ---            | ---          |       17 | ---      |        0 |
+-----------+----------------+--------------+----------+----------+----------+
|       102 | W - 2.0 - even | 2.0          |        4 | W        |        2 |
+-----------+----------------+--------------+----------+----------+----------+
|       102 | ---            | ---          |       24 | ---      |        0 |
+-----------+----------------+--------------+----------+----------+----------+
|       101 | F - 1.0 - odd  | 1.0          |       12 | L        |       -1 |
+-----------+----------------+--------------+----------+----------+----------+
|       103 | W - 2.0 - odd  | 2.0          |       35 | W        |        2 |
+-----------+----------------+--------------+----------+----------+----------+
|       103 | ---            | ---          |        9 | ---      |        0 |
+-----------+----------------+--------------+----------+----------+----------+
```

#### Backtesting

You can use real casino data using the `-m backtest` switch.

There is historical roulette casino data included in the `./resources/backtest` folder.
Place your text file in the folder (comma separated numbers) and the application will use it.

If you want to test your strategy against the full set of data in each file
set the numbers of spins to 0, using the `-s 0` switch.

```
./bin/roulette martingale,red:red:red:red:red:black,1,black,4,1 -s 0 -m backtest
```

```
+---------------------------------+---------------+--------------+----------------+-----------------+
| Filename                        |   Total Spins |   Total Bets |   Total Profit |   Win Ratio (%) |
+=================================+===============+==============+================+=================+
| bitcasino-arabic-roulette       |          1461 |           38 |            -14 |           42.11 |
+---------------------------------+---------------+--------------+----------------+-----------------+
| bitcasino-bombay-speed-roulette |          1461 |           53 |             -5 |           47.17 |
+---------------------------------+---------------+--------------+----------------+-----------------+
| bitcasino-en-vivo               |          1461 |           35 |            -15 |           42.86 |
+---------------------------------+---------------+--------------+----------------+-----------------+
| bitcasino-immersive-roulette    |          1461 |           44 |            -25 |           45.45 |
+---------------------------------+---------------+--------------+----------------+-----------------+
| bitcasino-roulette              |          1461 |           19 |             13 |           68.42 |
+---------------------------------+---------------+--------------+----------------+-----------------+
| bitcasino-speed-roulette        |          1461 |           31 |             17 |           54.84 |
+---------------------------------+---------------+--------------+----------------+-----------------+
| bitcasino-turkce-roulette       |          1461 |           33 |              4 |           57.58 |
+---------------------------------+---------------+--------------+----------------+-----------------+
| bitcasino-vip-roulette          |          1461 |           37 |              2 |           45.95 |
+---------------------------------+---------------+--------------+----------------+-----------------+
```
