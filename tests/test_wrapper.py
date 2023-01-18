import ast
import inspect
import sys
import traceback

sample = """
from tidy3d_lambda import entrypoint
from tidy3d import Medium


@entrypoint
def function_sample(arg1, arg2:str=None, arg3=1, arg4=None) -> Medium:
    return 1

def function_1():
    return 1

"""


def test_find_entrypoint():
    root = ast.parse(sample)
    for node in ast.walk(root):
        if isinstance(node, ast.FunctionDef):
            f: ast.FunctionDef = node
            print(ast.dump(f))
            v = f.args.args
            # print(ast.dump(v))


            for dec in f.decorator_list:
                assert dec.id == "entrypoint"


def test_parse():
    script = """
from tidy3d_lambda import entrypoint


@entrypoint
def function_

"""
    try:
        root = ast.parse(script)
    except:
        traceback.print_exc()


def test_compile():
    root = ast.parse(sample)
    module = compile(root, "test_compile", "exec")
    g = {}
    l = {}
    exec(module, g, l)
    print(g)
    print(l)


def call_function_1(a, b, c, d=1):
    return 1


def test_dynamically_call():
    params = [1, 2, 3, 4]
    call_function_1(*params)
