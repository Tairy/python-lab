# encoding:utf-8
from es import es


def get_tagged_logs():
    query_json = {
        "bool": {
            "must": [
                {
                    "exists": {"field": "tags"}
                }
            ]
        }
    }

    sort_json = [
        {
            "dt": {
                "order": "desc"
            }
        }
    ]

    res = es.search(index="app-server-log-prod-*",
                    body={"query": query_json, "sort": sort_json, "size": 5000, "from": 0})

    hits = res['hits']['hits']

    return hits


def get_origin_data():
    query_json = {
        "bool": {
            "must": [
                {
                    "match": {
                        "an": "sqkb-api-v2"
                    }
                },
                {
                    "match": {
                        "ll": "ERROR"
                    }
                }
            ]
        }
    }

    sort_json = [
        {
            "dt": {
                "order": "desc"
            }
        }
    ]

    res = es.search(index="app-server-log-prod-*",
                    body={"query": query_json, "sort": sort_json, "size": 2000, "from": 10000},
                    request_timeout=500)

    hits = res['hits']['hits']

    return hits


if __name__ == "__main__":
    logs = get_origin_data()
    for log in logs:
        error_message = log['_source']['em'].replace("\n", " ")
        if error_message.startswith('RecommendService') or 'RecommendService.php' in error_message:
            tag = 'recommend_service_timeout'
        elif error_message.startswith('call abservice error') or error_message.startswith(
                'shopping cart ab Operation timed') or error_message.startswith(
            'shopping cart ab Connection timed') or error_message.startswith(
            ' Operation timed out after 100 milliseconds '
            'with 0 out of -1 bytes received [{"file":"'
            '/home/www-data/sqkb-api-v2/vendor/arch/php-json-rpc/'
            'src/ABService.php"'
        ):
            tag = 'ab_service_timeout'
        elif error_message.startswith('HotCouponService'):
            tag = 'hot_coupon_service_timeout'
        elif error_message.startswith('OrderService') or error_message.startswith(
                'resend multi redPack msg failed cURL error 28'):
            tag = 'order_service_timeout'
        elif error_message.startswith('RebateService'):
            tag = 'rebate_service_error'
        elif error_message.startswith('SearchServiceRpc'):
            tag = 'search_service_error'
        elif error_message.startswith('ShopInfoService'):
            tag = 'shop_info_service_timeout'
        elif error_message.startswith('CouponCenter'):
            tag = 'coupon_center_service_timeout'
        elif error_message.startswith('get collect info') or error_message.startswith(
                'collect failed cURL error') or error_message.startswith(
            'collect cancel failed cURL error 28') or error_message.startswith(
            'get collect history failed cURL error 28'
        ):
            tag = 'collect_service_timeout'
        elif error_message.startswith(' SQLSTATE'):
            tag = 'sql_error'
        elif error_message.startswith('get stay open redPack failed') or error_message.startswith(
                'get user redPackTotalAmount'):
            tag = 'bonus_service_timeout'
        elif error_message.startswith('UserServiceRpc checkMobileBindHistory exception cURL error'):
            tag = 'user_service_timeout'
        elif error_message.startswith('getWechatUserInfo Exception cURL error '):
            tag = 'http_request_time_out'
        else:
            tag = 'unknown'

        dict_file = open("dataset/" + tag + ".txt", "a")
        dict_file.write(error_message + "\n")
        dict_file.close()
