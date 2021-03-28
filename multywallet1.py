#!flask/bin/python
# -*- coding: utf8 -*-
from flask import Flask, request, jsonify, Response, redirect, flash, make_response
from flask_restx import Api, Resource, fields
from flask import render_template, url_for
from flask_cors import CORS, cross_origin
import uuid
import time
from datetime import datetime, timedelta
# Подключаем библиотеку для работы с базами данных PostgreSQL:
import psycopg2
from catboost import CatBoostRegressor
import json
import requests
import os

from cosmospy import generate_wallet, seed_to_privkey, privkey_to_pubkey, pubkey_to_address
from mnemonic import Mnemonic

#from pywallet import wallet

from eth_account import Account
from eth_wallet import Wallet
from eth_wallet.utils import generate_entropy
from web3 import Web3, IPCProvider

import base64

from py_crypto_hd_wallet import HdWallet, HdWalletFactory, HdWalletSaver, HdWalletCoins, HdWalletWordsNum, HdWalletDataTypes

import binascii
from bip_utils import Bip44, Bip44Coins, Bip44Changes

import pyetherbalance 

from eth_tester import EthereumTester

from hexbytes import HexBytes

# Библиотеки для организации Websocket-соединений
import asyncio
from jsonrpc_websocket import Server
from aiohttp_json_rpc import JsonRpcClient

import websockets
from jsonrpcclient.clients.websockets_client import WebSocketsClient

import sys

from websocket import create_connection
import websocket

from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet, AtomMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional


app_dir = os.path.abspath(os.path.dirname(__file__))

#from flask_swagger_ui import get_swaggerui_blueprint

flask_app = Flask(__name__)
flask_app.secret_key = 'secret'

app_api = Api(app = flask_app, 
		  version = "1.0", 
		  title = "Cosmos wallet", 
		  description = "Мульти валютный онлайн-кошелек блокчейн сетей",
      static_folder="static",
      validate=True)

CORS(flask_app)
      
#CORS(flask_app, resources={r"/api/1.0/*": {"Access-Control-Allow-Origin": "*"}})
#CORS(app, resources=r'/api/*')
#app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

xdbname='walletdb'
xuser='alex'
xpassword='911alex'
xhost='localhost'

name_space__newauth = app_api.namespace('api/1.0/newauth', description='API / Версия API / API-авторизации нового пользователя в системе мультивалютного блокчейн-кошелька')
name_space__auth = app_api.namespace('api/1.0/auth', description='API / Версия API / API-авторизации пользователя в системе мультивалютного блокчейн-кошелька')
name_space__generate_mnemonic = app_api.namespace('api/1.0/genmnemonic', description='API / Версия API / API-генерации 12 слов на английском языке')
name_space__generate_wallet = app_api.namespace('api/1.0/genwallet', description='API / Версия API / API-создания кошелька для определённой монеты')
name_space__get_balans = app_api.namespace('api/1.0/getbalans', description='API / Версия API / API-запроса баланса определённой монеты')
name_space__send_tokens = app_api.namespace('api/1.0/sendtokens', description='API / Версия API / API-пересылки определённой монеты')

#CORS(name_space__newauth)
#CORS(name_space__auth)
#CORS(name_space__generate_mnemonic)
#CORS(name_space__generate_wallet)
#CORS(name_space__get_balans)

model__newauth = app_api.model('Авторизация нового пользователя в системе мультивалютного блокчейн-кошелька', {'password': fields.String(required = True, description="Пароль пользователя", help="Поле Пароль не может быть пустым."),
                                'login': fields.String(required = True, description="Имя пользователя", help="Поле Имя пользователя не может быть пустым.")})     

model__auth = app_api.model('Авторизация пользователя в системе мультивалютного блокчейн-кошелька', {'password': fields.String(required = True, description="Пароль пользователя", help="Поле Пароль не может быть пустым."),
                                'login': fields.String(required = True, description="Имя пользователя", help="Поле Имя пользователя не может быть пустым.")})     
                                 
model___generate_mnemonic = app_api.model('Генерация 12 слов на английском языке',
                               {'user_id': fields.String(required = True, description="ID пользователя", help="Поле ID пользователя сессии не может быть пустым."),
                               'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым.")})

model___generate_wallet = app_api.model('Создание кошелька для определённой монеты',
                               {'user_id': fields.String(required = True, description="ID пользователя", help="Поле ID пользователя сессии не может быть пустым."),
                               'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'coin_type': fields.String(required = True, description="Тип монеты", help="Поле Тип монеты не может быть пустым."),
                                'mnemonic': fields.String(required = True, description="Mnemonic", help="Поле Mnemonic не может быть пустым.")})
                                
model___get_balans = app_api.model('Запрос баланса определённой монеты',
                               {'user_id': fields.String(required = True, description="ID пользователя", help="Поле ID пользователя сессии не может быть пустым."),
                               'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'address': fields.String(required = True, description="Адрес кошелька", help="Поле Адрес кошелька не может быть пустым.")})
                                #'private_key': fields.String(required = True, description="Приватный ключ", help="Поле Прриватный ключ кошелька не может быть пустым.")})
                                
model___send_tokens = app_api.model('Пересылка определённой монеты',
                               {'user_id': fields.String(required = True, description="ID пользователя", help="Поле ID пользователя сессии не может быть пустым."),
                               'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'address_from': fields.String(required = True, description="Адрес кошелька отправителя", help="Поле Адрес кошелька отправителя не может быть пустым."),
                                'private_key': fields.String(required = True, description="Private_key кошелька отправителя", help="Поле Private_key отправителя не может быть пустым."),
                                'address_to': fields.String(required = True, description="Адрес кошелька получателя", help="Поле Адрес кошелька получателя не может быть пустым.")})

##Функция генерации уникальных идентификаторов:
def newidentificator():
    return str(uuid.uuid4())

def is_person(uuid):
    #select count(*) from (select * from foo) as x;
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #print(login)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    cur.execute("SELECT COUNT(*) FROM users WHERE (user_id='"+uuid+"')")
    results = cur.fetchall()
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    #if len(results) > 0:
    for row in results:
        return row[0]

def is_valid_session_id(person):
    #print(patient['doctor_id'])
    #select count(*) from (select * from foo) as x;
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    cur.execute("SELECT insystemtimeminutes,lastlogindatetime FROM users WHERE (user_id='"+person['user_id']+"' AND session_id='"+person['session_id']+"')")
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()       
    #print(person['session_id'])
    b = ''
    #print("1")
    if len(results) > 0:
        for row in results:
            #print("2")
            a_k =str(row[0]).split()
            a_k = ''.join(a_k)
            #print(person['session_id'])
            a_s = str(row[1]).split()
            a_s = ''.join(a_s)
            #print(a_k)
            #print(a_s)            
            a_d = time.mktime(time.strptime(a_s, '%d.%m.%Y%H:%M:%S'))
            now = datetime.now()
            now_d = time.mktime(time.strptime(now.strftime('%d.%m.%Y%H:%M:%S'), '%d.%m.%Y%H:%M:%S'))
            k = (now_d-a_d)/60
            k = k - int(a_k)
            b = str(k)
            #print(k)
            #if k > 0:
            #    b = 'wrong lasttime'
            #else:
            #    b = 'ok'
    else:
        b = ''
    return b

def save_new_user_into_db(person):
    print('00000000')
    person["user_id"] = newidentificator()
    person["session_id"] = newidentificator()
    now = datetime.now()
    person["lastlogindatetime"] = now.strftime("%d.%m.%Y %H:%M:%S")
    person["insystemtimeminutes"] = '10'
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    #cur.execute("SELECT surname, name, middlename, user_id, session_id, lastlogindatetime, insystemtimeminutes FROM users WHERE (login='"+person['login']+"' AND password='"+person['password']+"')")
    print('11111111')
    cur.execute("INSERT INTO users(user_id, session_id, lastlogindatetime, insystemtimeminutes, login, password) VALUES('"+person['user_id']+"','"+person['session_id']+"','"+person['lastlogindatetime']+"','"+person["insystemtimeminutes"]+"','"+person['login']+"','"+person['password']+"')")     
    #results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    con.commit()
    #Закрытие соединения
    con.close()
    print('222222222')
    
def is_login(person):
    #select count(*) from (select * from foo) as x;
    #con = MySQLdb.connect(host="localhost", user="mr_mamoru", passwd="rsmppass", db="rsmp", charset='utf8', use_unicode = True)
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    # Удаление пользователя:       
    cur.execute("SELECT COUNT(*) FROM users WHERE (login='"+person['login']+"')")
    results = cur.fetchall()
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    for row in results:
       return row[0]
    
def ishave_login(person):
    #select count(*) from (select * from foo) as x;
    #print(xdbname + ' '+ xuser + ' ' + xpassword + ' ' + xhost)
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #print('222222222222')
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    # Удаление пользователя:
    cur.execute("SELECT COUNT(*) FROM users WHERE (login='"+person['login']+"' AND password='"+person['password']+"')")
    results = cur.fetchall()
    b = ''
    #print('b=',b)
    #if len(results) > 0:
    for row in results:
        if row[0] > 0:
            #return row[0]
            now = datetime.now()
            a_d = newidentificator()
            cur.execute("UPDATE users SET session_id = '"+a_d+"', lastlogindatetime = '"+now.strftime("%d.%m.%Y %H:%M:%S")+"' WHERE (login='"+person['login']+"' AND password='"+person['password']+"')")           
            b='ok'
            #print('b=',b)
    cur.close()
    #Фиксация изменений
    con.commit()
    #Закрытие соединения
    con.close()  
    #print('b=',b)      
    return b
                                      
def get_user_info_from_db(person):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT user_id, session_id, lastlogindatetime, insystemtimeminutes FROM users WHERE (login='"+person['login']+"' AND password='"+person['password']+"')") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    if len(results) > 0:
        person={}
        for row in results:
            #s = str(row[0]).split() #Фамилия
            #person['surname'] = ' '.join(s)
            #s = str(row[1]).split() #Имя
            #person['name'] = ' '.join(s)
            #s = str(row[2]).split() #Отчество
            #person['middlename'] = ' '.join(s)
            s = str(row[0]).split() #uuid
            person['user_id'] = ' '.join(s)
            s = str(row[1]).split() #uuid
            person['session_id'] = ' '.join(s)
            s = str(row[2]).split() #lastlogindatetime
            person['lastlogindatetime'] = ' '.join(s)
            s = str(row[3]).split() #insystemtimeminutes
            person['insystemtimeminutes'] = ' '.join(s) 
        return person

def save_some__wallet_info_to_db(person):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    #cur.execute("SELECT surname, name, middlename, user_id, session_id, lastlogindatetime, insystemtimeminutes FROM users WHERE (login='"+person['login']+"' AND password='"+person['password']+"')")
    cur.execute("INSERT INTO wallets(namecoin, address, mnemonic, seed_bytes, public_key, private_key) VALUES('"+person['coin_type']+"','"+person['address']+"','"+person['mnemonic']+"','"+person['seed']+"','"+person['public_key']+"','"+person['private_key']+"')") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    con.commit()
    #Закрытие соединения
    con.close()

def generate_mnemonic_for_person(person):
    # Generate english mnemonic words
    person["mnemonic"] = Mnemonic(language="english").generate(strength=128) #wallet.generate_mnemonic(language="english", strength=256) #128)
    #person.update(wallet)
    return person

def generate_wallet_for_person(person):
    # Generate english mnemonic words
    #print('11111111')      
    #MNEMONIC: str = wallet.generate_mnemonic(language="english", strength=256) #128)
    
    #MNEMONIC = mnemonic.Mnemonic(language="english").generate(strength=256) #wallet.generate_mnemonic(language="english", strength=256) #128)
    
    #print(MNEMONIC)
    # Secret passphrase/password for mnemonic
    PASSPHRASE: Optional[str] = None # str("meherett")
    if person['coin_type'] == 'Atom':
        #print('1111111')
        #wallet = generate_wallet() #generate_wallet("m/44'/118'/0'/0/0","cosmos") #generate_wallet("m/44'/118'/0'/0/0","cosmos")
        #print(wallet)
        privkey = seed_to_privkey(person['mnemonic'], path="m/44'/118'/0'/0/0") 
        print(privkey)
        
        pubkey = privkey_to_pubkey(privkey)
        address = pubkey_to_address(pubkey, hrp="cosmos")
        wallet = {
            "derivation_path": "m/44'/118'/0'/0/0",
            "private_key": str(privkey), #privkey.decode("utf-8") ,
            "public_key": str(pubkey),
            "address": str(address) 
        }

        #print(address)
        #print(wallet)
        # Initialize Cosmos BIP44HDWallet
        #bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=AtomMainnet) #EthereumMainnet)
        # Get Atom BIP44HDWallet from mnemonic
        #bip44_hdwallet.from_mnemonic(mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE)
        # Clean default BIP44 derivation indexes/paths
        #bip44_hdwallet.clean_derivation()
        
        #person["seed"] = bip44_hdwallet.seed() #wallet['seed']
        #person["mnemonic"] = bip44_hdwallet.mnemonic() #wallet['mnemonic']
        #person["derivation_path"] = bip44_hdwallet.path() #"m/44'/118'/0'/0/0" #bip44_hdwallet.path() #wallet['derivation_path']
        #person["private_key"] = bip44_hdwallet.private_key() #str(wallet['private_key']) 
        #person["public_key"] = bip44_hdwallet.public_key() #str(wallet['public_key']) 
        #person["address"] = 'cosmos1' + bip44_hdwallet.address() #wallet['address']
        #person["address"] = wallet['address']
        person.update(wallet)
    elif person['coin_type'] == 'Ethereum':
        # Secret passphrase
        PASSPHRASE = None  # str("meherett")
        # Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese & korean
        LANGUAGE = "english" #"italian"  # default is english
        
        # 128 strength entropy
        #ENTROPY = generate_entropy(strength=128)
        #print(ENTROPY)
        # Initialize wallet
        wallet = Wallet()
        print(person['mnemonic'])
        
        wallet.from_mnemonic(mnemonic=person['mnemonic'], passphrase=PASSPHRASE, language=LANGUAGE)

        print(person['mnemonic'])

        # Get Ethereum wallet from entropy
        #wallet.from_entropy(entropy=ENTROPY, passphrase=PASSPHRASE, language=LANGUAGE)
        # Derivation from path
        wallet.from_path("m/44'/60'/0'/0/0'")
        # Or derivation from index
        #wallet.from_index(44, harden=True)
        #wallet.from_index(60, harden=True)
        #wallet.from_index(0, harden=True)
        #wallet.from_index(0)
        #wallet.from_index(0, harden=True)

        print(wallet)

        response = {
            'private_key' : wallet.private_key(),
            'public_key' : wallet.public_key(),
            'address' : wallet.address()
        }



        
        #print(person['mnemonic'])
        
        #wallet.from_mnemonic(mnemonic=person['mnemonic'], passphrase=PASSPHRASE, language=LANGUAGE)

        # Initialize Cosmos BIP44HDWallet
        #bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
        
        #print(person['mnemonic'])
        
        #k: str = person['mnemonic']
        
        # Get Atom BIP44HDWallet from mnemonic
        #bip44_hdwallet.from_mnemonic(mnemonic=k, language="english", passphrase=PASSPHRASE)
        # Clean default BIP44 derivation indexes/paths
        #bip44_hdwallet.clean_derivation()
        
        #print(person['mnemonic'])
                
        #person["derivation_path"] = bip44_hdwallet.path() #"m/44'/118'/0'/0/0" #bip44_hdwallet.path() #wallet['derivation_path']
        #person["private_key"] = bip44_hdwallet.private_key() #str(wallet['private_key']) 
        #person["public_key"] = bip44_hdwallet.public_key() #str(wallet['public_key']) 
        #person["address"] = bip44_hdwallet.address() #wallet['address']

        #person["address"] = wallet['address']


        #print(person['mnemonic'])

        # Generate english mnemonic words
        #MNEMONIC: str = generate_mnemonic(language="english", strength=128)
        # Secret passphrase/password for mnemonic
        #PASSPHRASE: Optional[str] = None  # str("meherett")

        #print(person['mnemonic'])

        # Initialize Ethereum mainnet BIP44HDWallet
        #bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
        #print(person['mnemonic'])
        # Get Ethereum BIP44HDWallet from mnemonic
        #bip44_hdwallet.from_mnemonic(mnemonic=person['mnemonic'], language="english", passphrase=PASSPHRASE)
        
        #print(person['mnemonic'])
        #person['mnemonic'] = wallet['mnemonic']
        #person['seed'] = str(hd_wallet.GetData(HdWalletDataTypes.SEED_BYTES)) #string(wallet['seed_bytes'])
        # Create from seed
        #print('1 - ' + person['seed'])
        #seed_bytes = binascii.unhexlify(wallet['seed_bytes'])
        #str1 = "".join(map(chr, seed_bytes))
        #print(str1)
        #person['seed'] = str1





        #privkey = seed_to_privkey(person['mnemonic'], path="m/44'/60'/0'/0/0") 
        #pubkey = privkey_to_pubkey(privkey)
        #address = pubkey_to_address(pubkey, hrp="0x")
        #wallet = {
        #    "derivation_path": "m/44'/60'/0'/0/0",
        #    "private_key": str(privkey), #privkey.decode("utf-8") ,
        #    "public_key": str(pubkey),
        #    "address": str(address) 
        #}
        #person.update(wallet)
        
        #response = wallet.dumps()
        person.update(response)

        #person["status"] = "ok"
    elif person['coin_type'] == 'Kava':
        hd_wallet_fact = HdWalletFactory(HdWalletCoins.KAVA)
        #hd_wallet = hd_wallet_fact.CreateRandom("kava_wallet", HdWalletWordsNum.WORDS_NUM_24)
        hd_wallet = hd_wallet_fact.CreateFromMnemonic("kawa_wallet", person['mnemonic'])
        hd_wallet.Generate(addr_num = 1)
        #HdWalletSaver(hd_wallet).SaveToFile("my_wallet.txt")
        #print(hd_wallet.ToDict())
        #response = hd_wallet.ToJson()
        response = hd_wallet.ToDict()
        
        #print(response)
        
        # Get wallet addresses
        addresses = hd_wallet.GetData(HdWalletDataTypes.ADDRESSES)
        # Get address count
        #addr_cnt = addresses.Count()
        # Get a specific address index
        #person['address'] = addresses[0]
        
        person.update(addresses[0].ToDict())
        
        #person['mnemonic'] = wallet['mnemonic']
        #person['seed'] = str(hd_wallet.GetData(HdWalletDataTypes.SEED_BYTES)) #string(wallet['seed_bytes'])
        # Create from seed
        #print('1 - ' + person['seed'])
        
        
        #seed_bytes = binascii.unhexlify(wallet['seed_bytes'])
        #str1 = "".join(map(chr, seed_bytes))
        #print(str1)
        #person["seed"] = str1
        
        
        #print('1.1 - ' + person['seed']) #str(seed_bytes, 'cp1252'))
        #bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.KAVA)
        #print('2 - ' + person['seed'])
        #person['private_key'] = bip44_mst.PrivateKey().ToExtended()
        #print('3 - ' + person['private_key'])
        #person['public_key'] = bip44_mst.PublicKey().ToExtended()
        #print('4 - ' + person['public_key'])
        
        
        # Get wallet addresses
        #addresses = hd_wallet.GetData(HdWalletDataTypes.ADDRESSES)
        # Get address count
        #addr_cnt = addresses.Count()
        # Get a specific address index
        #addr_0 = addresses[0]
        # Print first address in different formats
        #print(addresses[0].ToDict())
        #print(addresses[0].ToJson())
        
        # Iterate over all addresses and print their keys and addresses
        #for addr in addresses:
        #    print(addr.GetKey(HdWalletKeyTypes.EX_PRIV))
        #    print(addr.GetKey(HdWalletKeyTypes.EX_PUB))
        #    print(addr.GetKey(HdWalletKeyTypes.ADDRESS))
        
        
        
        #person['private_key'] = hd_wallet.private_key() #bip44_mst.PrivateKey().ToExtended()
        #print('3 - ' + person['seed'])
        #person['public_key'] = hd_wallet.public_key() #bip44_mst.PublicKey().ToExtended()
        #print('4 - ' + person['seed']) 
         
        #person['private_key'] = seed_to_privkey(seed: str, path: str = DEFAULT_DERIVATION_PAT)
        
        #adresses = wallet['addresses']
        #person['address'] = addresses['address']
        person.update(response)
        #person = hd_wallet.ToJson().dumps()   
    else:
        person["status"] = "Ошибка: неверно указано название поддерживаемых монет!" 
    return person
    
        
#async def ping_json_rpc():
#    """Connect to ws://localhost:8080/, call ping() and disconnect."""
#    rpc_client = JsonRpcClient()
#    try:
#        await rpc_client.connect('wss://gaia.hub.hackatom.org:443/websocket', 443)
#        call_result = await rpc_client.call('ping')
#        print(call_result)  # prints 'pong' (if that's return val of ping)
#    finally:
#        await rpc_client.disconnect()
        
#async def get_rpc(person):
#    async with websockets.connect("wss://gaia.hub.hackatom.org:443/websocket") as ws:
#        #response = await WebSocketsClient(ws).request("/balance/"+person['address'])
#        requests = "/balance/"+person['address']
#        response = await WebSocketsClient(ws).send(requests)
#    print(response.data.result)
    
async def get_rpc(person):
    uri = "wss://gaia.hub.hackatom.org:443/websocket"
    request = "/balance/"+person['address']
    print('Connecting...')
    async with websockets.connect(uri) as websocket:
        print('Connect!')
        await websocket.send(request)
        print('Request send!')
        while True:
            response = await websocket.recv()
            print('Response recieved!')
            responses.append(response)
            if len(responses) == num_response:
                return responses

def get_rpc2(person):
    #websocket.enableTrace(True)
    ws = create_connection("ws://echo.websocket.org/")
    print("Sending 'Hello, World'...")
    ws.send("Hello, World")
    print("Sent")
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)
    ws.close()
    return result

def get_cosmos_wallet_balans(person):
    headers = {
        'accept: application/json'
        #'Content-type': 'application/json',
    }
    url = "https://api.cosmos.network/bank/balances/" + person['address']
    response = requests.get(url).json()
    
    #print(person['address'])
    #response = call_async(get_rpc2(person))
    #response = asyncio.get_event_loop().run_until_complete(get_rpc2(person))
    #response = get_rpc2(person) 
    #print(person['address'])
    
    #asyncio.get_event_loop().run_until_complete(get_rpc2(person))
    #asyncio.get_event_loop().run_until_complete(ping_json_rpc())
    
    person.update(response)
    return person

def get_ethereum_wallet_balans(person):
    
    #headers = { 'accept: application/json' }
    #url = "https://api.cosmos.network/cosmos/bank/v1beta1/balances/" + person['address']
    #response = requests.get(url).json()
    
    url = 'https://api.ethplorer.io/getAddressInfo/'
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    response = session.get(url+str(person['address'])+'?apiKey=freekey', headers = headers).json()
    print(response)
    
    #print(person['address'])
    person.update(response)
    #person["balance"] = balance #str(balance)
    return person

def get_kava_wallet_balans(person):
    headers = {'accept: application/json'}
    url = "https://kava4.data.kava.io/bank/balances/" + person['address']
    response = requests.get(url).json()
    #print(response)    
    #print(person['address'])
    person.update(response)
    return person

@name_space__newauth.route("/")
#@cross_origin() # allow all origins all methods.
class NewAuthorize(Resource):
    @app_api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app_api.expect(model__newauth)
    def post(self):
        try:
            person = app_api.payload #request.form['data']
            if is_login(person) == 0:
                #print('111111')
                #print('111')
                save_new_user_into_db(person)
                person["status"] = "Вы успешно вошли в систему"
                #print(person["status"])
                #index('main')
                return person   
            else:
                person["status"] = 'Логин ' + person['login'] + ' уже зарегистрирован. Пожалуйста, придумайте другой логин.'
                #person.headers.add('Access-Control-Allow-Origin', '*')
                return person              
        except KeyError as e:
            name_space__auth.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space__auth.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")   

                                
@name_space__auth.route("/")
#@cross_origin() # allow all origins all methods.
class Authorize(Resource):
    @app_api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app_api.expect(model__auth)
    def post(self):
        try:
            auth1 = app_api.payload #request.form['data']
            #print('111')
            if ishave_login(auth1) != 'ok':
                return {
                    "status" : "Такого пользователя нет в системе" 
                }
            else:
                #print('222')
                person = get_user_info_from_db(auth1)
                person["status"] = "Вы успешно вошли в систему"
                #print(person["status"])
                #index('main')
                #person.headers.add('Access-Control-Allow-Origin', '*')
                return person
                 
        except KeyError as e:
            name_space__auth.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space__auth.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")   

@name_space__generate_mnemonic.route("/")
#@cross_origin() # allow all origins all methods.
class Generate_mnemonic(Resource):
    @app_api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app_api.expect(model___generate_mnemonic)
    def post(self):
        try:
            person = app_api.payload #request.form['data']
            #print('0000000')
            if is_person(person['user_id']) == 1:
                #print('00111111')
                if float(is_valid_session_id(person)) < 0:
                    #patient_data = [1,68,0,1,1,1,1,0,0,0,0,0,0,0,0,1,2,18,50,1,3,50,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1]
                    #disease = predict(patient_data)
                    #print('0000000')
                    person = generate_mnemonic_for_person(person)
                    #person["status"] = "ok"
                    #print(person)
                    #person.headers.add('Access-Control-Allow-Origin', '*')
                    return person #disease
                else:
                    person["status"] = "Время сессии истекло, войдите в систему заново по своему Логину и Паролю."
                    #person.headers.add('Access-Control-Allow-Origin', '*')
                    return person    
            else:
                person = {
                    "status" : "Пользователь с указанным идентификатором не зарегистрован в Базе данных",
                    "user_id" : person["user_id"]
                }    
                #person.headers.add('Access-Control-Allow-Origin', '*')
                return person
        except KeyError as e:
            name_space__generate_mnemonic.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space__generate_mnemonic.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400") 


@name_space__generate_wallet.route("/")
#@cross_origin() # allow all origins all methods.
class Generate_wallet(Resource):
    @app_api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app_api.expect(model___generate_wallet)
    def post(self):
        try:
            person = app_api.payload #request.form['data']
            #print('0000000')
            if is_person(person['user_id']) == 1:
                #print('00111111')
                if float(is_valid_session_id(person)) < 0:
                    #patient_data = [1,68,0,1,1,1,1,0,0,0,0,0,0,0,0,1,2,18,50,1,3,50,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1]
                    #disease = predict(patient_data)
                    #print('0000000')
                    person = generate_wallet_for_person(person)
                    #person["status"] = "ok"
                    #print(person)
                    #person.headers.add('Access-Control-Allow-Origin', '*')
                    return person #disease
                else:
                    person["status"] = "Время сессии истекло, войдите в систему заново по своему Логину и Паролю."
                    #person.headers.add('Access-Control-Allow-Origin', '*')
                    return person    
            else:
                person = {
                    "status" : "Пользователь с указанным идентификатором не зарегистрован в Базе данных",
                    "user_id" : person["user_id"]
                }    
                #person.headers.add('Access-Control-Allow-Origin', '*')
                return person
        except KeyError as e:
            name_space__generate_wallet.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space__generate_wallet.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400") 

@name_space__get_balans.route("/")
class Get_balans(Resource):
    @app_api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app_api.expect(model___get_balans)
    def post(self):
        try:
            person = app_api.payload #request.form['data']
            #print(str(person['address']))
            if is_person(person['user_id']) == 1:
                if float(is_valid_session_id(person)) < 0:
                    #patient_data = [1,68,0,1,1,1,1,0,0,0,0,0,0,0,0,1,2,18,50,1,3,50,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1]
                    #disease = predict(patient_data)
                    #print(str(person['address']))
                    s = str(person['address'])
                    #print(s[0:2])
                    if s[0:6] == 'cosmos':
                        person = get_cosmos_wallet_balans(person) #generate_wallet_for_person(person) 
                    elif s[0:2] == '0x':
                        #print(s[0:2])
                        person = get_ethereum_wallet_balans(person)
                    elif s[0:4] == 'kava':
                        #print(s[0:4])
                        person = get_kava_wallet_balans(person)
                    else:
                        person["status"] = "Токен не поддерживается"
                    #person["status"] = "ok"
                    #print(person)
                    #person.headers.add('Access-Control-Allow-Origin', '*')
                    return person #disease
                else:
                    person["status"] = "Время сессии истекло, войдите в систему заново по своему Логину и Паролю."
                    #person.headers.add('Access-Control-Allow-Origin', '*')
                    return person    
            else:
                person = {
                    "status" : "Пользователь с указанным идентификатором не зарегистрован в Базе данных",
                    "user_id" : person["user_id"]
                }    
                #person.headers.add('Access-Control-Allow-Origin', '*')
                return person
        except KeyError as e:
            name_space__get_balans.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space__get_balans.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

@name_space__send_tokens.route("/")
class Send_tokens(Resource):
    @app_api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app_api.expect(model___send_tokens)
    def post(self):
        try:
            person = app_api.payload #request.form['data']
            #print(str(person['address']))
            if is_person(person['user_id']) == 1:
                if float(is_valid_session_id(person)) < 0:
                    #patient_data = [1,68,0,1,1,1,1,0,0,0,0,0,0,0,0,1,2,18,50,1,3,50,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1]
                    #disease = predict(patient_data)
                    #print(str(person['address']))
                    s = str(person['address_from'])
                    st = str(person['address_to'])
                    #print(s[0:2])
                    if s[0:6] == 'cosmos' and st[0:6] == 'cosmos':
                        person = send_cosmos_cosmos_tokens(person) #generate_wallet_for_person(person)
                    elif s[0:4] == 'kava' and st[0:4] == 'kava':
                        person = send_kava_kava_tokens(person)
                    elif s[0:2] == '0x' and st[0:2] == '0x':
                        person = send_ethereum_ethereum_tokens(person)    
                    elif (s[0:6] == 'cosmos' and st[0:4] == 'kava') or (s[0:4] == 'kava' and st[0:6] == 'cosmos'): 
                        person = send_cosmos_kava_tokens(person)
                    elif (s[0:6] == 'cosmos' and st[0:2] == '0x') or (s[0:2] == '0x' and st[0:6] == 'cosmos'):
                        person = send_cosmos_ethereum_tokens(person)
                    elif (s[0:4] == 'kava' and st[0:2] == '0x') or (s[0:2] == '0x' and st[0:4] == 'kava'):
                        person = send_kava_ethereum_tokens(person)
                    else:
                        person["status"] = "Операция не поддерживается"
                    #person["status"] = "ok"
                    #print(person)
                    #person.headers.add('Access-Control-Allow-Origin', '*')
                    return person #disease
                else:
                    person["status"] = "Время сессии истекло, войдите в систему заново по своему Логину и Паролю."
                    #person.headers.add('Access-Control-Allow-Origin', '*')
                    return person    
            else:
                person = {
                    "status" : "Пользователь с указанным идентификатором не зарегистрован в Базе данных",
                    "user_id" : person["user_id"]
                }    
                #person.headers.add('Access-Control-Allow-Origin', '*')
                return person
        except KeyError as e:
            name_space__send_tokens.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space__send_tokens.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

if __name__ == '__main__':
        #app.run(debug=True)    
        flask_app.run(host="0.0.0.0", port="80")
