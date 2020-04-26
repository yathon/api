# 公开接口

## 交易对列表

POST /api/v1/public/symbols

### 返回字段

| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol |  |
| 价格精度 | price_decimal |  |
| 数量精度 | qty_decimal | |
| 状态 | state | 已上架=1，可交易=2|
| 最小数量限制 | limit_qty_min |  |
| 最大数量限制 | limit_qty_max |  |
| 最小总价限制 | limit_amount_min |  |
| 最大总价限制 | limit_amount_max |  |
| 最大总价限制 | limit_amount_max |  |
| 是否支持杠杆交易 | is_support_margin | 0=不支持 1=支持 |
| 是否为主板交易对 | is_main | false=不是 true=是 |
| 是否为指数交易对 | is_index | false=不是 true=是 |
| 是否为创新校对对 | is_innovate | false=不是 true=是 |


```json
{
    "status": 0,
    "msg": "ok",
    "data": [{
        "symbol": "BTC_USDT",
        "price_decimal": 2,
        "qty_decimal": 4,
        "state": 2,
        "limit_qty_min": 0.001,
        "limit_qty_max": 1000.0,
        "limit_amount_min": 1000.0,
        "limit_amount_max": 1000000.0,
        "is_support_margin": 1,
        "is_main": true,
        "is_index": false,
        "is_innovate": false
    }]
}
```

## 币种列表

POST /api/v1/public/currencies

### 返回字符

| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 币名 | currency |  |
| 链名 | chain_name |  |
| 币的全名 | full_name | |
| 是否支持memo | is_memo_support | 支持=1，不支持=0 |
| 最小提币金额 | min_withdraw_amount |  |
| 最小充值金额 | min_deposit_amount |  |
| 提币费用 | withdraw_fee | 当前币种为单位 |
| 充值确认数 | exchange_confirm |  |
| 提币确认数 | withdraw_confirm |  |
| 链上精度 | decimal |  |
| 是否可充值 | is_depositable |  |
| 是否可提币 | is_withdrawable |  |

```json
{
    "status": 0,
    "msg": "ok",
    "data": [{
        "currency": "ETH",
        "chain_name": "ETH",
        "full_name": "ETH",
        "is_memo_support": 0,
        "min_withdraw_amount": 0.0001,
        "min_deposit_amount": 0.0001,
        "withdraw_fee": 0.0001,
        "exchange_confirm": 12,
        "withdraw_confirm": 12,
        "decimal": 18,
        "is_depositable": 1,
        "is_withdrawable": 1
    }]
}
```

## 获取指数价格
GET /api/v1/public/index/{symbol}

### 参数说明

| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol | 指数交易对名称 |

### 返回字段

| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol |  |
| 指数价格 | index_price |  |
| 指数价格对应的时间戳 | timestamp_ms | 毫秒，UTC时间 |
| 生成指数价格的各数据源权重 | reference_weight | 当前此字段为null |

### 举例
GET https://api.betaex.com/api/v1/public/index/PT05_USDT

返回值：
```json
{
	"status": 0,
	"msg": "ok",
	"data": {
		"symbol": "PT05_USDT",
		"index_price": 0.7899,
		"timestamp_ms": 1587903200000,
		"reference_weight": null
	}
}
```
