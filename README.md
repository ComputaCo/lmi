# LMI

> Interfaces for AI

## Usage

```python
from lmi import component, app, use_state

@component
def MyButton(text, on_click):
    if len(text) > 10:
        raise ValueError("Text is too long")

    return [
        text,
        on_click
    ]

class CustomComponent(Component):
    def render(self) -> str:
        ...

@app
def MyApp():

    text, setText = use_state("click me")

    return [
        "Hello",
        MyButton(text, on_click=lambda: setText("clicked!"))
    ]
```

