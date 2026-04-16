---
name: kingbase-sql
description: 人大金仓数据库 (KingbaseES) 操作技能 - 当用户需要查询数据库、导出数据、查看表结构、分析 SQL 性能或执行任何 Kingbase 数据库操作时触发此技能
---

# Kingbase SQL 技能

你具备人大金仓数据库 (KingbaseES) 的操作能力。Kingbase 是国产关系型数据库，兼容 PostgreSQL 协议。

## 何时使用此技能

**Always:**
- 执行 SQL 查询（SELECT、INSERT、UPDATE、DELETE）
- 数据导出（CSV、Excel、JSON）
- 数据导入
- 查看表结构、索引、约束
- 分析 SQL 执行计划
- 执行 SQL 脚本文件

**前置条件：** 确保数据库连接已配置

## 核心实践

```
永远使用参数化查询，不要拼接用户输入到 SQL 中
```

**No exceptions:**
- 不要拼接字符串构建 SQL
- 不要硬编码密码
- 不要在日志中打印敏感信息

## 数据库连接

### 连接配置

优先使用环境变量：
- `KINGBASE_HOST`: 数据库主机 (默认：localhost)
- `KINGBASE_PORT`: 数据库端口 (默认：54321)
- `KINGBASE_DATABASE`: 数据库名
- `KINGBASE_USER`: 用户名
- `KINGBASE_PASSWORD`: 密码

### 连接字符串格式

```
kingbase://username:password@host:port/database
```

## 核心操作

### 1. 执行 SQL 查询

使用 helper 脚本执行查询：

```bash
/kingbase query "SELECT * FROM users LIMIT 10"
```

或使用 Python 辅助函数：

```python
from kingbase_helper import KingbaseHelper

helper = KingbaseHelper()
helper.connect()
df, msg = helper.execute_query("SELECT * FROM users WHERE status = %s", ('active',))
helper.disconnect()
```

**注意事项**:
- 使用参数化查询防止 SQL 注入
- SELECT 查询使用 `pd.read_sql_query`
- 非查询语句使用 `execute_command`

### 2. 导出数据

```bash
# 导出 CSV
/kingbase export "SELECT * FROM orders" --output orders.csv --format csv

# 导出 Excel
/kingbase export "SELECT * FROM orders" --output orders.xlsx --format excel

# 导出 JSON
/kingbase export "SELECT * FROM orders" --output orders.json --format json
```

### 3. 查看表结构

```bash
# 查看表结构
/kingbase describe users

# 列出所有表
/kingbase list
```

### 4. 分析执行计划

```bash
/kingbase explain "SELECT * FROM users WHERE status = 'active'"
```

## 安全实践

1. **参数化查询**: 永远不要拼接用户输入到 SQL 中
   ```python
   # 错误
   sql = f"SELECT * FROM users WHERE id = {user_input}"
   
   # 正确
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

## 辅助脚本

使用内置的 `kingbase_helper.py` 脚本：

```bash
# 测试连接
/kingbase connect -h localhost -p 54321 -d testdb -u system

# 执行查询
/kingbase query "SELECT * FROM users"

# 查看表结构
/kingbase describe users

# 列出所有表
/kingbase list

# 分析执行计划
/kingbase explain "SELECT * FROM users WHERE id = 1"

# 导出查询结果
/kingbase export "SELECT * FROM users" --output users.csv --format csv
```
