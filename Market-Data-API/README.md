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

参考 [TradeRecord.md](./TradeRecord.md)

## 盘口

参考 [Handicap.md](./Handicap.md)

## k线

参考 [K-line.md](./K-line.md)
