# -*- coding: utf-8 -*-

"""
定义orm示例
"""

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, DateTime, String, Boolean, SmallInteger, Integer

from utils.db_tool import date_time_now

metadata = MetaData()

"""
CREATE TABLE `t_info` (
  `c_id` int(11) NOT NULL PRIMARY KEY auto_increment COMMENT '主键id',
  `c_code` varchar(10) NOT NULL DEFAULT 'abc' COMMENT '类型',
  `c_status` tinyint(3) NOT NULL DEFAULT '1' COMMENT '状态',
  `c_update_dt` datetime NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '更新时间',
  `c_add_dt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
  `c_is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除', 
  kEY `ix_code` (`c_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试表';
"""
TestTable = Table(
    't_info', metadata,
    Column('c_id', Integer(), primary_key=True, nullable=False, comment='主键ID', autoincrement=True, key='id'),
    Column('c_code', String(10), nullable=False, comment='类型', key='code'),
    Column('c_status', SmallInteger(), nullable=False, default=1, comment='状态', key='status'),
    Column('c_add_dt', DateTime(), nullable=False, default=date_time_now, comment='添加时间', key='add_dt'),
    Column('c_update_dt', DateTime(), nullable=False, default=date_time_now, onupdate=date_time_now,
           comment='更新时间', key='update_dt'),
    Column('c_is_delete', Boolean(), nullable=False, default=False, comment='是否删除', key='is_delete')
)
