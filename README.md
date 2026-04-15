# Kingbase Plugin - 人大金仓数据库技能插件

本插件为 Claude Code 添加人大金仓数据库 (KingbaseES) 操作能力。

## 功能特性

- **SQL 查询执行**: 支持执行 SELECT、INSERT、UPDATE、DELETE 等 SQL 语句
- **数据导出导入**: 支持将查询结果导出为 CSV、Excel 等格式
- **表结构查看**: 查看表结构、索引、约束等元数据信息
- **性能分析**: 使用 EXPLAIN 分析 SQL 执行计划
- **批量操作**: 支持批量 SQL 脚本执行

## 安装方法

### 方式一：本地链接 (推荐开发调试使用)

在 Claude Code 配置中添加插件路径：

```json
// ~/.claude/settings.json 或项目级 settings.json
{
  "skills": {
    "additional": ["E:/project/kingbase-plugin/skills/kingbase-sql/SKILL.md"]
  }
}
```

### 方式二：打包安装

1. 打包插件：
```bash
cd E:/project/kingbase-plugin
# 使用 package_skill 脚本打包
python -m scripts.package_skill .
```

2. 将生成的 `.skill` 文件复制到 Claude Code 技能目录

## 使用方法

### 通过自然语言触发

直接描述你的数据库需求，例如：

- "查询 users 表的所有数据"
- "导出 orders 表到 CSV 文件"
- "查看 product 表的结构"
- "分析这条 SQL 的执行计划：SELECT * FROM users WHERE id = 1"

### 通过命令触发

使用 `/kingbase` 命令进入数据库交互模式。

## 配置连接

使用前需要配置数据库连接信息，支持以下方式：

### 环境变量方式

```bash
export KINGBASE_HOST=localhost
export KINGBASE_PORT=54321
export KINGBASE_DATABASE=testdb
export KINGBASE_USER=system
export KINGBASE_PASSWORD=your_password
```

### 连接字符串方式

```
kingbase://system:password@localhost:54321/testdb
```

## 依赖要求

- Python 3.8+
- `kingbaseadapi` 或 `psycopg2` (Kingbase 兼容 PostgreSQL 协议)
- 或使用 `ksql` 命令行工具

安装依赖：
```bash
pip install psycopg2-binary pandas openpyxl
```

## 文件结构

```
kingbase-plugin/
├── .claude-plugin/
│   └── plugin.json          # 插件配置
├── README.md                # 本文档
├── commands/
│   └── kingbase.md          # 命令定义
└── skills/
    └── kingbase-sql/
        └── SKILL.md         # 技能提示词
```

## 安全提示

- 请勿在生产环境直接执行未经验证的 SQL
- 敏感连接信息请使用环境变量管理
- 批量操作前建议先备份数据
