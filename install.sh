#!/usr/bin/env bash
#
# install.sh - Kingbase plugin installation script
# 安装必要的 Python 依赖和配置环境
#
# Usage:
#   ./install.sh           Install dependencies
#   ./install.sh --check   Check if dependencies are installed
#   ./install.sh --help    Show help
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 依赖列表
REQUIRED_PACKAGES=(
    "psycopg2-binary"
    "pandas"
    "openpyxl"
)

# 检查 Python 是否可用
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo "错误：需要 Python 3"
        echo "请先安装 Python 3: https://www.python.org/downloads/"
        exit 1
    fi

    echo "Python 版本：$(python3 --version)"
}

# 检查 pip 是否可用
check_pip() {
    if ! command -v pip3 &> /dev/null; then
        echo "错误：需要 pip3"
        echo "请安装 pip: https://pip.pypa.io/en/stable/installation/"
        exit 1
    fi

    echo "pip 版本：$(pip3 --version)"
}

# 检查依赖是否已安装
check_dependencies() {
    local missing=()

    echo ""
    echo "检查依赖包..."

    for package in "${REQUIRED_PACKAGES[@]}"; do
        if pip3 show "$package" &> /dev/null; then
            local version
            version=$(pip3 show "$package" | grep "Version:" | cut -d' ' -f2)
            echo "  [OK] $package ($version)"
        else
            echo "  [MISSING] $package"
            missing+=("$package")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo ""
        echo "缺失以下依赖：${missing[*]}"
        return 1
    fi

    echo ""
    echo "所有依赖已安装！"
    return 0
}

# 安装依赖
install_dependencies() {
    echo ""
    echo "安装依赖包..."

    for package in "${REQUIRED_PACKAGES[@]}"; do
        echo "  安装 $package..."
        pip3 install "$package"
    done

    echo ""
    echo "安装完成！"
}

# 测试数据库连接
test_connection() {
    echo ""
    echo "测试数据库连接..."

    local helper_script="$PLUGIN_ROOT/skills/kingbase-sql/scripts/kingbase_helper.py"

    if [[ ! -f "$helper_script" ]]; then
        echo "错误：找不到辅助脚本 $helper_script"
        return 1
    fi

    # 使用 helper 脚本测试连接
    python3 "$helper_script" connect \
        --host "${KINGBASE_HOST:-localhost}" \
        --port "${KINGBASE_PORT:-54321}" \
        --database "${KINGBASE_DATABASE:-}" \
        --user "${KINGBASE_USER:-system}" \
        --password "${KINGBASE_PASSWORD:-}"
}

# 显示帮助信息
show_help() {
    echo "Kingbase 插件安装脚本"
    echo ""
    echo "用法：$0 [选项]"
    echo ""
    echo "选项:"
    echo "  (无参数)      安装必要的 Python 依赖包"
    echo "  --check       检查依赖包是否已安装"
    echo "  --test        测试数据库连接"
    echo "  --help        显示此帮助信息"
    echo ""
    echo "环境变量:"
    echo "  KINGBASE_HOST     数据库主机 (默认：localhost)"
    echo "  KINGBASE_PORT     数据库端口 (默认：54321)"
    echo "  KINGBASE_DATABASE 数据库名"
    echo "  KINGBASE_USER     用户名"
    echo "  KINGBASE_PASSWORD 密码"
}

# 主程序
main() {
    case "${1:-}" in
        --check)
            check_python
            check_pip
            check_dependencies
            ;;
        --test)
            check_python
            test_connection
            ;;
        --help|-h|"")
            check_python
            check_pip
            if check_dependencies; then
                echo ""
                echo "插件已安装并配置完成！"
            else
                echo ""
                echo "正在安装依赖..."
                install_dependencies
            fi
            ;;
        *)
            echo "未知选项：$1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
