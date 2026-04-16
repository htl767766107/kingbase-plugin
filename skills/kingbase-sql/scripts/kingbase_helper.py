#!/usr/bin/env python3
"""
Kingbase 数据库辅助工具模块
提供数据库连接、查询执行、数据导出等核心功能
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 尝试导入必要的库
try:
    import psycopg2
except ImportError:
    print("错误：需要安装 psycopg2-binary", file=sys.stderr)
    print("运行：pip install psycopg2-binary", file=sys.stderr)
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    print("错误：需要安装 pandas", file=sys.stderr)
    print("运行：pip install pandas", file=sys.stderr)
    sys.exit(1)


class KingbaseHelper:
    """Kingbase 数据库辅助类"""

    def __init__(self, host=None, port=None, database=None, user=None, password=None):
        """初始化数据库连接参数"""
        self.host = host or os.getenv('KINGBASE_HOST', 'localhost')
        self.port = int(port or os.getenv('KINGBASE_PORT', '54321'))
        self.database = database or os.getenv('KINGBASE_DATABASE')
        self.user = user or os.getenv('KINGBASE_USER', 'system')
        self.password = password or os.getenv('KINGBASE_PASSWORD')
        self.conn = None

    def connect(self):
        """建立数据库连接"""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return True, "连接成功"
        except psycopg2.OperationalError as e:
            return False, f"连接失败：{str(e)}"
        except Exception as e:
            return False, f"错误：{str(e)}"

    def disconnect(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, sql, params=None):
        """执行 SQL 查询并返回 DataFrame"""
        if not self.conn:
            return None, "未连接到数据库"

        try:
            df = pd.read_sql_query(sql, self.conn, params=params)
            return df, "查询成功"
        except Exception as e:
            return None, f"查询失败：{str(e)}"

    def execute_command(self, sql, params=None):
        """执行非查询 SQL 语句（INSERT, UPDATE, DELETE 等）"""
        if not self.conn:
            return 0, "未连接到数据库"

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params or ())
            self.conn.commit()
            rowcount = cursor.rowcount
            cursor.close()
            return rowcount, "执行成功"
        except Exception as e:
            self.conn.rollback()
            return 0, f"执行失败：{str(e)}"

    def describe_table(self, table_name):
        """查看表结构信息"""
        sql = """
            SELECT
                column_name AS "列名",
                data_type AS "数据类型",
                is_nullable AS "可空",
                column_default AS "默认值",
                character_maximum_length AS "最大长度",
                numeric_precision AS "数值精度",
                numeric_scale AS "数值刻度"
            FROM information_schema.columns
            WHERE table_name = %s AND table_schema = 'public'
            ORDER BY ordinal_position
        """
        return self.execute_query(sql, (table_name,))

    def get_table_indexes(self, table_name):
        """查看表索引信息"""
        sql = """
            SELECT
                indexname AS "索引名",
                indexdef AS "索引定义"
            FROM pg_indexes
            WHERE tablename = %s AND schemaname = 'public'
        """
        return self.execute_query(sql, (table_name,))

    def list_tables(self):
        """列出数据库中所有表"""
        sql = """
            SELECT table_name AS "表名"
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """
        return self.execute_query(sql)

    def explain_query(self, sql):
        """分析 SQL 执行计划"""
        explain_sql = f"EXPLAIN ANALYZE {sql}"
        if not self.conn:
            return None, "未连接到数据库"

        try:
            cursor = self.conn.cursor()
            cursor.execute(explain_sql)
            plan = cursor.fetchall()
            cursor.close()
            return '\n'.join([row[0] for row in plan]), "执行计划分析完成"
        except Exception as e:
            return None, f"分析失败：{str(e)}"

    def export_to_csv(self, sql, output_path, params=None):
        """导出查询结果到 CSV"""
        df, msg = self.execute_query(sql, params)
        if df is None:
            return False, msg

        try:
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            return True, f"已导出 {len(df)} 行数据到 {output_path}"
        except Exception as e:
            return False, f"导出失败：{str(e)}"

    def export_to_excel(self, sql, output_path, params=None):
        """导出查询结果到 Excel"""
        df, msg = self.execute_query(sql, params)
        if df is None:
            return False, msg

        try:
            df.to_excel(output_path, index=False, sheet_name='Data')
            return True, f"已导出 {len(df)} 行数据到 {output_path}"
        except Exception as e:
            return False, f"导出失败：{str(e)}"

    def export_to_json(self, sql, output_path, params=None):
        """导出查询结果到 JSON"""
        df, msg = self.execute_query(sql, params)
        if df is None:
            return False, msg

        try:
            records = df.to_dict(orient='records')
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            return True, f"已导出 {len(df)} 行数据到 {output_path}"
        except Exception as e:
            return False, f"导出失败：{str(e)}"


def print_table(df):
    """以表格形式打印 DataFrame"""
    if df is None or df.empty:
        print("无数据")
        return

    # 使用 pandas 的表格格式输出
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    print(df.to_string(index=False))


def main():
    """主函数 - 命令行入口"""
    parser = argparse.ArgumentParser(description='Kingbase 数据库辅助工具')
    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # connect 命令
    connect_parser = subparsers.add_parser('connect', help='测试数据库连接')
    connect_parser.add_argument('--host', '-H', default=None, help='数据库主机')
    connect_parser.add_argument('--port', '-p', type=int, default=None, help='数据库端口')
    connect_parser.add_argument('--database', '-d', default=None, help='数据库名')
    connect_parser.add_argument('--user', '-u', default=None, help='用户名')
    connect_parser.add_argument('--password', '-P', default=None, help='密码')

    # query 命令
    query_parser = subparsers.add_parser('query', help='执行 SQL 查询')
    query_parser.add_argument('sql', help='SQL 查询语句')
    query_parser.add_argument('--host', '-H', default=None, help='数据库主机')
    query_parser.add_argument('--port', '-p', type=int, default=None, help='数据库端口')
    query_parser.add_argument('--database', '-d', default=None, help='数据库名')
    query_parser.add_argument('--user', '-u', default=None, help='用户名')
    query_parser.add_argument('--password', '-P', default=None, help='密码')

    # describe 命令
    describe_parser = subparsers.add_parser('describe', help='查看表结构')
    describe_parser.add_argument('table', help='表名')
    describe_parser.add_argument('--host', '-H', default=None, help='数据库主机')
    describe_parser.add_argument('--port', '-p', type=int, default=None, help='数据库端口')
    describe_parser.add_argument('--database', '-d', default=None, help='数据库名')
    describe_parser.add_argument('--user', '-u', default=None, help='用户名')
    describe_parser.add_argument('--password', '-P', default=None, help='密码')

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出所有表')
    list_parser.add_argument('--host', '-H', default=None, help='数据库主机')
    list_parser.add_argument('--port', '-p', type=int, default=None, help='数据库端口')
    describe_parser.add_argument('--database', '-d', default=None, help='数据库名')
    list_parser.add_argument('--user', '-u', default=None, help='用户名')
    list_parser.add_argument('--password', '-P', default=None, help='密码')

    # export 命令
    export_parser = subparsers.add_parser('export', help='导出查询结果')
    export_parser.add_argument('sql', help='SQL 查询语句')
    export_parser.add_argument('--output', '-o', required=True, help='输出文件路径')
    export_parser.add_argument('--format', '-f', choices=['csv', 'excel', 'json'],
                               default='csv', help='导出格式')
    export_parser.add_argument('--host', '-H', default=None, help='数据库主机')
    export_parser.add_argument('--port', '-p', type=int, default=None, help='数据库端口')
    export_parser.add_argument('--database', '-d', default=None, help='数据库名')
    export_parser.add_argument('--user', '-u', default=None, help='用户名')
    export_parser.add_argument('--password', '-P', default=None, help='密码')

    # explain 命令
    explain_parser = subparsers.add_parser('explain', help='分析 SQL 执行计划')
    explain_parser.add_argument('sql', help='SQL 查询语句')
    explain_parser.add_argument('--host', '-H', default=None, help='数据库主机')
    explain_parser.add_argument('--port', '-p', type=int, default=None, help='数据库端口')
    explain_parser.add_argument('--database', '-d', default=None, help='数据库名')
    explain_parser.add_argument('--user', '-u', default=None, help='用户名')
    explain_parser.add_argument('--password', '-P', default=None, help='密码')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 创建辅助实例
    helper = KingbaseHelper(
        host=args.host if hasattr(args, 'host') else None,
        port=args.port if hasattr(args, 'port') else None,
        database=args.database if hasattr(args, 'database') else None,
        user=args.user if hasattr(args, 'user') else None,
        password=args.password if hasattr(args, 'password') else None
    )

    # 执行命令
    if args.command == 'connect':
        success, msg = helper.connect()
        print(msg)
        if success:
            print(f"主机：{helper.host}:{helper.port}")
            print(f"数据库：{helper.database}")
            print(f"用户：{helper.user}")
            helper.disconnect()
        sys.exit(0 if success else 1)

    elif args.command == 'query':
        success, msg = helper.connect()
        if not success:
            print(msg)
            sys.exit(1)

        df, msg = helper.execute_query(args.sql)
        if df is None:
            print(msg)
            sys.exit(1)

        print_table(df)
        print(f"\n共 {len(df)} 行")
        helper.disconnect()

    elif args.command == 'describe':
        success, msg = helper.connect()
        if not success:
            print(msg)
            sys.exit(1)

        df, msg = helper.describe_table(args.table)
        if df is None:
            print(msg)
            sys.exit(1)

        print(f"表结构：{args.table}")
        print_table(df)
        helper.disconnect()

    elif args.command == 'list':
        success, msg = helper.connect()
        if not success:
            print(msg)
            sys.exit(1)

        df, msg = helper.list_tables()
        if df is None:
            print(msg)
            sys.exit(1)

        print("数据库表列表:")
        print_table(df)
        print(f"\n共 {len(df)} 个表")
        helper.disconnect()

    elif args.command == 'export':
        success, msg = helper.connect()
        if not success:
            print(msg)
            sys.exit(1)

        if args.format == 'csv':
            success, msg = helper.export_to_csv(args.sql, args.output)
        elif args.format == 'excel':
            success, msg = helper.export_to_excel(args.sql, args.output)
        elif args.format == 'json':
            success, msg = helper.export_to_json(args.sql, args.output)

        print(msg)
        helper.disconnect()
        sys.exit(0 if success else 1)

    elif args.command == 'explain':
        success, msg = helper.connect()
        if not success:
            print(msg)
            sys.exit(1)

        plan, msg = helper.explain_query(args.sql)
        if plan is None:
            print(msg)
            sys.exit(1)

        print("执行计划:")
        print(plan)
        helper.disconnect()


if __name__ == '__main__':
    main()
