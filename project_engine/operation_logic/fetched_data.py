import pyotp
from NorenRestApiPy.NorenApi import NorenApi
from flask import session
from datetime import datetime
import time

class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/',
                          websocket='wss://api.shoonya.com/NorenWSTP/')


import logging

# enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

# start of our program
api = ShoonyaApiPy()


def login_user(user, token, pwd, vc, app_key, imei):
    try:
        ret = api.login(userid=user, password=pwd, twoFA=pyotp.TOTP(token).now(), vendor_code=vc, api_secret=app_key, imei=imei)
        session["ret"] = ret
        session["login_api"] = api
        return ret, api
    except Exception as e:
        print(e)

def buy_order(symbol, quentity):
    ret = api.place_order(buy_or_sell='B', product_type="I",
                          exchange="NFO", tradingsymbol=symbol,
                          quantity=quentity, discloseqty=0, price_type='MKT', price=0, trigger_price=0,
                          retention='DAY', remarks='my_order_001')

    return ret

def sell_order(symbol, quentity):
    ret = api.place_order(buy_or_sell='S', product_type="I", exchange="NFO", tradingsymbol=symbol,
                    quantity=quentity, discloseqty=0, price_type='MKT', price=0,
                    trigger_price=0, retention='DAY', remarks='my_order_001')

    return ret


def gettig_current_price(exchange, token):
    one = api.get_quotes(exchange=exchange, token=token)
    current_price = one["lp"]

    return float(current_price)

def getting_token_number(exchange, symbol):
    ret = api.searchscrip(exchange=exchange, searchtext=symbol)
    token_id = ret["values"][0].get("token")

    return token_id


def di_desi_price_gen(current_price, di_desi_price):
    de_value = di_desi_price+25
    if current_price>=de_value:
        di_desi_price = di_desi_price+50

    if di_desi_price%100 == 0:
        di_make_value = 100
    else:
        di_make_value = 50

    return di_make_value


def main_process(api, exchange, strike_price, symbol,p_l_profit, quentity, target, p_l_loss, target1, target2, target3, count_repeat):
    count = 0
    token_id = getting_token_number(exchange=exchange, symbol=symbol)
    current_price = gettig_current_price(exchange="NFO", token=token_id)
    current_price = str(int(current_price))
    # if int(current_price[3:5]) > 50:
    #     own = current_price[0:2]
    #     one_plus = int(current_price[2]) + 1
    #     new_price = own + str(one_plus) + "00"
    #     di_desi_price = int(new_price)
    # else:
    #     own = current_price[0:3]
    #     new_price = own + "00"
    di_desi_price = int(strike_price)
    flag=True
    while flag:
        pos = api.get_positions()
        if pos:
            p_l = 0
            for own_pos in pos:
                p_l += float(own_pos["rpnl"])
        else:
            p_l = 0
        if p_l >= p_l_loss or p_l<=p_l_profit:
            if count < count_repeat:
                time.sleep(1)
                current_price = gettig_current_price(exchange="NFO", token="62808")
                current_pre_price = gettig_current_pre_price(exchange="NFO", token="62808")
                di_make_value = di_desi_price_gen(current_price, di_desi_price)
                if current_price>=di_desi_price and current_price<=di_desi_price+5:
                    symbol1 = f"{symbol}C{di_desi_price - di_make_value}"
                    ret = buy_order(symbol1, quentity=quentity)
                    count+=1

                    own_flag = True
                    sell_target = []
                    quentity_main = quentity
                    while own_flag:
                        time.sleep(1)
                        current_price1 = gettig_current_price(exchange="NFO", token="62808")
                        if current_price1 >= di_desi_price + target:
                            symbol1 = f"{symbol}C{di_desi_price - di_make_value}"
                            ret_sell = sell_order(symbol1, quentity=quentity_main)
                            own_flag = False
                        # elif target1!=0 and current_price1>=di_desi_price+target1 and current_price1<=di_desi_price+target1+15 and str(target1) not in sell_target:
                        #     symbol1 = f"{symbol}C{di_desi_price - di_make_value}"
                        #     ret_sell = sell_order(symbol1, quentity=25)
                        #     sell_target.append(str(target1))
                        #     quentity_main=quentity_main-25
                        # elif target2!=0 and current_price1>=di_desi_price+target2 and current_price1<=di_desi_price+target2+15 and str(target2) not in sell_target:
                        #     symbol1 = f"{symbol}C{di_desi_price - 100}"
                        #     ret_sell = sell_order(symbol1, quentity=25)
                        #     sell_target.append(str(target2))
                        #     quentity_main=quentity_main-25
                        # elif target3!=0 and current_price1>=di_desi_price+target3 and current_price1<=di_desi_price+target3+15 and str(target3) not in sell_target:
                        #     symbol1 = f"{symbol}C{di_desi_price - 100}"
                        #     ret_sell = sell_order(symbol1, quentity=25)
                        #     sell_target.append(str(target3))
                        #     quentity_main=quentity_main-25
                        elif current_price1 <= di_desi_price-5:
                            symbol1 = f"{symbol}C{di_desi_price - di_make_value}"
                            ret_sell = sell_order(symbol1, quentity=quentity_main)
                            count += 1
                            own_flag = False
                        else:
                            pass

                elif current_price<=di_desi_price-0.05 and current_price>=di_desi_price-5:
                    symbol1 = f"{symbol}P{di_desi_price + 100}"
                    ret = buy_order(symbol1, quentity=quentity)

                    sell_target = []
                    quentity_main = quentity
                    own_flag = True
                    while own_flag:
                        time.sleep(1)
                        current_price2 = gettig_current_price(exchange="NFO", token="62808")
                        if current_price2 <= di_desi_price - target:
                            symbol1 = f"{symbol}P{di_desi_price + 100}"
                            ret_sell = sell_order(symbol1, quentity=quentity_main)
                            di_desi_price = di_desi_price - target
                            count = 0
                            own_flag = False
                        elif target1!=0 and current_price2<=di_desi_price-target1 and current_price2>=di_desi_price-target1-15 and str(target1) not in sell_target:
                            symbol1 = f"{symbol}P{di_desi_price - 100}"
                            ret_sell = sell_order(symbol1, quentity=25)
                            sell_target.append(str(target1))
                            quentity_main=quentity_main-25
                        elif target2!=0 and current_price2<=di_desi_price-target2 and current_price2>=di_desi_price-target2-15 and str(target2) not in sell_target:
                            symbol1 = f"{symbol}P{di_desi_price - 100}"
                            ret_sell = sell_order(symbol1, quentity=25)
                            sell_target.append(str(target2))
                            quentity_main=quentity_main-25
                        elif target3!=0 and current_price2<=di_desi_price-target3 and current_price2>=di_desi_price-target3-15 and str(target3) not in sell_target:
                            symbol1 = f"{symbol}P{di_desi_price - 100}"
                            ret_sell = sell_order(symbol1, quentity=25)
                            sell_target.append(str(target3))
                            quentity_main=quentity_main-25
                        elif current_price2 >= di_desi_price:
                            symbol1 = f"{symbol}P{di_desi_price + 100}"
                            ret_sell = sell_order(symbol1, quentity=quentity_main)
                            count += 1
                            own_flag = False
                        else:
                            pass
                else:
                    pass
            else:
                time.sleep(1)
                current_price = gettig_current_price(exchange="NFO", token="62808")
                count=0
                if current_price >= di_desi_price + 100:
                    di_desi_price = current_price
                elif current_price <= di_desi_price - 100:
                    di_desi_price = current_price
                else:
                    pass
        else:
            time.sleep(1)
            current_price = gettig_current_price(exchange="NFO", token="62808")
            if current_price >= di_desi_price + 100:
                di_desi_price = current_price
            elif current_price <= di_desi_price - 100:
                di_desi_price = current_price
            else:
                pass


    return "process can be complate"



