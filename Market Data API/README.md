# 行情API

## API说明

### 服务地址

https://market.betaex.com

## 活跃订单簿

GET /api/v1/public/market/orderbook/{symbol}/{level}

### 参数说明
| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 交易级别 | level | 必须，当前仅支持ALL, 其他将被支持的级别L20、L50 |

### 举例

GET https://market.betaex.com/api/v1/public/market/orderbook/BTC_USDT/ALL
```json
{
    "status": 0,
    "msg": "ok",
    "data": {
        "type": "depth.ALL.BTC_USDT",
        "symbol": "BTC_USDT",
        "ts": 1572490711353,  // 时间戳
        "seq": 1572448705737, // 序号
        "asks": [
            10060.5, // 卖一价
            0.001,   // 卖一量
            10060.9, // 卖二价
            0.01    // 卖二量
        ],
        "bids": [
            10060.4, // 买一价
            0.009,   // 买一量
            10060.3, // 买二价
            0.01     // 买二量
        ]
    }
}
```

## 成交记录
GET /api/v1/public/market/trade/{symbol}
### 参数说明
| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |

### 举例
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

## 盘口
GET /api/v1/public/market/ticker/{symbol}

### 参数说明
| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
### 举例
GET https://market.betaex.com/api/v1/public/market/ticker/BTC_USDT
```json
{
    "status": 0,
    "msg": "ok",
    "data": {
        "type": "ticker.BTC_USDT",
        "seq": 25,
        "ticker": [
            14000.0,   // 最新一笔成交的成交价
            0.04,      // 最近一笔成交的成交量
            16000.0,   // 最大卖一价
            1.0,       // 最大卖一量
            15000.0,   // 最小买一价
            0.510964,  // 最小买一量
            11.0,      // 24小时前成交价
            14000.0,   // 24小时内最高价
            11.0,      // 24小时内最低价
            1.233,     // 24小时内基准货币成交量
            2845.06118 // 24小时内计价货币成交量
        ]
    }
}
```
## k线
GET /api/v1/public/market/kline/{symbol}/{interval}
### 参数说明
| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 间隔 | interval | 必须，当前支持1m、3m、5m、15m、30m、1h、2h、4h、6h、8h、12h、1d、3d、1w、1M |
| 起始时间戳,秒 | begin | 必须 |
| 终止时间戳,秒 | end | 必须 |
### 举例
GET https://market.betaex.com/api/v1/public/market/kline/BTC_USDT/1m?begin=1572492685&end=1572499129
```json
{
    "status": 0,
    "msg": "ok",
    "data": [     // 按时间升序排序
        {
            "symbol": "BTC_USDT",
            "kline_interval": "1m",
            "kline_interval_sec": 60,
            "kline_key": "kline.BTC_USDT.1m",
            "id": 1572498120,// k线时间段
            "seq": 10,       // 序号
            "high": 14000.0, // 最高价
            "low": 10060.5,  // 最低价
            "open": 10060.5, // 起始价
            "close": 14000.0,// 结束价
            "count": 7,  // 成交笔数
            "base_vol": 0.161, //基准货币成交量
            "quote_vol": 2111.2795, // 计价货币成交量
            "laste_update_tm": 0,
            "last_update_tm_ms": 1572498135957
        }
    ]
}
```
