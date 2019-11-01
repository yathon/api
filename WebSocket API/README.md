# WebSocket API

## API说明
### 服务地址
wss://ws.betaex.com
## 活跃订单簿
/sub?id=orderbook.{symbol}.{level}
### 参数说明

| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 交易级别 | level | 必须，当前仅支持ALL, 其他将被支持的级别L20、L50 |

### 举例
wss://ws.betaex.com/sub?id=orderbook.BTC_USDT.ALl

## 成交记录
/sub?id=trade.{symbol}

### 参数说明
| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |

### 举例
wss://ws.betaex.com/sub?id=trade.BTC_USDT

## 盘口
/sub?id=ticker.{symbol}

### 参数说明
| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
### 举例
wss://ws.betaex.com/sub?id=ticker.BTC_USDT
## k线
/sub?id=kline.{symbol}.{interval}

### 参数说明
| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 间隔 | interval | 必须，当前支持1m、3m、5m、15m、30m、1h、2h、4h、6h、8h、12h、1d、3d、1w、1M |

### 举例
wss://ws.betaex.com/sub?id=kline.BTC_USDT.1m