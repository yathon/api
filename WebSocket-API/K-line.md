# k线

/sub?id=kline.{symbol}.{interval}

## 参数说明

| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 间隔 | interval | 必须，当前支持1m、3m、5m、15m、30m、1h、2h、4h、6h、8h、12h、1d、3d、1w、1M |

## 举例

wss://ws.betaex.com/sub?id=kline.BTC_USDT.1m
