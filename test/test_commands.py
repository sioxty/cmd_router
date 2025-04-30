import pytest
from cmd_router.Commands import Router
from cmd_router.Types import Command, Event

@pytest.mark.asyncio
async def test_register_command():
    router = Router(prefix='/')

    @router.command(name='test', description='Test command')
    async def test_command(arg1, arg2):
        return f"Executed with {arg1} and {arg2}"

    commands = router.get_commands()
    assert len(commands) == 1
    assert commands[0].name == 'test'
    assert commands[0].description == 'Test command'


@pytest.mark.asyncio
async def test_handle_command():
    router = Router(prefix='/')

    @router.command(name='test')
    async def test_command(arg1, arg2):
        return f"Executed with {arg1} and {arg2}"

    result = []

    @router.event()
    async def on_not_found():
        result.append("not_found")

    @router.event()
    async def on_syntax_error():
        result.append("syntax_error")

    await router.handle_command('/test arg1 arg2')
    assert len(result) == 0  # No errors should occur

    await router.handle_command('/unknown')
    assert "not_found" in result

    await router.handle_command('/test arg1')
    assert "syntax_error" in result


@pytest.mark.asyncio
async def test_register_event_and_emit():
    router = Router()

    result = []

    @router.event()
    async def on_test_event(arg1, arg2):
        result.append((arg1, arg2))

    await router.emit('on_test_event', 'value1', 'value2')
    assert len(result) == 1
    assert result[0] == ('value1', 'value2')


@pytest.mark.asyncio
async def test_emit_event_not_found():
    router = Router()

    result = []

    @router.event()
    async def on_test_event():
        result.append("event_triggered")

    await router.emit('non_existent_event')
    assert len(result) == 0  # No event should be triggered