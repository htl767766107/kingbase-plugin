#!/bin/bash
# kingbase 命令脚本 - 人大金仓数据库交互命令
# 用法：/kingbase [子命令] [参数]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HELPER_SCRIPT="$SCRIPT_DIR/skills/kingbase-sql/scripts/kingbase_helper.py"

# 检查 Python 是否可用
if ! command -v python3 &> /dev/null; then
    echo "错误：需要 python3"
    exit 1
fi

# 显示帮助信息
show_help() {
    echo "人大金仓数据库交互命令"
    echo ""
    echo "用法：/kingbase [子命令] [参数]"
    echo ""
    echo "子命令:"
    echo "  connect   连接到数据库"
    echo "  query     执行 SQL 查询"
    echo "  export    导出查询结果"
    echo "  describe  查看表结构"
    echo "  explain   分析 SQL 执行计划"
    echo "  list      列出所有表"
    echo ""
    echo "示例:"
    echo "  /kingbase connect -h localhost -p 54321 -d testdb -u system"
    echo "  /kingbase query \"SELECT * FROM users LIMIT 10\""
    echo "  /kingbase export \"SELECT * FROM orders\" --format csv --output orders.csv"
    echo "  /kingbase describe users"
    echo "  /kingbase explain \"SELECT * FROM users WHERE status = 'active'\""
    echo "  /kingbase list"
    echo ""
    echo "环境变量:"
    echo "  KINGBASE_HOST     数据库主机 (默认：localhost)"
    echo "  KINGBASE_PORT     数据库端口 (默认：54321)"
    echo "  KINGBASE_DATABASE 数据库名"
    echo "  KINGBASE_USER     用户名"
    echo "  KINGBASE_PASSWORD 密码"
}

# 检查 helper 脚本是否存在
if [ ! -f "$HELPER_SCRIPT" ]; then
    echo "错误：找不到辅助脚本 $HELPER_SCRIPT"
    exit 1
fi

# 处理子命令
case "${1:-}" in
    connect)
        shift
        python3 "$HELPER_SCRIPT" connect "$@"
        ;;
    query)
        shift
        python3 "$HELPER_SCRIPT" query "$@"
        ;;
    export)
        shift
        python3 "$HELPER_SCRIPT" export "$@"
        ;;
    describe)
        shift
        python3 "$HELPER_SCRIPT" describe "$@"
        ;;
    explain)
        shift
        python3 "$HELPER_SCRIPT" explain "$@"
        ;;
    list)
        shift
        python3 "$HELPER_SCRIPT" list "$@"
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo "未知命令：$1"
        echo ""
        show_help
        exit 1
        ;;
esac
