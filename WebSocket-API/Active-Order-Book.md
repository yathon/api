# 活跃订单簿

/sub?id=orderbook.{symbol}.{level}

## 参数说明

| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 交易级别 | level | 必须，当前仅支持ALL, 其他将被支持的级别L20、L50 |

## 举例

wss://ws.betaex.com/sub?id=orderbook.BTC_USDT.ALl
