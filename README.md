# cmd_router

`cmd_router` is a Python library for creating command and event routers. It allows you to register commands and events, process them asynchronously, and easily integrate them into your projects.

---

## Installation

1. Download the library:
    ```bash
    pip install https://github.com/sioxty/cmd_router.git
    ```

## Usage

### Initializing the `Router`

```python
from cmd_router.Commands import Router

router = Router(prefix='/')  # Prefix for commands
```

---

### Registering Commands

Use the `@router.command` decorator to register commands.

```python
@router.command(name='greet', description='Greeting')
async def greet_command(name):
     print(f"Hello, {name}!")
```

---

### Handling Commands

Use the `handle_command` method to process text commands.

```python
await router.handle_command('/greet John')  # Outputs: Hello, John!
```

---

### Registering Events

Use the `@router.event` decorator to register events.

```python
@router.event()
async def on_custom_event(data):
     print(f"Received event with data: {data}")
```

---

### Emitting Events

Use the `emit` method to trigger events.

```python
await router.emit('on_custom_event', data='Hello, World!')
```

---

## Built-in Events

`cmd_router` includes several built-in events that are automatically triggered in specific situations. You can register handlers for these events to customize their behavior.

### `on_massage`

This event is triggered every time a command is processed, regardless of its validity. It is useful for logging or tracking all incoming commands.

```python
@router.event()
async def on_massage(text):
     print(f"Received text: {text}")
```

**Example Usage:**
```python
await router.handle_command('/unknown_command')
# Outputs: Received text: /unknown_command
```

---

### `on_not_found`

This event is triggered if a command is not found. Use it to handle situations where a user enters an unknown command.

```python
@router.event()
async def on_not_found():
     print("Command not found!")
```

**Example Usage:**
```python
await router.handle_command('/unknown_command')
# Outputs: Command not found!
```

---

### `on_syntax_error`

This event is triggered if a command is found but its arguments are incorrect. It allows you to handle syntax errors.

```python
@router.event()
async def on_syntax_error():
     print("Syntax error in the command!")
```

**Example Usage:**
```python
@router.command(name='add')
async def add_command(a, b):
     print(int(a) + int(b))

await router.handle_command('/add 5')  # Outputs: Syntax error in the command!
```

---

## Full Example

```python
from cmd_router.Commands import Router

router = Router(prefix='/')

# Registering commands
@router.command(name='greet', description='Greeting')
async def greet_command(name):
     print(f"Hello, {name}!")

# Registering events
@router.event()
async def on_massage(text):
     print(f"Received text: {text}")

@router.event()
async def on_not_found():
     print("Command not found!")

@router.event()
async def on_syntax_error():
     print("Syntax error in the command!")

# Main function to process commands in real-time
async def main():
     while True:
          await router.handle_command(input('>> '))
          # For example, if the user enters "/greet John", it will output: Hello, John!
```

---

## License

This project is licensed under the [MIT License](LICENSE).
