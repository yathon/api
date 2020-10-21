# 私密接口

私密接口包含签名验证和请求频率限制

## 币币账号余额列表

POST /api/v1/private/balance/list

### 接口说明

1. 此接口用于获取币币账号的每个币种的余额，币币账号用于币币交易
2. BetaEX中币种充值和提币的余额默认放在资金账号，如果需要进行币币交易，需要您先将资金账号的余额划转到币币账号

### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 账号类型 | account_type | 币币账号=trading |

```json
{
  "account_type": "trading",
  "nonce": 1519808456000
}
```

### 返回字段

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

## 币币账号余额详情

POST /api/v1/private/balance

### 参数

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

### 返回字段

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

## 杠杆账号余额列表

POST /api/v1/private/margin/balance/list

### 接口说明

1. 此接口用于获取钱包账号的每个币种的余额，杠杆账号参与于币币交易
2. BetaEX中币种充值和提币的余额默认放在资金账号，如果需要进行币币交易，需要您先将资金账号的余额划转到杠杆账号

### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |

```json
{
  "nonce": 1519808456000
}
```

### 返回字段

#### 交易对余额列表
| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 交易对名称 | symbol |  |
| 净资产等价btc | equal_btc |  |
| 净资产等价cny | equal_cny | |
| 保证金率 | insurance_rate | |
| 强平价格 | liquid_price |  |
| 强平锁定状态 | is_liquid_locked | 0=未锁定  >0=锁定 |  
| 借款精度 | loan_decimal |  |
| 币种余额列表 | currency_list | 列表中包含交易对中两个币种的余额 |

#### 币种余额列表
| 名称        | 字段     |  说明 |
| --------   | -----:   | :----: |
| 币种名称 | currency |  |
| 总余额 | balance |  |
| 可用数量 | avail | |
| 冻结数量 | frozen | |
| 借币数量 | loan |  |
| 累计的利息 | interest |  |  
| 可借数量 | loanable |  |
| 借币日利率 | interest_rate |  |
| 最小借币数量 | min_loan |  |
| 可划转数量 | transferable |  |

```json
{
	"status": 0,
	"msg": "ok",
	"data": [{
		"symbol": "string",
		"equal_btc": 0,
		"equal_cny": 0,
		"insurance_rate": 0,
		"liquid_price": 0,
		"is_liquid_locked": 0,
		"loan_decimal": 2,
		"currency_list": [{
			"currency": "string",
			"balance": 0,
			"avail": 0,
			"frozen": 0,
			"loan": 0,
			"interest": 0,
			"loanable": 0,
			"interest_rate": 0,
			"min_loan": 0,
			"transferable": 0
		}]
	}]
}
```

## 杠杆账号余额详情

POST /api/v1/private/margin/balance

### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 交易对名称 | symbol |  |

```json
{
  "symbol": "BTC_USDT",
  "nonce": 1519808456000
}
```

### 返回字段

```json
{
	"status": 0,
	"msg": "ok",
	"data": {
		"symbol": "string",
		"equal_btc": 0,
		"equal_cny": 0,
		"insurance_rate": 0,
		"liquid_price": 0,
		"is_liquid_locked": 0,
		"loan_decimal": 2,
		"currency_list": [{
			"currency": "string",
			"balance": 0,
			"avail": 0,
			"frozen": 0,
			"loan": 0,
			"interest": 0,
			"loanable": 0,
			"interest_rate": 0,
			"min_loan": 0,
			"transferable": 0
		}]
	}
}
```

## 订单创建

POST /api/v1/private/order/create

### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 客户端订单ID | cid | 必须，不可重复，未来扩展功能 |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 交易方向 | side | 必须，买入='buy', 卖出='sell'|
| 价格 | price | 必须，价格限制由所选的交易对决定 |
| 数量 | qty  | 必须，数量限制由所选的交易对决定 |
| 交易类型 | type | 必须，当前仅支持限价交易, 限价='limit' |
| 账号类型 | account_type | 可选，默认'trading'. 币币账号=trading，杠杆账号=margin |

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

### 响应数据

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

### 状态码

## 订单详情

POST /api/v1/private/order/state

### 参数

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

## 返回值

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
| 成交总额 | filled_amount | |
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
        "filled_amount": 0.0,
        "filled_qty": 0.0,
        "maker_fee": 0.0,
        "taker_fee": 0.0,
        "update_tm_ms": 1571737204000,
        "create_tm_ms": 1571737204000
    }
}
```

## 订单取消

POST /api/v1/private/order/cancel

### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 订单ID | order_id |  |
| 交易对名称 | symbol | |
| 账号类型 | account_type | 可选，默认'trading'. 币币账号=trading，杠杆账号=margin |

```json
{
  "symbol": "BTC_USDT",
  "order_id": "BTC_USDT.buy.82b75796f17811e9acb4acde48001122.1571383550293",
  "nonce": 1519808456000
}
```

### 响应数据

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

## 活跃订单列表

POST /api/v1/private/order/active/list

### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 交易方向 | side | 可选，买入='buy', 卖出='sell'，默认查询所有交易状态 |
| 订单状态 | state | 可选，未完成订单状态中的一个，默认查询所有未完成状态的订单 |
| 起始时间 | start_tm_ms | 毫秒时间戳，可选，默认最小时间戳 |
| 截止时间 | end_tm_ms | 毫秒时间戳，可选，默认当前时间戳 |
| 请求数量 | limit | 可选，默认20，最大100，创建时间降序排列 |
| 账号类型 | account_type | 可选，默认'trading'. 币币账号=trading，杠杆账号=margin |

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

### 返回数据

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
| 成交总额 | filled_amount | |
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

## 历史订单列表

POST /api/v1/private/order/history/list

### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 交易方向 | side | 可选，买入='buy', 卖出='sell'，默认查询所有交易状态 |
| 订单状态 | state | 可选，完成订单状态中的一个，默认查询所有完结状态的订单 |
| 起始时间 | start_tm_ms | 毫秒时间戳，可选，默认最小时间戳 |
| 截止时间 | end_tm_ms | 毫秒时间戳，可选，默认当前时间戳 |
| 请求数量 | limit | 可选，默认20，最大100，创建时间降序排列 |
| 账号类型 | account_type | 可选，默认'trading'. 币币账号=trading，杠杆账号=margin |

```json
{
  "symbol": "BTC_USDT",
  "side": " buy",
  "state": "filled",
  "start_tm_ms": 1519808456000,
  "end_tm_ms": 1519808456000,
  "limit": 20,
  "nonce": 1519808456000
}
```

### 返回字段

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
| 成交总额 | filled_amount | |
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
        "filled_amount": 0.0,
        "filled_qty": 0.0,
        "maker_fee": 0.0,
        "taker_fee": 0.0,
        "source": "api",
        "update_tm_ms": 1571737204337,
        "create_tm_ms": 1571737204337
    }]
}
```

## 交易历史

POST /api/v1/private/trade/list

### 参数

| 名称 | 字段 | 说明 |
| -------- | -----: | :----: |
| 交易对名称 | symbol | 必须，通过交易对列表获取支持的交易对 |
| 起始时间 | start_tm_ms | 毫秒时间戳，可选，默认最小时间戳 |
| 截止时间 | end_tm_ms | 毫秒时间戳，可选，默认当前时间戳 |
| 请求数量 | limit | 可选，默认20，最大100，创建时间降序排列 |
| 账号类型 | account_type | 可选，默认'trading'. 币币账号=trading，杠杆账号=margin |

```json
{
  "symbol": "BTC_USDT",
  "start_tm_ms": 1519808456000,
  "end_tm_ms": 1519808456000,
  "limit": 20,
  "nonce": 1519808456000
}
```

### 返回字段

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
