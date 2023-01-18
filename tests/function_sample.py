from tidy3d import Medium, Structure, Geometry, Box

from tidy3d_lambda import entrypoint


@entrypoint
def function_sample(arg1, arg2: str = None, arg3=1, arg4=None) -> Structure:
    return Structure(geometry=Box(size=[0, 0, 0]), medium=Medium())


def function_1():
    return 1
