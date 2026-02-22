"""
Garmin Assistant — personal MCP wrapper
Combines garmin_mcp live tools with GarminDB local database tools
"""
import sys
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# garmin_mcp internals — configure + register each module
from garmin_mcp import init_api
from garmin_mcp import (
    activity_management,
    health_wellness,
    user_profile,
    devices,
    gear_management,
    weight_management,
    challenges,
    training,
    workouts,
    data_management,
    womens_health,
)

load_dotenv()

app = FastMCP("Garmin Assistant")


def setup_garmin_mcp_tools():
    """Register all upstream garmin_mcp tools on our app."""
    import os
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    client = init_api(email, password)
    if not client:
        print("Failed to connect to Garmin Connect", file=sys.stderr)
        return

    modules = [
        activity_management, health_wellness, user_profile, devices,
        gear_management, weight_management, challenges, training,
        workouts, data_management, womens_health,
    ]
    for mod in modules:
        mod.configure(client)
        mod.register_tools(app)

    print("garmin_mcp tools registered", file=sys.stderr)


def setup_garmindb_tools():
    """Register local database query tools using GarminDB."""
    import garmindb
    from garmindb import GarminDB, Fit, GarminConnectConfigManager

    config = GarminConnectConfigManager()
    db_params = config.get_db_params()

    @app.tool()
    def query_daily_summary(date: str) -> str:
        """Query local GarminDB for a daily activity summary (YYYY-MM-DD).
        Uses the local SQLite database — no internet required."""
        try:
            db = GarminDB.GarminDB(db_params)
            # Query the local database
            result = GarminDB.DailySummary.get(db, date)
            if not result:
                return f"No local data for {date}. Run a sync first."
            return str(result)
        except Exception as e:
            return f"Error querying local DB: {e}"

    @app.tool()
    def query_weight_history(start_date: str, end_date: str) -> str:
        """Query local GarminDB for weight history between two dates (YYYY-MM-DD).
        Uses the local SQLite database — no internet required."""
        try:
            db = GarminDB.GarminDB(db_params)
            results = GarminDB.Weight.get_for_period(db, start_date, end_date)
            if not results:
                return f"No weight data between {start_date} and {end_date} in local DB."
            return "\n".join(str(r) for r in results)
        except Exception as e:
            return f"Error querying local DB: {e}"

    @app.tool()
    def sync_garmindb() -> str:
        """Trigger a GarminDB sync to download the latest Garmin data to local SQLite.
        Downloads recent data only (--latest flag)."""
        import subprocess
        result = subprocess.run(
            ["uv", "run", "garmindb_cli.py", "--all", "--download", "--import", "--analyze", "--latest"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return "Sync completed successfully."
        return f"Sync failed:\n{result.stderr}"

    print("GarminDB tools registered", file=sys.stderr)


def run():
    setup_garmin_mcp_tools()
    setup_garmindb_tools()
    app.run()


if __name__ == "__main__":
    run()
