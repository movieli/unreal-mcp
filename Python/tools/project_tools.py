"""
Project Tools for Unreal MCP.

This module provides tools for managing project-wide settings and configuration.
"""

import logging
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_project_tools(mcp: FastMCP):
    """Register project tools with the MCP server."""
    
    @mcp.tool()
    def create_input_mapping(
        ctx: Context,
        action_name: str,
        key: str,
        input_type: str = "Action"
    ) -> Dict[str, Any]:
        """
        Create an input mapping for the project.
        
        Args:
            action_name: Name of the input action
            key: Key to bind (SpaceBar, LeftMouseButton, etc.)
            input_type: Type of input mapping (Action or Axis)
            
        Returns:
            Response indicating success or failure
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "action_name": action_name,
                "key": key,
                "input_type": input_type
            }
            
            logger.info(f"Creating input mapping '{action_name}' with key '{key}'")
            response = unreal.send_command("create_input_mapping", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input mapping creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating input mapping: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def create_data_asset(
        ctx: Context,
        name: str,
        asset_class: str,
        package_path: str = "/Game/Data"
    ) -> Dict[str, Any]:
        """
        Create a new data asset.

        Args:
            name: Asset name
            asset_class: Native asset class name, e.g. LevelStageDataAsset
            package_path: Unreal content path, e.g. /Game/Data/Stages
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            response = unreal.send_command("create_data_asset", {
                "name": name,
                "asset_class": asset_class,
                "package_path": package_path,
            })
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            error_msg = f"Error creating data asset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def create_data_table(
        ctx: Context,
        name: str,
        row_struct: str,
        package_path: str = "/Game/Data"
    ) -> Dict[str, Any]:
        """
        Create a new Unreal DataTable asset.

        Args:
            name: DataTable asset name
            row_struct: Native row struct name, e.g. EnemyUnitTemplateRow
            package_path: Unreal content path, e.g. /Game/Data/Enemies
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            response = unreal.send_command("create_data_table", {
                "name": name,
                "row_struct": row_struct,
                "package_path": package_path,
            })
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            error_msg = f"Error creating data table: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def set_asset_properties(
        ctx: Context,
        asset_path: str,
        properties: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Set one or more properties on a loaded Unreal asset.

        Args:
            asset_path: Unreal asset path, e.g. /Game/Data/Stages/DA_Stage_1_1
            properties: Property map keyed by Unreal property name
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            response = unreal.send_command("set_asset_properties", {
                "asset_path": asset_path,
                "properties": properties,
            })
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            error_msg = f"Error setting asset properties: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def upsert_data_table_rows(
        ctx: Context,
        asset_path: str,
        rows: List[Dict[str, Any]],
        clear_existing: bool = False,
        key_field: str = "row_name",
    ) -> Dict[str, Any]:
        """
        Add or update rows in a DataTable using JSON-compatible row objects.

        Args:
            asset_path: Unreal DataTable asset path
            rows: Row objects. Each item must include a row name field or a nested data object.
            clear_existing: If true, empties the table before inserting rows.
            key_field: Field name used to read the row key from each row object.
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            response = unreal.send_command("upsert_data_table_rows", {
                "asset_path": asset_path,
                "rows": rows,
                "clear_existing": clear_existing,
                "key_field": key_field,
            })
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            error_msg = f"Error upserting DataTable rows: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def delete_asset(
        ctx: Context,
        asset_path: str,
    ) -> Dict[str, Any]:
        """
        Delete an Unreal asset by content path.

        Args:
            asset_path: Unreal asset path, e.g. /Game/Blueprints/BP_Foo
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            response = unreal.send_command("delete_asset", {
                "asset_path": asset_path,
            })
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            error_msg = f"Error deleting asset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def rename_asset(
        ctx: Context,
        asset_path: str,
        new_asset_path: str,
    ) -> Dict[str, Any]:
        """
        Rename or move an Unreal asset by content path.

        Args:
            asset_path: Existing Unreal asset path, e.g. /Game/Blueprints/BP_Foo
            new_asset_path: Target Unreal asset path, e.g. /Game/Blueprints/Archive/BP_Foo
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            response = unreal.send_command("rename_asset", {
                "asset_path": asset_path,
                "new_asset_path": new_asset_path,
            })
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            error_msg = f"Error renaming asset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def set_blueprint_class_default_property(
        ctx: Context,
        blueprint_name: str,
        property_name: str,
        property_value,
    ) -> Dict[str, Any]:
        """
        Set a class default property on a Blueprint CDO.
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            response = unreal.send_command("set_blueprint_property", {
                "blueprint_name": blueprint_name,
                "property_name": property_name,
                "property_value": property_value,
            })
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            error_msg = f"Error setting blueprint class default property: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def set_world_settings_property(
        ctx: Context,
        property_name: str,
        property_value,
    ) -> Dict[str, Any]:
        """
        Set a property on the current map's WorldSettings and save the level.
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            response = unreal.send_command("set_world_settings_property", {
                "property_name": property_name,
                "property_value": property_value,
            })
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            error_msg = f"Error setting WorldSettings property: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def start_play_in_editor(
        ctx: Context,
    ) -> Dict[str, Any]:
        """
        Start Play In Editor for the current level.
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            response = unreal.send_command("start_play_in_editor", {})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            error_msg = f"Error starting Play In Editor: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def stop_play_in_editor(
        ctx: Context,
    ) -> Dict[str, Any]:
        """
        Stop the active Play In Editor session.
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            response = unreal.send_command("stop_play_in_editor", {})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            error_msg = f"Error stopping Play In Editor: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def is_in_play_in_editor(
        ctx: Context,
    ) -> Dict[str, Any]:
        """
        Check whether the editor is currently in a Play In Editor session.
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            response = unreal.send_command("is_in_play_in_editor", {})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            error_msg = f"Error checking Play In Editor status: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    logger.info("Project tools registered successfully") 