# Kingbase Plugin - 人大金仓数据库技能插件

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/htl767766107/kingbase-plugin)

为 Claude Code 添加人大金仓数据库 (KingbaseES) 操作能力。

## 功能特性

- **SQL 查询执行**: 支持执行 SELECT、INSERT、UPDATE、DELETE 等 SQL 语句
- **数据导出导入**: 支持将查询结果导出为 CSV、Excel、JSON 等格式
- **表结构查看**: 查看表结构、索引、约束等元数据信息
- **性能分析**: 使用 EXPLAIN 分析 SQL 执行计划
- **批量操作**: 支持批量 SQL 脚本执行

## 快速开始

### 1. 安装依赖

```bash
# 使用安装脚本
./install.sh

# 或手动安装
pip install psycopg2-binary pandas openpyxl
```

### 2. 配置数据库连接

```bash
# 环境变量方式（推荐）
export KINGBASE_HOST=localhost
export KINGBASE_PORT=54321
export KINGBASE_DATABASE=testdb
export KINGBASE_USER=system
export KINGBASE_PASSWORD=your_password
```

### 3. 测试连接

```bash
/kingbase connect
```

## 使用方法

### 通过自然语言触发

直接描述你的数据库需求：

- "查询 users 表的所有数据"
- "导出 orders 表到 CSV 文件"
- "查看 product 表的结构"
- "分析这条 SQL 的执行计划：SELECT * FROM users WHERE id = 1"

### 通过命令触发

```bash
# 执行查询
/kingbase query "SELECT * FROM users LIMIT 10"

# 导出数据
/kingbase export "SELECT * FROM orders" --output orders.csv --format csv

# 查看表结构
/kingbase describe users

# 列出所有表
/kingbase list

# 分析执行计划
/kingbase explain "SELECT * FROM users WHERE status = 'active'"
```

## 命令参考

| 命令 | 描述 | 示例 |
|------|------|------|
| `connect` | 测试数据库连接 | `/kingbase connect -h localhost -p 54321` |
| `query` | 执行 SQL 查询 | `/kingbase query "SELECT * FROM users"` |
| `export` | 导出查询结果 | `/kingbase export "SELECT..." --output data.csv` |
| `describe` | 查看表结构 | `/kingbase describe users` |
| `explain` | 分析执行计划 | `/kingbase explain "SELECT..."` |
| `list` | 列出所有表 | `/kingbase list` |

### export 命令选项

| 选项 | 描述 |
|------|------|
| `--output, -o` | 输出文件路径（必填） |
| `--format, -f` | 导出格式：csv, excel, json（默认：csv） |
| `--host, -H` | 数据库主机 |
| `--port, -p` | 数据库端口 |
| `--database, -d` | 数据库名 |
| `--user, -u` | 用户名 |
| `--password, -P` | 密码 |

## 安装方法

### 方式一：本地安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/htl767766107/kingbase-plugin.git ~/.claude/plugins/kingbase

# 安装依赖
~/.claude/plugins/kingbase/install.sh

# 重新加载插件
/reload-plugins
```

### 方式二：从 GitHub 安装

```bash
/plugin install https://github.com/htl767766107/kingbase-plugin.git
```

## 文件结构

```
kingbase-plugin/
├── .claude-plugin/
│   ├── marketplace.json       # Marketplace 配置
│   └── plugin.json            # 插件配置
├── .version-bump.json         # 版本管理配置
├── install.sh                 # 安装脚本
├── README.md                  # 本文档
├── commands/
│   ├── kingbase.md            # 命令文档
│   └── kingbase.sh            # 命令入口
└── skills/
    └── kingbase-sql/
        ├── SKILL.md           # 技能定义
        └── scripts/
            └── kingbase_helper.py  # 辅助工具
```

## 开发

### 版本管理

使用版本管理脚本管理版本号：

```bash
# 检查当前版本
./scripts/bump-version.sh --check

# bump 版本
./scripts/bump-version.sh 1.0.2

# 审计版本引用
./scripts/bump-version.sh --audit
```

### 运行测试

```bash
# 测试数据库连接
/kingbase connect

# 测试查询
/kingbase query "SELECT 1"
```

## 安全提示

- 请勿在生产环境直接执行未经验证的 SQL
- 敏感连接信息请使用环境变量管理
- 批量操作前建议先备份数据
- 永远使用参数化查询，防止 SQL 注入

## 常见问题

### 连接失败

1. 检查数据库服务是否启动
2. 确认端口配置正确（默认 54321）
3. 检查防火墙设置

### 依赖缺失

```bash
# 重新安装依赖
./install.sh
```

### 权限不足

联系 DBA 授权相应的数据库权限。

## License

MIT License - 详见 [LICENSE](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

- htl767766107 <767766107@qq.com>
