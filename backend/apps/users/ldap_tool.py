# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  ldap相关


import logging
from django.conf import settings
from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES, MODIFY_REPLACE, MODIFY_ADD, MODIFY_DELETE, HASHED_SALTED_SHA
from ldap3.utils.hashed import hashed

logger = logging.getLogger('views')


class LdapTool(object):
    """
    Operation Dcouments: http://ldap3.readthedocs.io/
    用户信息字段：uid、cn为用户id，sn为用户姓名 
    返回结果：{'result': 0, 'description': 'success', 'dn': '', 'message': '', 'referrals': None, 'type': 'modifyResponse'}
    用户离职不删除记录，移动到Leaved组下
    """
    def __init__(self, ldap_uri=settings.LDAP_URI, base_dn=settings.BASE_DN, user=settings.LDAP_USER, password=settings.LDAP_PASSWORD, user_dn_flag=settings.USER_DN_FLAG, group_type=settings.GROUP_TYPE):
        self.ldap_uri = ldap_uri
        self.base_dn = base_dn
        self.user = user
        self.passwd = password
        self.user_dn_flag = user_dn_flag
        self.group_type = group_type
        self.leaved_base_dn = 'ou=Leaved,%s' % base_dn #离职账户所在OU
        self.user_search_filter = '(objectclass=person)' #搜索用户
        self.group_search_filter = '(objectclass={})'.format(group_type) #搜索组
        self.s = Server(ldap_uri, get_info=ALL)
        self._conn = Connection(self.s, self.user, self.passwd, auto_bind=True)

    @property
    def conn(self):
        if not self._conn:
            self._conn = Connection(self.s, self.user, self.passwd, auto_bind=True)

        return self._conn

    def search_user(self, key=None, value=None, attributes=ALL_ATTRIBUTES):
        """
        搜索用户
        """
        search_base = 'ou=People,{}'.format(self.base_dn)
        search_filter = '(&{}({}={}))'.format(self.user_search_filter, key, value)
        ret = self.conn.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE, attributes=attributes)
        if ret: return self.conn.response[0]
        return None

    def search_all(self, class_name='top', attributes=ALL_ATTRIBUTES):
        search_base = self.base_dn
        search_filter = '(objectClass=%s)' % class_name
        ret = self.conn.extend.standard.paged_search(search_base, search_filter, attributes=attributes)
        if ret: return self.conn.response
        return None

    def get_user(self, uid=None, attributes=ALL_ATTRIBUTES):
        """
        获取用户信息
        """
        search_base = 'ou=People,{}'.format(self.base_dn)
        search_filter = '(&{}({}={}))'.format(self.user_search_filter,self.user_dn_flag,uid)
        ret = self.conn.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE, attributes=attributes)
        if ret: return self.conn.response[0]
        return None


    def get_users(self, attributes=ALL_ATTRIBUTES):
        """
        获取用户列表
        """
        search_base = 'ou=People,{}'.format(self.base_dn)
        search_filter = self.user_search_filter
        ret = self.conn.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE, attributes=attributes)
        if ret: return self.conn.response
        return None

    def get_group(self, cn=None, attributes=ALL_ATTRIBUTES):
        """
        查用户组
        """
        search_base = 'ou=Group,{}'.format(self.base_dn)
        search_filter = '(&{}(cn={}))'.format(self.group_search_filter, cn)
        ret = self.conn.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE, attributes=attributes)
        if ret: return self.conn.response[0]
        return None

    def get_groups(self, prefix=None, attributes=ALL_ATTRIBUTES):
        """
        查用户组列表
        """
        search_base = 'ou=Group,{}'.format(self.base_dn)
        search_filter = self.group_search_filter
        ret = self.conn.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE, attributes=attributes)
        if ret:
            if prefix:
                return [row for row in self.conn.response if row['dn'].startswith(prefix)]
            else:
                return self.conn.response
        return None

    def del_dn(self,dn):
        self.conn.delete(dn)
        return self.conn.result

    def del_group(self, cn):
        """
        删除用户组
        """
        dn = "cn={},ou=Group,{}".format(cn, self.base_dn)
        self.conn.delete(dn)
        return self.conn.result

    def del_user(self, uid):
        """
        删除用户
        """
        dn = "{}={},ou=People,{}".format(self.user_dn_flag, uid, self.base_dn)
        self.conn.delete(dn)
        return self.conn.result

    def rename_dn(self,dn,newname):
        '''
        修改dn名
        newname: 新的名字，格式：cn=新名字"
        '''
        self.conn.modify_dn(dn,newname)
        return self.conn.result

    def move_dn(self,dn,new_dn):
        '''
        移动dn
        '''
        relative_dn,new_superior = new_dn.split(',',1)
        self.conn.modify_dn(dn=dn,relative_dn=relative_dn,new_superior=new_superior)
        return self.conn.result

    def modify_password(self, uid, password):
        dn = "{}={},ou=People,{}".format(self.user_dn_flag, uid, self.base_dn)
        password = hashed(HASHED_SALTED_SHA, password)
        self.conn.modify(dn, {'userPassword': (MODIFY_REPLACE, password)})
        return self.conn.result

    def user_auth(self, uid, password):
        dn = "{}={},ou=People,{}".format(self.user_dn_flag, uid, self.base_dn)
        conn2 = Connection(self.s, dn, password, check_names=True, lazy=False, raise_exceptions=False)
        return conn2.bind()

    def group_add_user(self, cn, members=[]):
        dn = "cn={},ou=Group,{}".format(cn, self.base_dn)
        if members:
            members = ['cn={},ou=People,{}'.format(row, self.base_dn) for row in  members]
        else:
            members = ['']
        if self.group_type == 'groupOfUniqueNames':
            attr_key = 'uniqueMember'
        else:
            attr_key = 'member'
        self.conn.modify(dn, {attr_key: [(MODIFY_ADD, members)]})
        return self.conn.result

    def group_del_user(self, cn, members=[]):
        dn = "cn={},ou=Group,{}".format(cn, self.base_dn)
        if members:
            members = ['cn={},ou=People,{}'.format(row, self.base_dn) for row in  members]
        else:
            members = ['']
        if self.group_type == 'groupOfUniqueNames':
            attr_key = 'uniqueMember'
        else:
            attr_key = 'member'
        self.conn.modify(dn, {attr_key: [(MODIFY_DELETE, members)]})
        return self.conn.result

    def compare_attr(self,dn,attr,value):
        '''
        比较指定某个属性
        '''
        return self.conn.compare(dn=dn,attribute=attr,value=value)

    def modify_dn(self, dn, attrs):
        changes_dict = {}
        for k,v in attrs.items():
            changes_dict[k] = [(MODIFY_REPLACE,[v])]
        self.conn.modify(dn, changes_dict)
        return self.conn.result

    def modify_user(self, uid, attrs):
        dn = '{}={},ou=People,{}'.format(self.user_dn_flag, uid, self.base_dn)
        changes_dict = {}
        for k,v in attrs.items():
            changes_dict[k] = [(MODIFY_REPLACE,[v])]
        self.conn.modify(dn, changes_dict)
        return self.conn.result

    def add_user(self, attrs):
        '''
        {'uid':'xxx','mail':'xxx@qq.com','sn':'xxxxx','telephonenumber':'1860xxxxxxx', 'userPassword':'password'}
        '''
        uid = attrs['uid']
        attrs['cn'] = uid
        telephonenumber = attrs['telephonenumber']
        password = attrs['userPassword']
        dn = "{}={},ou=People,{}".format(self.user_dn_flag, uid, self.base_dn)
        if self.get_user(uid) is not None:
            return {'result': 68, 'description': 'entryAlreadyExists', 'dn': dn, 'message': '', 'referrals': None, 'type': 'addResponse'}
        if telephonenumber and self.search_user(key='telephoneNumber', value=telephonenumber):
            return {'result': 68, 'description': 'telephoneNumberAlreadyExists', 'dn': dn, 'message': '', 'referrals': None, 'type': 'addResponse'}
        attrs['objectclass'] = ['top', 'inetOrgPerson']
        attrs['userPassword'] = hashed(HASHED_SALTED_SHA, password)
        self.conn.add(dn, attributes=attrs)
        return self.conn.result

    def add_group(self, cn, description='', members=[]):
        '''
        添加组
        '''
        dn = "cn={},ou=Group,{}".format(cn, self.base_dn)
        attrs = {}
        attrs['objectclass'] = ['top', self.group_type]
        attrs['description'] = description
        if members:
            members = ['cn={},ou=People,{}'.format(row, self.base_dn) for row in  members]
        else:
            members = ['']
        if self.group_type == 'groupOfUniqueNames':
            attr_key = 'uniqueMember'
        else:
            attr_key = 'member'
        attrs[attr_key] = members
        self.conn.add(dn, attributes=attrs)
        return self.conn.result

    def unbind(self):
        self.conn.unbind()