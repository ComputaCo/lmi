from lmi.hooks.use_state import update_use_state_calls_in_func


def component(func):
    return Component()

    func = update_use_state_calls_in_func(func)
