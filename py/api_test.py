'''
Created on Jul 10, 2019

@author: gjwang
'''
import json
import unittest
from time import sleep

from py.awsex_client import AwsexApiKeyClient


ORDER_STATE_PENDING_SUBMIT_STR   = 'pending_submit'
ORDER_STATE_SUBMITTED_STR        = 'submitted'
ORDER_STATE_PARTIAL_FILLED_STR   = 'partial_filled'
ORDER_STATE_PARTIAL_CANCELED_STR = 'partial_canceled'
ORDER_STATE_FILLED_STR           = 'filled'
ORDER_STATE_CANCELED_STR         = 'canceled'
ORDER_STATE_PENDING_CANCEL_STR   = 'pending_cancel'
ORDER_STATE_SYS_CANCELED_STR     = 'sys_canceled'

ORDER_STATE_OPEN = (ORDER_STATE_PENDING_SUBMIT_STR, ORDER_STATE_SUBMITTED_STR, ORDER_STATE_PARTIAL_FILLED_STR,
                    ORDER_STATE_PENDING_CANCEL_STR)
ORDER_STATE_CLOSED = (ORDER_STATE_PARTIAL_CANCELED_STR, ORDER_STATE_FILLED_STR,
                      ORDER_STATE_CANCELED_STR, ORDER_STATE_SYS_CANCELED_STR,
                      )


STATUS_SUCCESS = 0


SYMBOL = 'BTC_USDT'
API_BASE_URL = ''
API_KEY = ''
API_SECRET = ''


class ApiKeyTest(unittest.TestCase):
    def setUp(self):
        self.symbol = SYMBOL
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.awsex_client = AwsexApiKeyClient(API_BASE_URL, self.api_key, self.api_secret)

    # 获取服务器时间戳
    def testPublicTimestampMs(self):
        ret = self.awsex_client.get_timestamp_ms()
        print('testPublicTimestampMs ret=', str(ret.text))
        result = json.loads(ret.text)
        self.assertEqual(result['status'], STATUS_SUCCESS)
        data = result['data']
        self.assertIn('timestamp_ms', data, 'should return timestamp_ms')
        self.assertEqual(len(str(data['timestamp_ms'])), 13, 'timestamp in ms')

    # 获取交易对列表
    def testPublicSymbols(self):
        ret = self.awsex_client.get_symbols()
        print('testPublicSymbols ret=', str(ret.text))
        result = json.loads(ret.text)
        self.assertEqual(result['status'], STATUS_SUCCESS)
        
        ret = self.awsex_client.get_symbols(method='POST')
        print('testPublicSymbols ret=', str(ret.text))
        result = json.loads(ret.text)
        self.assertEqual(result['status'], STATUS_SUCCESS)

    # 签名测试
    def testSignature(self):
        ret = self.awsex_client.signature_test()
        print('testSignature ret=', str(ret.text))
        result = json.loads(ret.text)
        self.assertEqual(result['status'], STATUS_SUCCESS)
        data = result['data']
        self.assertEqual(data['auth'], 'pass')
        self.assertEqual(data['source'], 'api')

    # 获取一个余额
    def testGetBalance(self):
        ret = self.awsex_client.get_balance()
        print('testGetBalance ret=', str(ret.text))
        result = json.loads(ret.text)
        self.assertEqual(result['status'], STATUS_SUCCESS)

    # 获取余额列表
    def testListBalance(self):
        ret = self.awsex_client.list_balance()
        print('testGetBalance ret=', str(ret.text))
        result = json.loads(ret.text)
        self.assertEqual(result['status'], STATUS_SUCCESS)

    # 创建订单
    def testCreateOrder(self):
        data = self.create_order()
        self.assertTrue(data['state'] == ORDER_STATE_PENDING_SUBMIT_STR)

    # 创建并取消订单
    def testOrderCreateQueryCancel(self):
        delay_time_sec = 0.5
        for _ in range(1):
            # 创建订单
            data = self.create_order()
            self.assertTrue(data['state'] == ORDER_STATE_PENDING_SUBMIT_STR)

            # 查询订单状态
            order_id = data['order_id']
            sleep(delay_time_sec)
            data = self.get_order_state(order_id)
            self.assertTrue(data['state'] == ORDER_STATE_SUBMITTED_STR)

            # 取消订单
            sleep(delay_time_sec)
            data = self.cancel_order(order_id)
            self.assertTrue(data['state'] == ORDER_STATE_PENDING_CANCEL_STR)

            # 查询订单状态
            sleep(0.5)
            data = self.get_order_state(order_id)
            self.assertTrue(data['state'] == ORDER_STATE_CANCELED_STR)

    # 查询活跃订单列表
    def testListActiveOrder(self):
        self.list_active_order()

    # 查询完结订单列表
    def testListHistoryOrder(self):
        self.list_history_order()

    # 查询交易记录列表
    def testListTrade(self):
        self.list_trade()

    def create_order(self):
        symbol = SYMBOL
        side = 'buy'
        qty = 1.3
        price = 11000.0
        _type = 'limit'

        ret = self.awsex_client.create_order(symbol, side, qty, price, _type=_type)
        print('create_order ret=', str(ret.text))
        result = json.loads(ret.text)
        self.assertEqual(result['status'], STATUS_SUCCESS)
        self.assertTrue(result['data'])
        data = result['data']
        return data

    def get_order_state(self, order_id):
        ret = self.awsex_client.get_order_state(order_id, self.symbol)
        result = json.loads(ret.text)
        print('get_order_state', result)

        self.assertEqual(result['status'], STATUS_SUCCESS)
        self.assertTrue(result['data'])
        data = result['data']
        return data

    def cancel_order(self, order_id):
        ret = self.awsex_client.cancel_order(order_id, self.symbol)
        print('cancel_order', ret.text)

        result = json.loads(ret.text)
        self.assertEqual(result['status'], STATUS_SUCCESS)
        self.assertTrue(result['data'])
        data = result['data']
        return data

    def list_active_order(self):
        ret = self.awsex_client.list_active_order(SYMBOL)

        print('list_active_order', ret.text)

        result = json.loads(ret.text)
        self.assertEqual(result['status'], STATUS_SUCCESS)
        data = []
        if 'data' in result:
            data = result['data']
        return data

    def list_history_order(self):
        ret = self.awsex_client.list_history_order(SYMBOL)

        print('list_history_order', ret.text)

        result = json.loads(ret.text)
        self.assertEqual(result['status'], STATUS_SUCCESS)
        data = []
        if 'data' in result:
            data = result['data']
        return data

    def list_trade(self):
        ret = self.awsex_client.list_trade(SYMBOL)

        print('list_trade', ret.text)

        result = json.loads(ret.text)
        data = []
        if 'data' in result:
            data = result['data']
        return data


if __name__ == "__main__":
    unittest.main()
