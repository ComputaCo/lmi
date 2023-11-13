import inspect
import ast
import astunparse
import random


__USE_STATE_KV_PAIRS = {}


def use_state(default, /, append=False):
    pass


def _use_state(id, default, /, append=False):
    if id in __USE_STATE_KV_PAIRS:
        return __USE_STATE_KV_PAIRS[id][1]
    else:

        def get_value():
            return __USE_STATE_KV_PAIRS[id][0]

        def set_value(val):
            __USE_STATE_KV_PAIRS[id][0] = val

        fns = (get_value, set_value)
        if append:

            def append_fn(val):
                set_value(get_value() + val)

            fns += (append_fn,)
        __USE_STATE_KV_PAIRS[id][1] = fns


class UseStateTransformer(ast.NodeTransformer):
    def visit_Call(self, node):
        # Check if this call is a call to `use_state`
        if isinstance(node.func, ast.Name) and node.func.id == "use_state":
            # Create a new `Call` node that replaces `use_state` with `_use_state`
            # and inserts a random id as the first argument
            new_node = ast.Call(
                func=ast.Name(id="_use_state", ctx=ast.Load()),
                args=[ast.Constant(value=random.randint(0, 10**8))] + node.args,
                keywords=node.keywords,
            )
            return ast.copy_location(new_node, node)
        return self.generic_visit(node)


def update_use_state_calls_in_func(func):
    # TODO: @component should do this automatically

    # Get the source code of the function
    source = inspect.getsource(func)
    # Parse it into an AST
    tree = ast.parse(source)
    # Transform the AST
    transformer = UseStateTransformer()
    transformed_tree = transformer.visit(tree)
    # Unparse the transformed AST back into source code
    transformed_source = astunparse.unparse(transformed_tree)
    # Compile the transformed source code into a function
    namespace = {}
    exec(transformed_source, func.__globals__, namespace)
    return namespace[func.__name__]
