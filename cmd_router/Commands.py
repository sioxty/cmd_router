from .Types import Command, Event
"""
Router Class
This module defines the `Router` class, which provides a framework for handling commands and events 
with a customizable prefix. It allows for the registration of commands and events, and provides 
methods to handle and emit them asynchronously.
Classes:
    - Router: A class to manage commands and events.
Methods:
    - __init__(prefix: str = '/'):
        Initializes the Router instance with a command prefix.
    - get_commands():
        Returns the list of registered commands.
    - handle_command(text: str):
        Handles a command by checking its prefix and activating it if valid.
    - __search_command(command_name: str):
        Searches for a command by its name in the registered commands.
    - __activate_command(text: str):
        Activates a command by parsing its name and arguments, and executes its associated function.
    - command(name: str, description: str | None = None):
        A decorator to register a command with a name, description, and associated function.
    - event():
        A decorator to register an event with its associated function.
    - emit(event_name: str, *args, **kwargs):
        Emits an event by its name, triggering its associated function with the provided arguments.
Attributes:
    - prefix (str): The prefix used to identify commands.
    - _events (list[Event]): A list of registered events.
    - __commands (list[Command]): A list of registered commands.
"""
import logging

log = logging.getLogger(__name__)

class Router:
    def __init__(
            self,
            prefix: str='/',
        ):
        self.prefix = prefix
        self._events:list[Event] = [ ]
        self.__commands:list[Command] = [ ]
        
    def get_commands(self):
        """
        Retrieve the list of commands.
        Returns:
            list: The list of commands.
        """
        
        return self.__commands
    
    async def handle_command(self, text: str):
        """
        Handles an incoming command by emitting an event and activating the command if it matches the prefix.
        Args:
            text (str): The input text to process as a command.
        Emits:
            An event named 'on_massage' with the provided text.
        Behavior:
            - If the input text starts with the defined prefix, the command is activated.
            - Otherwise, the text is only emitted as an event.
        """
        
        await self.emit(event_name='on_massage', text=text)
        if text[0] == self.prefix:
            await self.__activate_command(text)
        
    async def __search_command(self,command_name:str):
        for command in self.__commands:
            
            if command_name == command.name:
                log.debug(f"Command {command_name} found")
                return command
        
    async def __activate_command(self,text: str):
        log.debug(f"Activating command: {text}")
        text = text.split()
        command_name = text[0].replace(self.prefix,"")
        command = await self.__search_command(command_name)
        if not command:
            await self.emit(event_name='on_not_found')
            return
        
        try:
            command_args = text[1:]
            await command.func(*command_args)
        
        except Exception as e:
            await self.emit(event_name='on_syntax_error')
            log.debug(f"Error executing command {command_name}")
    
    def command(self, name: str, description: str | None = None):
        """
        Registers a command with the specified name and optional description.
        Args:
            name (str): The name of the command to register.
            description (str | None, optional): A brief description of the command. 
                If not provided, the function's docstring or a default message 
                ("No description provided") will be used.
        Returns:
            Callable: A decorator that wraps the provided function, registering it 
            as a command and preserving its asynchronous behavior.
        """
        
        def decorator(func):
            log.debug(f"Registering command: {name}")
            # Якщо description не передано, використовуємо docstring функції або значення за замовчуванням
            desc = description or func.__doc__ or "No description provided"
            
            self.__commands.append(Command(name=name, func=func, description=desc))
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            return wrapper
        return decorator
    
    def event(self):
        """
        A decorator method to register an event handler function.
        This method is used to decorate a function, registering it as an event
        handler. The event name is derived from the function's name, and the
        function is wrapped to allow asynchronous execution.
        Returns:
            decorator (function): A decorator function that registers the 
            decorated function as an event handler and wraps it for asynchronous 
            execution.
        """
        
        def decorator(func):
            event_name = func.__name__
            log.debug(f"Registering event: {event_name}")
            self._events.append(Event(name=event_name, func=func))
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            return wrapper
        return decorator
    
    async def emit(self, event_name:str, *args, **kwargs):
        """
        Asynchronously emits an event by its name and executes the associated function(s) 
        with the provided arguments and keyword arguments.
        Args:
            event_name (str): The name of the event to emit.
            *args: Positional arguments to pass to the event's associated function.
            **kwargs: Keyword arguments to pass to the event's associated function.
        Logs:
            - Logs the event emission process.
            - Logs when a matching event is found and executed.
        Behavior:
            - Iterates through the registered events (`self._events`).
            - If an event with a matching name is found, its associated function is executed.
        """
        
        log.debug(f"Emitting event: {event_name}")
        for event in self._events:
            if  event_name== event.name:
                log.debug(f"Event {event_name} found, executing...")
                await event.func(*args, **kwargs)
