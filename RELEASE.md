# 🚀 发布准备清单

## ✅ 已完成

- [x] `.claude-plugin/plugin.json` 字段完整（name, version, description, author）
- [x] `README.md` 包含安装和使用说明
- [x] `.gitignore` 排除不必要文件
- [x] `LICENSE` 文件存在（MIT）
- [x] 无硬编码密钥或敏感信息
- [x] Git 仓库已初始化
- [x] 初始提交已完成
- [x] 版本标签 v1.0.0 已创建

## 📌 下一步操作

### 1. 创建 GitHub 仓库

由于 `gh` CLI 未安装，请手动创建：

1. 访问 https://github.com/new
2. 仓库名：**kingbase-plugin** 或 **claude-code-kingbase**
3. 设为 **Public**
4. 不要勾选 "Add a README file"

### 2. 推送代码到 GitHub

```bash
# 替换为你的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/kingbase-plugin.git
git branch -M main
git push -u origin main
git push --tags
```

### 3. GitHub 仓库设置

创建仓库后，建议配置：

- **Description**: `Claude Code 插件 - 人大金仓数据库 (KingbaseES) 操作能力`
- **Topics**: `claude-code-plugin`, `claude-code`, `kingbase`, `database`, `sql`
- **About**: 添加插件文档链接

### 4. 发布到社区

#### GitHub Discussions
访问 https://github.com/anthropics/claude-code/discussions
新建讨论帖，标题示例：
> 🎉 [Plugin] Kingbase Plugin - 人大金仓数据库操作插件

#### 分享模板
```markdown
## 插件名称
Kingbase Plugin

## 功能描述
为 Claude Code 添加人大金仓数据库 (KingbaseES) 操作能力，
支持 SQL 查询、数据导出、表结构查看、执行计划分析等。

## 安装方式
```json
{
  "skills": {
    "additional": ["path/to/kingbase-plugin/skills/kingbase-sql/SKILL.md"]
  }
}
```

## 使用示例
- 查询数据库表
- 导出数据到 CSV/Excel
- 分析 SQL 执行计划

## GitHub 仓库
https://github.com/YOUR_USERNAME/kingbase-plugin
```

## 📦 本地安装测试

在 Claude Code 配置中添加：
```bash
E:\project\kingbase-plugin\skills\kingbase-sql\SKILL.md
```

测试命令：
- `/kingbase --help`
- 或直接描述："查询数据库 users 表"
