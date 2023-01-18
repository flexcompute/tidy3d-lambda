import pytest

from tidy3d_lambda.exceptions import NoEntryPointsFoundError, MultipleEntryPointsFoundError
from tidy3d_lambda.script_engine import ScriptEngine


def test_compile_syntax_error():
    with pytest.raises(SyntaxError):
        ScriptEngine("", script_id="").compile()


def test_compile_no_entrypoint():
    with pytest.raises(NoEntryPointsFoundError):
        ScriptEngine("","def func(): pass").compile()
        ScriptEngine("","def a(): pass").compile()


def test_compile_multiple_entrypoint():
    script = \
        """
from tidy3d_lambda import entrypoint


@entrypoint
def function_sample():
    return 1

@entrypoint
def function_1():
    return 1
    
"""
    with pytest.raises(MultipleEntryPointsFoundError):
        ScriptEngine("", script=script).compile()


def test_compile_no_return():
    script = \
        """
from tidy3d_lambda import entrypoint

@entrypoint
def function_sample(arg1, arg2:str=None, arg3=1, arg4=None):
    return 1
"""
    with pytest.raises(TypeError):
        ScriptEngine("dummy_name", script=script).compile()


def test_compile_deps():
    script = \
        """
from tidy3d_lambda import entrypoint
from tidy3d import Structure
    
@entrypoint
def function_sample(arg1, arg2:str=None, arg3=1, arg4=None) -> Structure:
    return 1
"""
    engine = ScriptEngine("", script=script)
    context = engine.compile()
    assert context.deps == ["arg1", "arg2", "arg3", "arg4"]


def test_compile_exec():
    script = \
        """
from tidy3d import Medium, Structure, Geometry, Box

from tidy3d_lambda import entrypoint


@entrypoint
def function_sample(arg1, arg2: str = None, arg3=1, arg4=None) -> Structure:
    return Structure(geometry=Box(size=[0, 0, 0]), medium=Medium())


def function_1():
    return 1

"""
    engine = ScriptEngine("script1", script=script)
    context = engine.compile()
    context.params = [1, "2", 3, 4]
    res = engine.exec(context)
    assert res.name == "script1"