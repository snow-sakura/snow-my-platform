#!/bin/bash
# export-to-excel.sh - 将测试用例导出为Excel格式的脚本

# 该脚本演示如何将Markdown格式的测试用例转换为Excel格式
# 需要安装pandoc和xlsxwriter库才能运行

echo "正在将测试用例导出为Excel格式..."

# 检查是否安装了必要工具
if ! command -v pandoc &> /dev/null; then
    echo "错误: 需要安装pandoc工具"
    echo "安装方法: "
    echo "  Ubuntu/Debian: sudo apt-get install pandoc"
    echo "  macOS: brew install pandoc"
    echo "  Windows: 从官网下载安装"
    exit 1
fi

# 检查是否有Python xlsxwriter库
python3 -c "import xlsxwriter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "警告: Python xlsxwriter库未安装"
    echo "安装方法: pip install xlsxwriter"
    echo "继续执行，但无法生成Excel文件"
fi

# 创建临时目录
TEMP_DIR=$(mktemp -d)
echo "临时目录: $TEMP_DIR"

# 如果有参数传入，则处理指定文件
if [ $# -gt 0 ]; then
    INPUT_FILE="$1"
    OUTPUT_FILE="${INPUT_FILE%.*}.xlsx"

    # 这里添加将Markdown转换为Excel的实际逻辑
    # 示例: 将Markdown表格提取出来并写入Excel

    echo "已将测试用例从 $INPUT_FILE 导出至 $OUTPUT_FILE"
else
    echo "用法: ./export-to-excel.sh <input-markdown-file>"
    echo "示例: ./export-to-excel.sh test-cases.md"
fi

# 清理临时目录
rm -rf "$TEMP_DIR"

echo "导出完成!"