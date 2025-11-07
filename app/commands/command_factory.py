from app.commands.command import Command
from app.commands.external_cmd import ExternalCmd
import os
import importlib
import inspect
from pathlib import Path
from typing import Type, Dict, Set, Optional

class CommandFactory:
    _instance: Optional['CommandFactory'] = None

    def __init__(self) -> None:
        self._registry: Dict[str, Type[Command]] = {}
        CommandFactory._instance = self

    @classmethod
    def get_instance(cls) -> 'CommandFactory':
        """
        Get the singleton instance of CommandFactory.
        Returns:
            CommandFactory: The singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def registered_commands(self) -> Set[str]:
        """
        Get the set of all registered command names.
        Returns:
            Set[str]: Set of command names
        """
        return set(self._registry.keys()) | {"exit"}

    def register(self, name: str, command_cls: Type[Command]):
        self._registry[name] = command_cls

    def create(self, name: str) -> Command:
        command_cls = self._registry.get(name)

        if command_cls:
            return command_cls()
        else:
            return ExternalCmd(cmd=name)
        
    @property
    def commands(self):
        return self._registry.keys()

    @staticmethod
    def create_with_builtins() -> 'CommandFactory':
        """
        Creates a new CommandFactory instance with all built-in commands automatically registered.
        Built-in commands are discovered from the commands/builtin directory.
        The command name is derived from the lowercase class name (excluding 'Command' suffix if present).
        
        Returns:
            CommandFactory: A new factory instance with all built-in commands registered.
        """
        factory = CommandFactory()
        
        # Get the absolute path to the builtin commands directory
        builtin_dir = Path(__file__).parent / 'builtin'
        
        # Iterate through all .py files in the builtin directory
        for file_path in builtin_dir.glob('*.py'):
            if file_path.name == '__init__.py':
                continue
                
            # Convert file path to module path
            relative_path = file_path.relative_to(Path(__file__).parent.parent)
            module_path = str(relative_path).replace(os.sep, '.').replace('.py', '')
            module_name = f"app.{module_path}"
            
            try:
                # Import the module
                module = importlib.import_module(module_name)
                
                # Find all Command subclasses in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, Command) and 
                        obj != Command):
                        
                        # Convert class name to command name
                        # Remove 'Command' suffix if present and convert to lowercase
                        cmd_name = name.lower()
                        if cmd_name.endswith('command'):
                            cmd_name = cmd_name[:-7]
                        
                        # Register the command
                        factory.register(cmd_name, obj)
                        
            except ImportError as e:
                print(f"Warning: Failed to import built-in command module {module_name}: {e}")
                
        return factory