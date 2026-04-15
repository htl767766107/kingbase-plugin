---
name: kingbase-sql
description: 人大金仓数据库 (KingbaseES) 操作技能 - 当用户需要查询数据库、导出数据、查看表结构、分析 SQL 性能或执行任何 Kingbase 数据库操作时触发此技能。包括：SQL 查询、数据导出导入、表结构查看、执行计划分析、批量脚本执行等场景。
---

# Kingbase SQL 技能

你具备人大金仓数据库 (KingbaseES) 的操作能力。Kingbase 是国产关系型数据库，兼容 PostgreSQL 协议。

## 何时使用此技能

当用户请求涉及以下操作时，使用此技能：

- **SQL 查询**: 执行 SELECT、INSERT、UPDATE、DELETE 等语句
- **数据导出**: 将查询结果导出为 CSV、Excel、JSON 等格式
- **数据导入**: 从文件导入数据到数据库表
- **元数据查询**: 查看表结构、索引、约束、视图等
- **性能分析**: 使用 EXPLAIN 分析 SQL 执行计划
- **批量操作**: 执行 SQL 脚本文件
- **数据备份**: 备份表或整个数据库

## 前置检查

在开始任何数据库操作前，确认以下信息：

1. **连接配置**: 检查是否已配置数据库连接
   - 优先使用环境变量：`KINGBASE_HOST`、`KINGBASE_PORT`、`KINGBASE_DATABASE`、`KINGBASE_USER`、`KINGBASE_PASSWORD`
   - 如无环境变量，询问用户提供连接信息

2. **依赖检查**: 确认必要的 Python 包已安装
   ```bash
   # 检查依赖
   pip show psycopg2-binary pandas openpyxl
   ```

3. **连接测试**: 先测试数据库连接是否可用

## 数据库连接

### 连接方式

Kingbase 兼容 PostgreSQL 协议，可使用 psycopg2 连接：

```python
import psycopg2

conn = psycopg2.connect(
    host=os.getenv('KINGBASE_HOST', 'localhost'),
    port=os.getenv('KINGBASE_PORT', '54321'),
    database=os.getenv('KINGBASE_DATABASE'),
    user=os.getenv('KINGBASE_USER', 'system'),
    password=os.getenv('KINGBASE_PASSWORD')
)
```

### 连接字符串格式

```
kingbase://username:password@host:port/database
```

## 核心操作

### 1. 执行 SQL 查询

```python
import psycopg2
import pandas as pd

def execute_query(sql, params=None):
    """执行 SQL 查询并返回 DataFrame"""
    conn = get_connection()
    try:
        df = pd.read_sql_query(sql, conn, params=params)
        return df
    finally:
        conn.close()

# 示例
df = execute_query("SELECT * FROM users WHERE status = %s", ('active',))
print(df.to_string())
```

**注意事项**:
- 使用参数化查询防止 SQL 注入
- SELECT 查询使用 `pd.read_sql_query`
- 非查询语句使用 cursor.execute

### 2. 导出数据

```python
def export_to_csv(sql, output_path, params=None):
    """导出查询结果到 CSV"""
    df = execute_query(sql, params)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    return f"已导出 {len(df)} 行数据到 {output_path}"

def export_to_excel(sql, output_path, params=None):
    """导出查询结果到 Excel"""
    df = execute_query(sql, params)
    df.to_excel(output_path, index=False, sheet_name='Data')
    return f"已导出 {len(df)} 行数据到 {output_path}"
```

### 3. 查看表结构

```python
def describe_table(table_name):
    """查看表结构信息"""
    sql = """
        SELECT 
            column_name AS 列名，
            data_type AS 数据类型，
            is_nullable AS 可空，
            column_default AS 默认值
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position
    """
    return execute_query(sql, (table_name,))

def get_table_indexes(table_name):
    """查看表索引信息"""
    sql = """
        SELECT 
            indexname AS 索引名，
            indexdef AS 索引定义
        FROM pg_indexes
        WHERE tablename = %s
    """
    return execute_query(sql, (table_name,))
```

### 4. 分析执行计划

```python
def explain_query(sql):
    """分析 SQL 执行计划"""
    explain_sql = f"EXPLAIN ANALYZE {sql}"
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(explain_sql)
        plan = cursor.fetchall()
        return '\n'.join([row[0] for row in plan])
    finally:
        conn.close()
```

### 5. 列出所有表

```python
def list_tables():
    """列出数据库中所有表"""
    sql = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """
    return execute_query(sql)
```

### 6. 批量执行 SQL 脚本

```python
def execute_script_file(script_path):
    """执行 SQL 脚本文件"""
    with open(script_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # 按分号分割执行多条语句
        statements = sql_script.split(';')
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                cursor.execute(stmt)
        conn.commit()
        return "脚本执行成功"
    except Exception as e:
        conn.rollback()
        return f"执行失败：{e}"
    finally:
        conn.close()
```

## 安全实践

1. **参数化查询**: 永远不要拼接用户输入到 SQL 中
   ```python
   # ❌ 错误
   sql = f"SELECT * FROM users WHERE id = {user_input}"
   
   # ✅ 正确
   sql = "SELECT * FROM users WHERE id = %s"
   cursor.execute(sql, (user_input,))
   ```

2. **事务管理**: 修改数据的操作必须使用事务
   ```python
   try:
       cursor.execute(update_sql)
       conn.commit()
   except Exception:
       conn.rollback()
       raise
   ```

3. **连接关闭**: 使用 try-finally 确保连接关闭

4. **敏感信息**: 不在日志或输出中打印密码

## 错误处理

常见错误及解决方案：

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| connection refused | 数据库未启动或端口错误 | 检查服务状态和端口配置 |
| authentication failed | 用户名或密码错误 | 确认凭据正确 |
| database does not exist | 数据库不存在 | 检查数据库名拼写 |
| relation does not exist | 表不存在 | 检查表名或 schema |
| permission denied | 权限不足 | 联系 DBA 授权 |

## 输出格式

向用户展示结果时：

1. **小数据集** (< 50 行): 直接展示表格
2. **大数据集**: 展示前 20 行 + 总行数
3. **导出文件**: 提供下载路径
4. **执行计划**: 格式化展示关键信息

## 示例对话

**用户**: "查询 users 表的前 10 条数据"

**你**: 
1. 确认连接配置
2. 执行：`SELECT * FROM users LIMIT 10`
3. 展示结果表格

**用户**: "把 orders 表导出为 Excel"

**你**:
1. 执行：`SELECT * FROM orders`
2. 导出到 `orders_YYYYMMDD.xlsx`
3. 告知文件路径和行数

**用户**: "分析这条 SQL: SELECT * FROM users WHERE email LIKE '%@gmail.com'"

**你**:
1. 执行 EXPLAIN ANALYZE
2. 解释执行计划
3. 指出潜在性能问题（如全表扫描、索引使用情况）

## 辅助脚本

如需频繁使用，可创建辅助脚本 `kingbase_helper.py`:

```python
#!/usr/bin/env python3
"""Kingbase 数据库辅助工具"""
import os
import psycopg2
import pandas as pd
from contextlib import contextmanager

@contextmanager
def get_connection():
    """获取数据库连接上下文管理器"""
    conn = psycopg2.connect(
        host=os.getenv('KINGBASE_HOST', 'localhost'),
        port=os.getenv('KINGBASE_PORT', '54321'),
        database=os.getenv('KINGBASE_DATABASE'),
        user=os.getenv('KINGBASE_USER', 'system'),
        password=os.getenv('KINGBASE_PASSWORD')
    )
    try:
        yield conn
    finally:
        conn.close()

def query(sql, params=None):
    """执行查询返回 DataFrame"""
    with get_connection() as conn:
        return pd.read_sql_query(sql, conn, params=params)

def execute(sql, params=None):
    """执行非查询语句"""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            conn.commit()
            return cursor.rowcount
```
