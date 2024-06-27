import types
import pkgutil
import importlib
import inspect

def walk_extensions(module: types.ModuleType) -> frozenset[str]:
    """
    Return all extension names from the given module.

    Args:
        module (types.ModuleType): The module to look for extensions in.

    Returns:
        A set of strings that can be passed directly to :obj:`discord.ext.commands.Bot.load_extension`.
    """

    def on_error(name: str):
        raise ImportError(name=name)  # pragma: no cover

    modules = set()

    for module_info in pkgutil.walk_packages(module.__path__, f"{module.__name__}.", onerror=on_error):

        if module_info.ispkg:
            imported = importlib.import_module(module_info.name)
            if not inspect.isfunction(getattr(imported, "setup", None)):
                # If it lacks a setup function, it's not an extension.
                continue

        modules.add(module_info.name)

    return frozenset(modules)