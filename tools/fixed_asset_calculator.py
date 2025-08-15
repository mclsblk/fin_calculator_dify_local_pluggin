from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class FixedAssetCalculatorTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        current_assets = tool_parameters.get("current_assets")
        current_liabilities = tool_parameters.get("current_liabilities")
        asset_input = tool_parameters.get("asset_input")
        type_of_method = tool_parameters.get("type")
        if current_assets is None or current_liabilities is None \
            or asset_input is None or type_of_method is None:
            yield self.create_json_message({
                "error": "Missing required parameters.",
                "received parameters": {tool_parameters}
            })
            return
        if type_of_method == "asset_in":
            new_assets = current_assets + asset_input
            new_liabilities = current_liabilities
            new_ratio = new_assets / new_liabilities if new_liabilities != 0 else float('inf')
            original_ratio = current_assets / current_liabilities if current_liabilities != 0 else float('inf')
            yield self.create_json_message({
                "original_ratio": original_ratio,
                "new_ratio": new_ratio,
                "change": new_ratio - original_ratio
            })
        elif asset_input >= current_liabilities:
            yield self.create_json_message({
                "error": "liabilities are paid completely."
            })
            return
        elif type_of_method == "pay_debt":
            new_assets = current_assets - asset_input
            new_liabilities = current_liabilities - asset_input
            new_ratio = new_assets / new_liabilities if new_liabilities != 0 else float('inf')
            original_ratio = current_assets / current_liabilities if current_liabilities != 0 else float('inf')
            yield self.create_json_message({
                "original_ratio": original_ratio,
                "new_ratio": new_ratio,
                "change": new_ratio - original_ratio
            })
        elif type_of_method == "liability_out":
            new_assets = current_assets
            new_liabilities = current_liabilities - asset_input
            new_ratio = new_assets / new_liabilities if new_liabilities != 0 else float('inf')
            original_ratio = current_assets / current_liabilities if current_liabilities != 0 else float('inf')
            yield self.create_json_message({
                "original_ratio": original_ratio,
                "new_ratio": new_ratio,
                "change": new_ratio - original_ratio
            })
        else:
            yield self.create_json_message({
                "error": f"Invalid type of method '{type_of_method}'. Use 'asset_in', 'pay_debt', or 'liability_out'."
            })