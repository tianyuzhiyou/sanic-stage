# -*- coding: utf-8 -*-

"""
sqlalchemy-corn封装
"""

import datetime
import math
import re
from operator import itemgetter

from sqlalchemy import select, insert, update, and_, not_, or_, func, delete, null, MetaData, Table
from sqlalchemy.sql.expression import bindparam
from aiomysql.sa import SAConnection, Engine
from sqlalchemy.sql.expression import extract
from utils.loggers import logger

__all__ = [
    'fetchone', 'fetchall', 'fetchcount', 'fetch_id',
    'make_columns', 'make_clauses', 'make_order_by', 'get_defaults',
    'calculate_offset', 'calculate_limit', 'calculate_total_pages',
    'parse_as_sort',
]

metadata = MetaData()
date_time_fmt = "%Y-%m-%d %H:%M:%S"
date_time_now = datetime.datetime.now
null_datetime = datetime.datetime(1970, 1, 1, 0, 0, 0)
null_date = datetime.date(1970, 1, 1)


def get_defaults(db_table: Table) -> dict:
    """获取表格的默认值，解决无法自动生成默认值的问题"""
    defaults = {}
    for column in db_table.columns:
        if column.default is not None:
            value = column.default.arg
            if callable(value):
                if "date_time_now" in repr(value):
                    value = datetime.datetime.now()
                else:
                    value = value()
            defaults[column.key] = value
    return defaults


def get_onupdates(db_table: Table) -> dict:
    """获取表格的自动更新值，解决无法自动生成更新值的问题"""
    onupdates = {}
    for column in db_table.columns:
        if column.onupdate is not None:
            value = column.onupdate.arg
            if callable(value):
                if "date_time_now" in repr(value):
                    value = datetime.datetime.now()
                else:
                    value = value()
            onupdates[column.key] = value
    return onupdates


async def insertone(engine: Engine, table: Table, values: dict, conn: SAConnection = None):
    """封装单条插入，提供默认值获取，凡是单条插入，可用这个方法，否则无法正常处理默认值问题"""
    data = get_defaults(table)
    data.update(values)
    stmt = insert(table).values(data)
    if not conn:
        async with engine.acquire() as conn:
            cursor = await conn.execute(stmt)
    else:
        cursor = await conn.execute(stmt)
    return cursor.lastrowid


async def insertmany(engine: Engine, table: Table, rows: list, conn: SAConnection = None):
    defaults = get_defaults(table)
    new_rows = []
    for row in rows:
        data = {**defaults}
        data.update(row)
        new_rows.append(data)
    stmt = insert(table).values(new_rows)
    if not conn:
        async with engine.acquire() as conn:
            cursor = await conn.execute(stmt)
    else:
        cursor = await conn.execute(stmt)
    return cursor.rowcount


async def insertdifferent(engine: Engine, table: Table, rows: list, fields: list, conn: SAConnection = None):
    """
    批量插入不相同的数据
    :param rows: 列表套字典 字典中内容可以不相同
    :param fields: 列表 未设置默认值需要创建的数据
    :return:
    """
    defaults = get_defaults(table)
    new_rows = []
    for row in rows:
        data = {**defaults}
        data.update(row)
        new_rows.append(data)
    stmt = insert(table).values({col.key: bindparam(col.key) for col in table.columns if col.key in fields})
    if not conn:
        async with engine.acquire() as conn:
            cursor = await conn.execute(stmt, new_rows)
    else:
        cursor = await conn.execute(stmt, new_rows)
    return cursor.rowcount


async def delete_many(engine: Engine, table: Table, where, conn: SAConnection = None):
    """删除记录, 返回记录数量"""
    stmt = delete(table).where(where)
    if not conn:
        async with engine.acquire() as conn:
            cursor = await conn.execute(stmt)
    else:
        cursor = await conn.execute(stmt)
    count = cursor.rowcount
    return count


async def updateone(engine: Engine, table: Table, where, values: dict, conn: SAConnection = None):
    """强行区分开单个更新和多个更新，以提供更好的提示作用"""
    onupdates = get_onupdates(table)
    values.update(onupdates)
    stmt = update(table).where(where).values(values)
    if not conn:
        async with engine.acquire() as conn:
            cursor = await conn.execute(stmt)
    else:
        cursor = await conn.execute(stmt)

    count = cursor.rowcount
    return count


async def updatemany(engine: Engine, table: Table, where, values: dict, conn: SAConnection = None):
    """强行区分开单个更新和多个更新"""
    onupdates = get_onupdates(table)
    values.update(onupdates)
    stmt = update(table).where(where).values(values)
    if not conn:
        async with engine.acquire() as conn:
            cursor = await conn.execute(stmt)
    else:
        cursor = await conn.execute(stmt)

    count = cursor.rowcount
    return count


async def updatedifferent(engine: Engine, table: Table, where, rows: list, fields: list, conn: SAConnection = None):
    """批量更新不相同的数据"""
    onupdates = get_onupdates(table)
    new_rows = []
    for row in rows:
        data = {**onupdates}
        data.update(row)
        new_rows.append(data)
    stmt = update(table).where(where).values(
        {col.key: bindparam(col.key) for col in table.columns if col.key in fields})
    if not conn:
        async with engine.acquire() as conn:
            cursor = await conn.execute(stmt, new_rows)
    else:
        cursor = await conn.execute(stmt, new_rows)

    count = cursor.rowcount
    return count


async def fetchone(engine: Engine, stmt, conn: SAConnection = None):
    if not conn:
        async with engine.acquire() as conn:
            cursor = await conn.execute(stmt)
    else:
        cursor = await conn.execute(stmt)

    if cursor.rowcount:
        db_result = await cursor.fetchone()
        result = dict(db_result)
    else:
        result = {}
    return result


async def fetchall(engine: Engine, stmt, conn: SAConnection = None):
    if not conn:
        async with engine.acquire() as conn:
            cursor = await conn.execute(stmt)
    else:
        cursor = await conn.execute(stmt)

    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def fetchcount(engine: Engine, stmt, conn: SAConnection = None):
    if not conn:
        async with engine.acquire() as conn:
            count = await conn.scalar(stmt)
    else:
        count = await conn.scalar(stmt)
    return count or 0


def make_columns(t, fields=None):
    if not fields:
        return [t.c[col.key].label(col.key) for col in t.columns]
    if not isinstance(fields, (list, tuple)):
        raise Exception('fields 参数必须是列表')
    columns = []
    table_columns = t.columns.keys()
    for field in fields:
        if not field:
            raise Exception('提交的参数无效')
        if field not in table_columns:
            raise Exception(f'fields error {field}')
        columns.append(t.c[field].label(field))
    logger.debug(columns)
    if not columns:
        raise Exception('没有选择任何返回数据字段')
    return columns


def is_comparison_operator(operator):
    """比较操作符"""
    if operator in ('$eq', '$in', '$gt', '$gte', '$lt', '$lte', '$ne', '$nin', '$like', '$between'):
        return True
    return False


def is_logical_operator(operator):
    """逻辑操作符"""
    if operator in ('$and', '$or', '$not', '$nor'):
        return True
    return False


def make_comparison_clause(t, field, operator, value):
    # Comparison
    if not is_comparison_operator(operator):
        raise Exception('Not Comparison operator')
    if operator == '$eq':
        if isinstance(value, (list, tuple)):
            clause = t.c[field].in_(value)
        else:
            clause = t.c[field] == value
    elif operator == '$in':
        clause = t.c[field].in_(value)
    elif operator == '$gt':
        clause = t.c[field] > value
    elif operator == '$gte':
        clause = t.c[field] >= value
    elif operator == '$lt':
        clause = t.c[field] < value
    elif operator == '$lte':
        clause = t.c[field] <= value
    elif operator == '$ne':
        clause = t.c[field] != value
    elif operator == '$nin':
        clause = t.c[field].notin_(value)
    elif operator == '$like':
        clause = t.c[field].like(f'%{value}%')
    elif operator == '$between':
        if len(value) != 2:
            raise Exception(f'区间列表格式错误{value}')
        left, right = value
        clause = t.c[field].between(left, right)
    else:
        raise Exception(f'参数格式错误 {field} {operator} {value}')
    return clause


def make_logical_clauses(t, operator, query_items):
    clauses = []
    for query in query_items:
        clauses.extend(make_clauses(t, query))
    if operator == '$and':
        return and_(*clauses)
    elif operator == '$or':
        return or_(*clauses)
    elif operator == '$nor':
        return and_(*[not_(clause) for clause in clauses])
    else:
        raise Exception(f'操作符错误 {operator} {query_items}')


def make_clauses(t, query):
    """dict -> clauses 单表级别的查询语句构建"""
    clauses = []
    table_columns = t.columns.keys()
    for k, v in query.items():
        if is_logical_operator(k):
            clause = make_logical_clauses(t, k, v)
            clauses.append(clause)
        else:
            if isinstance(v, (list, tuple)):
                if k not in table_columns:
                    raise Exception(f'不支持的字段 {k}')
                clause = t.c[k].in_(v)
                clauses.append(clause)
            elif isinstance(v, dict):
                for operator, value in v.items():
                    if operator == '$not' and isinstance(value, dict):
                        if not value:
                            raise Exception(f'查询参数格式错误 {v}')
                        clause = not_(and_(*make_clauses(t, {k: value})))
                    else:
                        if k not in table_columns:
                            raise Exception(f'不支持的字段 {k}')
                        clause = make_comparison_clause(t, k, operator, value)
                    clauses.append(clause)
            else:
                if k not in table_columns:
                    raise Exception(f'不支持的字段 {k}')
                clause = t.c[k] == v
                clauses.append(clause)
    return clauses


def multisort(xs, specs):
    for key, reverse in reversed(specs):
        xs.sort(key=itemgetter(key), reverse=reverse)
    return xs


def make_multisort_specs(sort=None):
    if not sort:
        return []
    specs = []
    for sort_item in sort:
        for k, v in sort_item.items():
            v = str(v).lower()
            if v in ['-1', 'desc', 'descending']:
                specs.append((k, True))
            elif v in ['1', 'asc', 'ascending']:
                specs.append((k, False))
    return specs


def _make_order_by(t, sort=None):
    clauses = []
    if not sort:
        return clauses
    for k, v in sort.items():
        v = str(v).lower()
        if v in ['-1', 'desc', 'descending']:
            clauses.append(t.c[k].desc())
        elif v in ['1', 'asc', 'ascending']:
            clauses.append(t.c[k].asc())
    return clauses


def make_order_by(t, sort=None):
    sort = parse_as_sort(sort)
    clauses = []
    if not sort:
        return clauses
    if isinstance(sort, (list, tuple)):
        for sort_item in sort:
            clauses.extend(_make_order_by(t, sort_item))
    elif isinstance(sort, dict):
        clauses.extend(_make_order_by(t, sort))
    else:
        raise Exception(f'不支持的排序参数格式 {sort}')
    logger.debug(f'order_by {clauses=}')
    return clauses


ORDER_PATTERN = re.compile(r'\?|[-+]?[.\w]+$')


def parse_as_sort(items=None):
    sort = []
    if not isinstance(items, (list, tuple)):
        return sort

    for k in items:
        if not ORDER_PATTERN.match(k):
            raise Exception(f'$sort 值格式错误: {k}')
        if k.startswith(('-',)):
            sort.append({k.replace('-', ''): -1})
        elif k.startswith(('+',)):
            sort.append({k.replace('+', ''): 1})
        else:
            sort.append({k: 1})
    return sort


def calculate_offset(page=1, per_page=10):
    offset = (page - 1) * per_page
    return offset


def calculate_limit(per_page=10, per_page_max=1000):
    limit = min(per_page, per_page_max)
    return limit


def calculate_total_pages(count=0, limit=10):
    return int(math.ceil(count / float(limit)))
