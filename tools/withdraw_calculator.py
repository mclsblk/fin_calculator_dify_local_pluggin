from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class WithdrawCalculatorTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        current_assets = tool_parameters.get("current_assets")
        current_liabilities = tool_parameters.get("current_liabilities")
        calculation_type = tool_parameters.get("calculation_type")
        
        # 基础参数验证
        if current_assets is None or current_liabilities is None or calculation_type is None:
            yield self.create_json_message({
                "error": "Missing required parameters: current_assets, current_liabilities, and calculation_type are required."
            })
            return
            
        # 验证资产和负债的有效性
        if current_assets <= 0 or current_liabilities <= 0:
            yield self.create_json_message({
                "error": "Current assets and liabilities must be positive numbers."
            })
            return
            
        # 计算当前担保比例
        current_ratio = current_assets / current_liabilities
        
        if calculation_type == "calculate_new_ratio":
            # 计算提取资金后的新比例
            withdrawal_amount = tool_parameters.get("withdrawal_amount")
            
            if withdrawal_amount is None:
                yield self.create_json_message({
                    "error": "withdrawal_amount is required when calculating new ratio."
                })
                return
                
            if withdrawal_amount < 0:
                yield self.create_json_message({
                    "error": "Withdrawal amount must be non-negative."
                })
                return
                
            if withdrawal_amount > current_assets:
                yield self.create_json_message({
                    "error": "Withdrawal amount cannot exceed current assets."
                })
                return
                
            # 计算提取后的新资产和新比例
            new_assets = current_assets - withdrawal_amount
            new_ratio = new_assets / current_liabilities if current_liabilities > 0 else 0
            
            if new_ratio < 3:
                yield self.create_json_message({
                    "error": "New ratio after withdrawal must be at least 3."
                })
                return
            
            # 返回计算结果
            yield self.create_json_message({
                "current_ratio": round(current_ratio, 4),
                "withdrawal_amount": withdrawal_amount,
                "new_assets": new_assets,
                "new_ratio": round(new_ratio, 4),
                "ratio_change": round(new_ratio - current_ratio, 4),
                "calculation_type": "new_ratio_after_withdrawal"
            })
            
        elif calculation_type == "calculate_withdrawable_amount":
            # 计算在目标比例下的最大可提取金额
            target_ratio = tool_parameters.get("target_ratio")
            
            if target_ratio is None:
                yield self.create_json_message({
                    "error": "target_ratio is required when calculating withdrawable amount."
                })
                return
                
            if target_ratio < 3:
                yield self.create_json_message({
                    "error": "Target ratio must be at least 3."
                })
                return
                
            # 计算在目标比例下需要保留的最小资产
            required_assets = current_liabilities * target_ratio
            
            # 计算可提取的最大金额
            max_withdrawable = current_assets - required_assets
            
            if max_withdrawable < 0:
                yield self.create_json_message({
                    "current_ratio": round(current_ratio, 4),
                    "target_ratio": target_ratio,
                    "max_withdrawable_amount": 0,
                    "required_assets": required_assets,
                    "current_assets": current_assets,
                    "message": "Current ratio is already below target ratio. No withdrawal possible.",
                    "calculation_type": "max_withdrawable_amount"
                })
            else:
                yield self.create_json_message({
                    "current_ratio": round(current_ratio, 4),
                    "target_ratio": target_ratio,
                    "max_withdrawable_amount": round(max_withdrawable, 2),
                    "required_assets": required_assets,
                    "current_assets": current_assets,
                    "remaining_assets_after_withdrawal": required_assets,
                    "calculation_type": "max_withdrawable_amount"
                })
                
        else:
            yield self.create_json_message({
                "error": f"Invalid calculation type '{calculation_type}'. Use 'calculate_new_ratio' or 'calculate_withdrawable_amount'."
            })