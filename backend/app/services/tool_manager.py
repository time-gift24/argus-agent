import copy

from sqlalchemy.orm import Session

from app.models.tool import Tool
from app.tools import BUILTIN_TOOLS
from app.tools.loader import load_builtin_tool, extract_metadata


class ToolManager:
    _instance: "ToolManager | None" = None

    def __init__(self):
        # name -> (module_path, metadata)
        self._registry: dict[str, tuple[str, dict]] = {}

    @classmethod
    def get_instance(cls) -> "ToolManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register(self, module_path: str) -> None:
        tool = load_builtin_tool(module_path)
        meta = extract_metadata(tool)
        self._registry[meta["name"]] = (module_path, meta)

    def create(self, name: str):
        """Return a new BaseTool instance. Raises KeyError if not found."""
        module_path, _ = self._registry[name]
        tool = load_builtin_tool(module_path)
        if hasattr(tool, "model_copy"):
            return tool.model_copy(deep=True)
        return copy.deepcopy(tool)

    def get_schema(self, name: str) -> dict:
        """Return the JSON schema for a tool by name."""
        _, meta = self._registry[name]
        return meta["argus_schema"]

    def list_names(self) -> list[str]:
        """Return all registered builtin tool names."""
        return list(self._registry.keys())


def seed_builtin_tools(db: Session) -> None:
    """Register builtin tools in memory and upsert their metadata into the database."""
    manager = ToolManager.get_instance()

    for module_path in BUILTIN_TOOLS:
        manager.register(module_path)

    for name in manager.list_names():
        _, meta = manager._registry[name]
        record = db.query(Tool).filter(Tool.name == name).first()
        if record:
            record.description = meta["description"]
            record.argus_schema = meta["argus_schema"]
            continue

        db.add(Tool(**meta, is_builtin=True))

    db.commit()
