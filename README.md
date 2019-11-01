# 交易api

## API说明

### 服务地址

https://api.betaex.com

### 签名认证

1. 如果您没有API_KEY_ID和API_KEY_SECRET，请前往个人中心申请
2. 使用密钥API_KEY_SECRET和算法hmac对消息体进行SHA512签名，获取HEX格式字符串作为签名结果

#### 密钥

1. API_KEY_SECRET转为字节

#### 被签名的数据

1. 被签名的数据主要是放在消息体中的json参数
2. 必须包含时间参数nonce，值为毫秒时间戳
3. 将消息体转为字节

```json
// 签名数据json示例
{
  "param_1_key": "param_1_value",
  "nonce": 1519808456000
}
```

#### 签名示例python伪代码

```python
import json
import hmac
import requests

from hashlib import sha512

API_KEY_ID = ''
API_KEY_SECRET = ''

# 必需时间参数nonce
params = {
    "nonce": 1519808456000
}

params_str = json.dumps(params, separators=(',', ':'))

signature = hmac.new(API_KEY_SECRET.encode('utf8'), params_str.encode('utf8'), sha512).hexdigest()

headers = {
    'api_key': API_KEY_ID,
    'signature': signature
}
url = ''
ret = requests.post(url, json=None, data=params_str, headers=headers, cookies=None)

```

#### 请求Header

1. api_key: API_KEY_ID
2. signature: 签名结果

### 请求频率限制

默认10秒内最大请求量100

### 接口响应

1. 所有接口返回数据均为application/json
2. status=0表示成功, 其他状态参考具体的接口
3. data存放需要返回具体的数据，如果无需返回数据，data可能不存在

```json
{
    "status": 0,
    "msg": "ok",
    "data": {}
  }
```

## 公开接口

### 交易对列表

POST /api/v1/public/symbols

#### 返回字段

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
        "limit_amount_max": 1000000.0
    }]
}
```

### 币种列表

/api/v1/public/currencies

#### 返回字符

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

## 私密接口

私密接口包含签名验证和请求频率限制

### 余额列表

POST /api/v1/private/balance/list

#### 接口说明

1. 此接口用于获取币币账号的每个币种的余额，币币账号用于币币交易
2. betaex中币种充值和提币的余额默认放在资金账号，如果需要进行币币交易，需要您先将资金账号的余额划转到币币账号

#### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 账号类型 | account_type | 币币账号=trading |

```json
{
  "account_type": "trading",
  "nonce": 1519808456000
}
```

#### 返回字段

| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 币名 | currency |  |
| 可用余额 | avail |  |
| 冻结余额 | frozen | |
| 总余额 | balance | |
| 币种链上精度 | decimal |  |

```json
{
    "status": 0,
    "msg": "ok",
    "data": [{
        "currency": "BTC",
        "avail": 998.9842,
        "frozen": 0.0,
        "balance": 998.9842,
        "decimal": 8
    }]
}
```

### 余额详情

POST /api/v1/private/balance

#### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 账号类型 | account_type | 当前仅支持币币账号余额查询，币币账号=trading |
| 币名 | currency |  |

```json
{
  "currency": "BTC",
  "account_type": "trading",
  "nonce": 1519808456000
}
```

#### 返回字段

```json
{
    "status": 0,
    "msg": "ok",
    "data": {
        "currency": "BTC",
        "avail": 998.9842,
        "frozen": 0.0,
        "balance": 998.9842
    }
}
```

### 订单创建

POST /api/v1/private/order/create

#### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 客户端订单ID | cid | 必须，不可重复，未来扩展功能 |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 交易方向 | side | 必须，买入='buy', 卖出='sell'|
| 价格 | price | 必须，价格限制由所选的交易对决定 |
| 数量 | qty  | 必须，数量限制由所选的交易对决定 |
| 交易类型 | type | 必须，当前仅支持限价交易, 限价='limit' |

```json
{
  "cid": "33c394def0af11e980edacde48001122",
  "symbol": "BTC_USDT",
  "side": "buy",
  "price": 100.00,
  "qty": 100.00,
  "type": "limit",
  "nonce": 1519808456000
}
```

#### 响应数据

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 订单ID | order_id | 可用于订单详情查询 |
| 订单状态 | state | 具体状态见下表 |

订单状态说明：  

| 订单状态值 | 说明 |
| -------- | :----: |
| pending_submit | 提交中 |
| submitted | 提交完成 |
| partial_filled | 部分成交 |
| partial_canceled | 部分取消 |
| filled | 已成交 |
| pending_cancel | 取消处理中 | |
| canceled | 已取消 |
| sys_canceled | 系统取消 |

- 活动订单状态
  - pending_submit
  - submitted
  - partial_filled
- 完结订单状态
  - partial_canceled
  - filled
  - canceled
  - sys_canceled

```json
{
    "status": 0,
    "msg": "ok",
    "data": {
        "order_id": "BTC_USDT.buy.82b75796f17811e9acb4acde48001122.1571383550293",
        "state": "pending_submit"
    }
}
```

#### 状态码

### 订单详情

POST /api/v1/private/order/state

#### 参数

| 名称 | 字段 | 说明 |
| --------   | -----:   | :----: |
| 订单ID | order_id |  |
| 交易对名称 | symbol | |

```json
{
  "symbol": "BTC_USDT",
  "order_id": "BTC_USDT.buy.82b75796f17811e9acb4acde48001122.1571383550293",
  "nonce": 1519808456000
}
```

### 返回值

| 名称 | 字段 | 说明 |
| --------   | -----:   | :----: |
| 订单ID | order_id |  |
| 客户端订单ID | cid |  |
| 交易对名称 | symbol | |
| 交易方向 | side | 买入='buy', 卖出='sell'|
| 交易类型 | type | 当前仅支持限价交易, 限价='limit' |
| 价格 | price | |
| 数量 | qty  |  |
| 订单状态 | state | |
| 订单总额 | amount | |
| 成交总额 | executed_amount | |
| 成交数量 | filled_qty | |
| 挂单费用 | maker_fee | |
| 吃单费用 | taker_fee | |
| 更新时间 | update_tm_ms | 毫秒时间戳 |
| 创建时间 | create_tm_ms | 毫秒时间戳 |

```json
{
    "status": 0,
    "msg": "ok",
    "data": {
        "order_id": "BTC_USDT.buy.ecf07180f4af11e9812dacde48001122.1571737204314",
        "cid": "cid_ece71d74f4af11e9b16aacde48001122",
        "symbol": "BTC_USDT",
        "side": "buy",
        "type": "limit",
        "qty": 1.3,
        "price": 11000.0,
        "state": "pending_submit",
        "amount": 14300.0,
        "executed_amount": 0.0,
        "filled_qty": 0.0,
        "maker_fee": 0.0,
        "taker_fee": 0.0,
        "update_tm_ms": 1571737204000,
        "create_tm_ms": 1571737204000
    }
}
```

### 订单取消

POST /api/v1/private/order/cancel

#### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 订单ID | order_id |  |
| 交易对名称 | symbol | |

```json
{
  "symbol": "BTC_USDT",
  "order_id": "BTC_USDT.buy.82b75796f17811e9acb4acde48001122.1571383550293",
  "nonce": 1519808456000
}
```

#### 响应数据

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 订单ID | order_id | 可用于订单详情查询 |
| 订单状态 | state |  |

```json
{
    "status": 0,
    "msg": "ok",
    "data": {
        "order_id": "BTC_USDT.buy.82b75796f17811e9acb4acde48001122.1571383550293",
        "state": "pending_submit"
    }
}
```

### 活跃订单列表

POST /api/v1/private/order/active/list

#### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 交易方向 | side | 可选，买入='buy', 卖出='sell'，默认查询所有交易状态 |
| 订单状态 | state | 可选，完结订单状态中的一个，默认查询所有完结状态的订单 |
| 起始时间 | start_tm_ms | 毫秒时间戳，可选，默认最小时间戳 |
| 截止时间 | end_tm_ms | 毫秒时间戳，可选，默认当前时间戳 |
| 请求数量 | limit | 可选，默认20，最大100，创建时间降序排列 |

```json
{
  "symbol": "BTC_USDT",
  "side": " buy",
  "state": "pending_submit",
  "start_tm_ms": 1519808456000,
  "end_tm_ms": 1519808456000,
  "limit": 20,
  "nonce": 1519808456000
}
```

#### 返回数据

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 订单ID | order_id |  |
| 客户端订单ID | cid |  |
| 交易对名称 | symbol | |
| 交易方向 | side | 买入='buy', 卖出='sell'|
| 交易类型 | type | 当前仅支持限价交易, 限价='limit' |
| 价格 | price | |
| 数量 | qty  |  |
| 订单状态 | state | |
| 订单总额 | amount | |
| 成交总额 | executed_amount | |
| 成交数量 | filled_qty | |
| 挂单费用 | maker_fee | |
| 吃单费用 | taker_fee | |
| 来源 | source | 'web'或 'api'|
| 更新时间 | update_tm_ms | 毫秒时间戳 |
| 创建时间 | create_tm_ms | 毫秒时间戳 |

```json
{
    "status": 0,
    "msg": "ok",
    "data": [{
        "order_id": "BTC_USDT.buy.ecf07180f4af11e9812dacde48001122.1571737204314",
        "cid": "cid_ece71d74f4af11e9b16aacde48001122",
        "symbol": "BTC_USDT",
        "side": "buy",
        "type": "limit",
        "qty": 1.3,
        "price": 11000.0,
        "state": "pending_submit",
        "amount": 14300.0,
        "executed_amount": 0.0,
        "filled_qty": 0.0,
        "maker_fee": 0.0,
        "taker_fee": 0.0,
        "source": "api",
        "update_tm_ms": 1571737204337,
        "create_tm_ms": 1571737204337
    }]
}
```

### 历史订单列表

POST /api/v1/private/order/history/list

#### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 交易方向 | side | 可选，买入='buy', 卖出='sell'，默认查询所有交易状态 |
| 订单状态 | state | 可选，完结订单状态中的一个，默认查询所有完结状态的订单 |
| 起始时间 | start_tm_ms | 毫秒时间戳，可选，默认最小时间戳 |
| 截止时间 | end_tm_ms | 毫秒时间戳，可选，默认当前时间戳 |
| 请求数量 | limit | 可选，默认20，最大100，创建时间降序排列 |

```json
{
  "symbol": "BTC_USDT",
  "side": " buy",
  "state": "pending_submit",
  "start_tm_ms": 1519808456000,
  "end_tm_ms": 1519808456000,
  "limit": 20,
  "nonce": 1519808456000
}
```

#### 返回字段

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 订单ID | order_id |  |
| 客户端订单ID | cid |  |
| 交易对名称 | symbol | |
| 交易方向 | side | 买入='buy', 卖出='sell'|
| 交易类型 | type | 当前仅支持限价交易, 限价='limit' |
| 价格 | price | |
| 数量 | qty  |  |
| 订单状态 | state | |
| 订单总额 | amount | |
| 成交总额 | executed_amount | |
| 成交数量 | filled_qty | |
| 挂单费用 | maker_fee | |
| 吃单费用 | taker_fee | |
| 来源 | source | 'web'或 'api'|
| 更新时间 | update_tm_ms | 毫秒时间戳 |
| 创建时间 | create_tm_ms | 毫秒时间戳 |

```json
{
    "status": 0,
    "msg": "ok",
    "data": [{
        "order_id": "BTC_USDT.buy.ecf07180f4af11e9812dacde48001122.1571737204314",
        "cid": "cid_ece71d74f4af11e9b16aacde48001122",
        "symbol": "BTC_USDT",
        "side": "buy",
        "type": "limit",
        "qty": 1.3,
        "price": 11000.0,
        "state": "pending_submit",
        "amount": 14300.0,
        "executed_amount": 0.0,
        "filled_qty": 0.0,
        "maker_fee": 0.0,
        "taker_fee": 0.0,
        "source": "api",
        "update_tm_ms": 1571737204337,
        "create_tm_ms": 1571737204337
    }]
}
```

### 交易历史

POST /api/v1/private/trade/list

#### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 起始时间 | start_tm_ms | 毫秒时间戳，可选，默认最小时间戳 |
| 截止时间 | end_tm_ms | 毫秒时间戳，可选，默认当前时间戳 |
| 请求数量 | limit | 可选，默认20，最大100，创建时间降序排列 |

```json
{
  "symbol": "BTC_USDT",
  "start_tm_ms": 1519808456000,
  "end_tm_ms": 1519808456000,
  "limit": 20,
  "nonce": 1519808456000
}
```

#### 返回字段

| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易id | id |  |
| 订单ID | order_id |  |
| 交易对名称 | symbol | |
| 交易方向 | side | 买入='buy', 卖出='sell'|
| 交易类型 | type | 当前仅支持限价交易, 限价='limit' |
| 价格 | price | |
| 数量 | qty  |  |
| 交易总额 | amount | |
| 是否买入为挂单 | is_buy_maker | |
| 卖出费用 | qty_fee | |
| 买入费用 | amount_fee | |
| 创建时间 | create_tm_ms | 毫秒时间戳 |

```json
{
    "status": 0,
    "msg": "ok",
    "data": [{
        "id": 575,
        "symbol": "BTC_USDT",
        "price": 12000.0,
        "qty": 1.0,
        "amount": 12000.0,
        "is_buy_maker": 0,
        "create_tm_ms": 1569034615064,
        "order_id": "BTC_USDT.buy.7521f48cdc1b11e996ddacde48001122",
        "qty_fee": 0.002,
        "amount_fee": 0.0,
        "type": "limit",
        "side": "buy"
    }]
}
```

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