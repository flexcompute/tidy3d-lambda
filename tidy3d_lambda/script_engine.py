import ast

from .exceptions import NoEntryPointsFoundError, MultipleEntryPointsFoundError


class Context:

    def __init__(self, deps: [str]):
        self.deps = deps

    def set_params(self, params: list):
        if len(params) != len(self.deps):
            raise TypeError("Wrong number of parameters.")
        self.params = params


class ScriptEngine:

    def __init__(self, script_id, script: str):
        self.script_id = script_id
        self.ast = None
        self.script: str = script
        self.entry_func: ast.FunctionDef = None
        self.global_vars = globals()
        self.local_vars = globals()

    def compile(self) -> Context:
        """
        Compile a script into a function.
        """
        self.ast = ast.parse(self.script)

        entrypoint_funcs = self._get_entrypoint_func()

        if not entrypoint_funcs:
            raise NoEntryPointsFoundError()
        if len(entrypoint_funcs) > 1:
            raise MultipleEntryPointsFoundError()
        self.entry_func = entrypoint_funcs[0]
        if not self.entry_func.returns or "Structure" not in ast.dump(self.entry_func.returns):
            raise TypeError("Entry function must return a Structure.")
        ast_node = compile(self.script, self.script_id, "exec")
        exec(ast_node, self.global_vars, self.local_vars)

        return Context(deps=self._get_deps())

    def exec(self, context: Context):
        """
        Execute the script.
        """
        func = self.local_vars[self.entry_func.name]
        result = func(*context.params)
        # set_model_name(result, self.script_id)
        return result

    def _get_deps(self) -> [str]:
        """
        Get the dependencies of the script.
        """
        return list(map(lambda x: x.arg, self.entry_func.args.args))

    def _get_entrypoint_func(self) -> [ast.FunctionDef]:
        """
        Get the entrypoint function from the AST.
        """
        res = []
        for node in self.ast.body:
            if isinstance(node, ast.FunctionDef):
                if isinstance(node, ast.FunctionDef):
                    for dec in node.decorator_list:
                        if dec.id == "entrypoint":
                            res.append(node)
        return res


def set_model_name(model, name):
    """
    Unfreeze a pydantic model.
    """
    allow_mutation, frozen = model.__config__.allow_mutation, model.__config__.frozen
    model.__config__.allow_mutation = True
    model.__config__.frozen = False
    model.name = name
    model.__config__.allow_mutation = allow_mutation
    model.__config__.frozen = frozen
    return model
