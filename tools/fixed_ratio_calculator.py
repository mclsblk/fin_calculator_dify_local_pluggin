from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class FixedRatioCalculatorTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        current_assets = tool_parameters["current_assets"]
        current_liabilities = tool_parameters["current_liabilities"]
        expected_ratio = tool_parameters["expected_ratio"]
        type_of_method = tool_parameters["type"]


        # 参数验证
        if current_assets is None or current_liabilities is None \
            or expected_ratio is None or type_of_method is None:
            yield self.create_json_message({
                "error": "Missing required parameters: current_assets, current_liabilities, expected_ratio, and type are required.",
                "received parameters": {tool_parameters}
            })
            return
            
        # 验证数值的有效性
        if current_assets < 0 or current_liabilities <= 0 or expected_ratio <= 0:
            yield self.create_json_message({
                "error": "Current assets must be non-negative, current liabilities and expected ratio must be positive."
            })
            return
            
        # 计算当前比例
        current_ratio = current_assets / current_liabilities
        
        if type_of_method == "asset_in":
            # 增加投资以达到期望比例
            required_assets = current_liabilities * expected_ratio
            additional_assets_needed = required_assets - current_assets
            
            if additional_assets_needed <= 0:
                yield self.create_json_message({
                    "current_ratio": round(current_ratio, 4),
                    "expected_ratio": expected_ratio,
                    "additional_assets_needed": 0,
                    "message": "Current ratio already meets or exceeds the expected ratio. No additional investment needed.",
                    "calculation_type": "asset_addition"
                })
            else:
                yield self.create_json_message({
                    "current_ratio": round(current_ratio, 4),
                    "expected_ratio": expected_ratio,
                    "additional_assets_needed": round(additional_assets_needed, 2),
                    "calculation_type": "asset_addition"
                })
                
        elif type_of_method == "pay_debt":
            # 偿还债务以达到期望比例
            required_liabilities = current_assets / expected_ratio
            debt_to_pay = current_liabilities - required_liabilities
            
            if debt_to_pay <= 0:
                yield self.create_json_message({
                    "current_ratio": round(current_ratio, 4),
                    "expected_ratio": expected_ratio,
                    "debt_to_pay": 0,
                    "message": "Current ratio already meets or exceeds the expected ratio. No debt payment needed.",
                    "calculation_type": "debt_payment"
                })
            else:
                yield self.create_json_message({
                    "current_ratio": round(current_ratio, 4),
                    "expected_ratio": expected_ratio,
                    "debt_to_pay": round(debt_to_pay, 2),
                    "calculation_type": "debt_payment"
                })
                
        elif type_of_method == "liability_out":
            # 计算需要减少的负债金额
            # 设 x 为减少的负债金额，则新的比例为：(current_assets - x) / (current_liabilities - x) = expected_ratio
            # 解得：x = (current_liabilities * expected_ratio - current_assets) / (expected_ratio - 1)
            liability_reduction = (current_liabilities * expected_ratio - current_assets) / (expected_ratio - 1)

            if liability_reduction <= 0:
                yield self.create_json_message({
                    "current_ratio": round(current_ratio, 4),
                    "expected_ratio": expected_ratio,
                    "liability_reduction_needed": 0,
                    "message": "Current ratio already meets or exceeds the expected ratio. No liability reduction needed.",
                    "calculation_type": "liability_reduction"
                })
            elif liability_reduction > current_liabilities:
                yield self.create_json_message({
                    "error": "Cannot reduce liabilities by more than the current total liabilities."
                })
                return
            else:
                yield self.create_json_message({
                    "current_ratio": round(current_ratio, 4),
                    "expected_ratio": expected_ratio,
                    "liability_reduction_needed": round(liability_reduction, 2),
                    "calculation_type": "liability_reduction"
                })
        else:
            yield self.create_json_message({
                "error": f"Invalid type of method '{type_of_method}'. Use 'asset_in', 'pay_debt', or 'liability_out'."
            })