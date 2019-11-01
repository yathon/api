# 成交记录

GET /api/v1/public/market/trade/{symbol}

## 参数说明

| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |

## 举例

GET https://market.betaex.com/api/v1/public/market/trade/BTC_USDT

```json
{
    "status": 0,
    "msg": "ok",
    "data": [
        {
            "trade_id": "52220f42fb8a11e9b84c02a7107ba21a",
            "side": "sell",
            "price": 10060.4,
            "qty": 0.001,
            "ts": 1572490711353
        },
        {
            "trade_id": "dc84492cfb2e11e9b84c02a7107ba21a",
            "side": "sell",
            "price": 10060.0,
            "qty": 0.01,
            "ts": 1572451429823
        }
    ]
}
```
