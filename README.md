### c_cats

Scripts for fetching cryptocurrency data and generating chart images, suitable for presentation use.

### Usage
```
$ pwd
Users/YOUR_NAME/c_cats/scripts

$ ls
get_data.py	show_chart.py	technical.py

$ python3 get_data.py
            time        high        low         open    ...
0           foo         foo         foo         foo     ...
...         ...         ...         ...         ...     ...
3802        bar         bar         bar         bar     ...  

[3803 rows x 10 columns]

$ ls
btc2usd.csv get_data.py	show_chart.py	technical.py

$ python3 show_chart.py
```
![show_chart_ex.png](/docs/show_chart_ex.png)
![show_chart_ex2.png](/docs/show_chart_ex2.png)

---

### You can easily try System Trading

```
$ pwd
/Users/your_name/c_cats/c_cats

$ python3 btc_technical.py
[c_cats] LAST_DATE: 20200427
[c_cats] TODAY_DATE: 20200427
--------------------------------------------------------------------------------
DATE:2019-06-01  PRICE:925022  SIGNAL:0.0  STOP_LOSS:0.0  SECURE_PROFIT:0.0  JPY:10000000  BTC:0.0  TOTAL:10000000
DATE:2019-06-02  PRICE:946500  SIGNAL:0.0  STOP_LOSS:0.0  SECURE_PROFIT:0.0  JPY:10000000  BTC:0.0  TOTAL:10000000
DATE:2019-06-03  PRICE:878998  SIGNAL:0.0  STOP_LOSS:0.0  SECURE_PROFIT:0.0  JPY:10000000  BTC:0.0  TOTAL:10000000
...
DATE:2020-03-30  PRICE:693221  SIGNAL:0.0  STOP_LOSS:0.0  SECURE_PROFIT:0.0  JPY:9799231  BTC:0.0  TOTAL:9799231
DATE:2020-03-31  PRICE:691824  SIGNAL:0.0  STOP_LOSS:0.0  SECURE_PROFIT:0.0  JPY:9799231  BTC:0.0  TOTAL:9799231
DATE:2020-04-01  PRICE:714987  SIGNAL:0.0  STOP_LOSS:0.0  SECURE_PROFIT:0.0  JPY:9799231  BTC:0.0  TOTAL:9799231
[START] 	JPY: 10000000 	BTC: 0.0 	TOTAL: 10000000
[BUY-AND-HOLD] 	JPY: 657280 	BTC: 10 	TOTAL: 7807150
[ALGORITHM] 	JPY: 9799231 	BTC: 0.0 	TOTAL: 9799231
[c_cats] Simulation Result:-2.00769%  Trading Count:8
--------------------------------------------------------------------------------
[c_cats] You don't have to trade BTC today
```

![result_example3.png](/docs/result_example3.png)
