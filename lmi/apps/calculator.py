import operator


@component
def calculator():
    """Calculator application."""

    get_visible_number, set_visible_number = use_state(0)
    get_stored_number, set_stored_number = use_state()
    get_operation, set_operation = use_state()

    def equals():
        op = get_operation()
        input1 = get_stored_number()
        input2 = get_visible_number()
        if op and input1 and input2:
            result = op(input1, input2)
            set_visible_number(result)

    def binary_operation():
        if get_stored_number() is None:
            set_stored_number(get_visible_number)
            set_visible_number(0)
        else:
            equals()

    def add():
        set_operation(operator.add)
        return binary_operation()

    def subtract():
        set_operation(operator.sub)
        return binary_operation()

    def multiply():
        set_operation(operator.mul)
        return binary_operation()

    def divide():
        set_operation(operator.truediv)
        return binary_operation()

    return [
        f"Number: {get_visible_number:.2e}",
        [
            add,
            subtract,
            multiply,
            divide,
        ],
        equals,
    ]
