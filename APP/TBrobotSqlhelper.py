#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql

#调用数据库配置
def get_conn():
    host="192.168.98.133"
    port=3306
    db='mmh'
    user='dev'
    password='devdb'
    conn=pymysql.connect(host=host,port=port,user=user,passwd=password,db=db,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    return conn

#信息查询装饰函数
def Search(func):
    def out(self):
        conn = get_conn()
        cursor = conn.cursor()
        sql,parama = func(self)
        cursor.execute(sql, parama)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data
    return out

#信息插入装饰器
def Insert(func):
    def out(self,dic):
        conn = get_conn()
        cursor = conn.cursor()
        sql,parama = func(self,dic)
        cursor.execute(sql, parama)
        conn.commit()
        cursor.close()
        conn.close()
    return out


#车辆信息查询
class Car(object):
    def __init__(self,LicentseNo):
        self.LicenseNo=LicentseNo

    #数据库查询车辆信息
    @Search
    def SearchInDatebase(self):
        sql = "select engine_no,frame_no,car_owner,enroll_date,brand_name from car_info where license_no=%s"
        parama=(self.LicenseNo,)
        return sql,parama

