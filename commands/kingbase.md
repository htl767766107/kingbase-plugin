# kingbase

人大金仓数据库交互命令。

## 用法

```
/kingbase [子命令] [参数]
```

## 子命令

| 子命令 | 描述 |
|--------|------|
| `connect` | 连接到数据库 |
| `query` | 执行 SQL 查询 |
| `export` | 导出查询结果 |
| `describe` | 查看表结构 |
| `explain` | 分析 SQL 执行计划 |
| `list` | 列出所有表 |

## 示例

```bash
# 连接数据库
/kingbase connect -h localhost -p 54321 -d testdb -u system

# 执行查询
/kingbase query "SELECT * FROM users LIMIT 10"

# 导出 CSV
/kingbase export "SELECT * FROM orders" --format csv --output orders.csv

# 查看表结构
/kingbase describe users

# 分析执行计划
/kingbase explain "SELECT * FROM users WHERE status = 'active'"

# 列出所有表
/kingbase list
```

## 环境变量

- `KINGBASE_HOST`: 数据库主机 (默认：localhost)
- `KINGBASE_PORT`: 数据库端口 (默认：54321)
- `KINGBASE_DATABASE`: 数据库名
- `KINGBASE_USER`: 用户名
- `KINGBASE_PASSWORD`: 密码

## 输出格式

支持以下输出格式：
- `table`: 表格格式 (默认)
- `csv`: CSV 格式
- `json`: JSON 格式
- `excel`: Excel 格式
