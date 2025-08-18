# 金融担保资产计算器 - Dify插件

**Author:** lmc  
**Version:** 0.0.2
**Type:** tool  

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![Dify Plugin](https://img.shields.io/badge/dify-plugin-green.svg)](https://dify.ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📖 Description

这是一个专为Dify平台开发的金融计算器插件，提供全面的担保资产比例计算功能。插件支持多种财务场景分析，帮助用户进行精确的资产负债管理和风险评估。

### 🎯 主要功能

- **🧮 固定资产计算器** - 根据给定资产数量计算新的担保比例
- **📊 固定比例计算器** - 根据期望比例计算所需的资产调整
- **💰 提取资金计算器** - 分析资金提取对担保比例的影响

## 提示
该项目尚未发布于dify marketplace，若要安装使用，请于pull源代码之后，参考dify文档插件开发部分进行打包，再上传至dify中完成安装。项目中可能会随时遇到奇异bug或不完善之处，欢迎随时提出。

### 已知问题
- llm使用时不识别参数
- marketplace展示时不展示参数及其描述

## 📚 使用说明

### 1. 固定资产计算器 (Fixed Asset Calculator)

计算在给定资产变动下的新担保比例。

**参数：**
- `current_assets` - 当前资产总额
- `current_liabilities` - 当前负债总额  
- `asset_input` - 给定的资产金额
- `type` - 操作类型：
  - `asset_in` - 增加投资
  - `pay_debt` - 偿还债务
  - `liability_out` - 减少负债

**示例：**
```json
{
  "current_assets": 100000,
  "current_liabilities": 50000,
  "asset_input": 20000,
  "type": "asset_in"
}
```

### 2. 固定比例计算器 (Fixed Ratio Calculator)

计算达到目标担保比例所需的资产调整。

**参数：**
- `current_assets` - 当前资产总额
- `current_liabilities` - 当前负债总额
- `expected_ratio` - 期望的担保比例
- `type` - 操作类型（同上）

**示例：**
```json
{
  "current_assets": 80000,
  "current_liabilities": 50000,
  "expected_ratio": 2.0,
  "type": "asset_in"
}
```

### 3. 提取资金计算器 (Withdraw Calculator)

分析资金提取对担保比例的影响。

**参数：**
- `current_assets` - 当前资产总额
- `current_liabilities` - 当前负债总额
- `calculation_type` - 计算类型：
  - `calculate_new_ratio` - 计算提取后的新比例
  - `calculate_withdrawable_amount` - 计算最大可提取金额
- `withdrawal_amount` - 提取金额（calculate_new_ratio时必需）
- `target_ratio` - 目标比例（calculate_withdrawable_amount时必需）

**示例：**
```json
{
  "current_assets": 200000,
  "current_liabilities": 75000,
  "calculation_type": "calculate_new_ratio",
  "withdrawal_amount": 25000
}
```
### 提示
当LLM无法正确理解或处理参数时，可以在您的提示词中添加[参数示例](./parameter_examples.md)文件中的示例来辅助模型推理。这些示例提供了标准格式的参数输入，有助于模型更准确地理解您的需求。


## 🔧 技术详情

### 项目结构

```
fin_calculator/
├── manifest.yaml              # 插件清单文件
├── main.py                   # 主入口文件
├── requirements.txt          # 依赖包列表
├── GUIDE.md                 # 开发指南
├── PRIVACY.md               # 隐私政策
├── parameter_examples.txt   # 参数使用示例
├── provider/
│   ├── fin_calculator.py    # 工具提供者实现
│   └── fin_calculator.yaml  # 提供者配置
├── tools/
│   ├── fixed_asset_calculator.py    # 固定资产计算器
│   ├── fixed_asset_calculator.yaml
│   ├── fixed_ratio_calculator.py    # 固定比例计算器
│   ├── fixed_ratio_calculator.yaml
│   ├── withdraw_calculator.py       # 提取资金计算器
│   └── withdraw_calculator.yaml
└── _assets/
    ├── icon.svg             # 图标文件
    └── icon-dark.svg        # 深色图标
```

## 📋 更新日志

### v0.0.1 (2025-08-15)
- 初始版本
- 实现计算器功能
- 完善错误处理

### v0.0.2 (2025-08-17)
- 修复参数不显示问题
- 修复llm对description不可见问题
- 完善描述


## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

**⚠️ 免责声明：** 本插件仅供教育和学习目的使用，不构成任何投资建议。使用前请咨询专业的财务顾问。



