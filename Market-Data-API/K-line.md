# k线

GET /api/v1/public/market/kline/{symbol}/{interval}

## 参数说明

| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 间隔 | interval | 必须，当前支持1m、3m、5m、15m、30m、1h、2h、4h、6h、8h、12h、1d、3d、1w、1M |
| 起始时间戳,秒 | begin | 必须 |
| 终止时间戳,秒 | end | 必须 |

## 举例

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
