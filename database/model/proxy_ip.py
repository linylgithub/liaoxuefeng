#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
@version: 0.1
@author:linyl
@file: proxy_ip.py
@time: 2018/10/11 12:15
"""
import logging

from database.proxy_ip import proxy_ip, user
from database.connect import *

class User(Base):
    """用户表"""

    __table__ = user
    @classmethod
    def to_dict(cls,row):
        if not row:
            return None
        d = {'id': row.id,
             'name': row.name,
             'password': row.password
             }
        return d

    @classmethod
    def get(cls, session, user_id):
        row = session.query(cls).filter(cls.id == user_id).first()
        return cls.to_dict(row)

    @classmethod
    def update(cls, session, user_id, name, password):
        try:
            session.query(cls.id == user_id).update({cls.name: name, cls.password: password})
            session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    @classmethod
    def add(cls, session, name, password):
        user = cls(name=name,
                   password=password)
        session.add(user)
        try:
            session.commit()
            return user.id
        except Exception as e:
            logging.error(e)
            return None

    @classmethod
    def remove(cls, session, user_id):
        try:
            session.query(cls.id == user_id).delete()
            session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

class ProxyIP(Base):

    __table__ = proxy_ip

    @classmethod
    def to_dict(cls,row):
        if not row:
            return None
        d = {'id': row.id,
             'protocol': row.protocol,
             'ip_host': row.ip_host,
             'status': row.status,
             'count': row.count
             }
        return d

    @classmethod
    def get_one_by_id(cls, session, ip_id):
        row = session.query(cls).filter(cls.id == ip_id).one()
        return cls.to_dict(row)

    @classmethod
    def get_status_ip_list(cls, session):
        row_list = session.query(cls).filter(cls.status == 'normal').all()
        return [cls.to_dict(row) for row in row_list]

    @classmethod
    def get_one_by_ip(cls, session,ip_host):
        row = session.query(cls).filter(cls.ip_host == ip_host).one()
        return cls.to_dict(row)

    @classmethod
    def add(cls, session, protocol, ip_host, status):
        ip_inst = cls(protocol = protocol, 
                      ip_host=ip_host,
                      status=status)
        session.add(ip_inst)
        try:
            session.commit()
            return ip_inst.id
        except Exception as e:
            logging.error(e)
            return None

    @classmethod
    def update_status(cls, session, ip_host):
        try:
            session.query(cls.ip_host == ip_host).update({cls.status:'destroy'})
            session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    @classmethod
    def update_ip_host(cls, session, ip_host, new_ip_host):
        try:
            session.query(cls.ip_host == ip_host).update({cls.ip_host:new_ip_host})
            session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False


if __name__ == '__main__':
    session = Session()
    # user_id = User.add(session,name='test',password='123456')
    # print(User.get(session,user_id=user_id))
    ip_id = ProxyIP.add(session,ip_host='124.235.181.175:80',status='true')
    print(ProxyIP.get_one_by_id(session,ip_id=ip_id))
    session.close()