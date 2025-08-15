金融计算器插件参数使用例子
=======================================

根据YAML文件配置，以下是详细的参数使用例子，帮助大模型更好地理解如何调用这些工具：

## 1. Fixed Asset Calculator (固定资产计算器)

### 场景1：增加投资 (asset_in)
{
  "current_assets": 100000,
  "current_liabilities": 50000,
  "asset_input": 20000,
  "type": "asset_in"
}
说明：当前资产10万，负债5万，新增投资2万，计算新的担保比例。

### 场景2：偿还债务 (pay_debt)
{
  "current_assets": 150000,
  "current_liabilities": 80000,
  "asset_input": 15000,
  "type": "pay_debt"
}
说明：用1.5万现金偿还债务，计算偿还后的担保比例。

### 场景3：减少负债 (liability_out)
{
  "current_assets": 200000,
  "current_liabilities": 100000,
  "asset_input": 30000,
  "type": "liability_out"
}
说明：使用3万资产来减少相应的负债，计算新的担保比例。

## 2. Fixed Ratio Calculator (固定比例计算器)

### 场景1：计算需要增加的资产 (asset_in)
{
  "current_assets": 80000,
  "current_liabilities": 50000,
  "expected_ratio": 2.0,
  "type": "asset_in"
}
说明：要达到2.0的担保比例（资产是负债的2倍），需要增加多少资产？

### 场景2：计算需要偿还的债务 (pay_debt)
{
  "current_assets": 120000,
  "current_liabilities": 80000,
  "expected_ratio": 2.5,
  "type": "pay_debt"
}
说明：要达到2.5的担保比例，需要偿还多少债务？

### 场景3：计算应减少的负债 (liability_out)
{
  "current_assets": 180000,
  "current_liabilities": 90000,
  "expected_ratio": 3.0,
  "type": "liability_out"
}
说明：要达到3.0的担保比例，应该使用资产减少多少负债？

## 3. Withdraw Calculator (提取资金计算器)

### 场景1：计算提取后的新比例 (calculate_new_ratio)
{
  "current_assets": 200000,
  "current_liabilities": 75000,
  "calculation_type": "calculate_new_ratio",
  "withdrawal_amount": 25000
}
说明：提取2.5万资金后，新的担保比例是多少？

### 场景2：计算最大可提取金额 (calculate_withdrawable_amount)
{
  "current_assets": 300000,
  "current_liabilities": 100000,
  "calculation_type": "calculate_withdrawable_amount",
  "target_ratio": 2.0
}
说明：在保持担保比例不低于2.0的情况下，最多可以提取多少资金？

## 大模型调用参考

### 完整的调用示例

// 示例1：我想知道如果投资5万元，我的担保比例会变成多少
{
  "tool": "fixed_asset_calculator",
  "parameters": {
    "current_assets": 150000,
    "current_liabilities": 60000,
    "asset_input": 50000,
    "type": "asset_in"
  }
}

// 示例2：我想达到3倍的担保比例，需要增加多少投资
{
  "tool": "fixed_ratio_calculator", 
  "parameters": {
    "current_assets": 100000,
    "current_liabilities": 50000,
    "expected_ratio": 3.0,
    "type": "asset_in"
  }
}

// 示例3：我想提取3万元，提取后的担保比例是多少
{
  "tool": "withdraw_calculator",
  "parameters": {
    "current_assets": 200000,
    "current_liabilities": 80000,
    "calculation_type": "calculate_new_ratio",
    "withdrawal_amount": 30000
  }
}

### 参数说明总结

参数名                  类型      含义               示例值
current_assets         number    当前资产总额       100000
current_liabilities    number    当前负债总额       50000
asset_input           number    给定的资产金额     20000
expected_ratio        number    期望的担保比例     2.5
withdrawal_amount     number    提取金额           15000
target_ratio          number    目标担保比例       2.0
type                  select    操作类型           "asset_in", "pay_debt", "liability_out"
calculation_type      select    计算类型           "calculate_new_ratio", "calculate_withdrawable_amount"

### 常见业务场景对应的调用

1. "我想知道投资后的比例" → 使用 fixed_asset_calculator + type: "asset_in"
2. "我想达到某个比例需要多少钱" → 使用 fixed_ratio_calculator + type: "asset_in"
3. "我想提取钱后比例变成多少" → 使用 withdraw_calculator + calculation_type: "calculate_new_ratio"
4. "保持比例下最多能提取多少" → 使用 withdraw_calculator + calculation_type: "calculate_withdrawable_amount"

### 参数验证规则

1. 所有资产和负债金额必须为正数
2. 比例值必须为正数
3. 提取金额不能超过当前资产
4. type 参数必须是 "asset_in", "pay_debt", "liability_out" 之一
5. calculation_type 参数必须是 "calculate_new_ratio", "calculate_withdrawable_amount" 之一
6. 使用 calculate_new_ratio 时必须提供 withdrawal_amount
7. 使用 calculate_withdrawable_amount 时必须提供 target_ratio

### 工具选择指南

选择 Fixed Asset Calculator 当：
- 已知具体投资金额，想知道结果比例
- 已知具体偿债金额，想知道结果比例

选择 Fixed Ratio Calculator 当：
- 已知目标比例，想知道需要多少资金调整
- 需要计算达到特定比例的投资需求

选择 Withdraw Calculator 当：
- 需要计算提取资金对比例的影响
- 需要确定在保持特定比例下的最大提取额度

这些例子应该能帮助大模型准确理解各个工具的使用场景和参数配置方式。
