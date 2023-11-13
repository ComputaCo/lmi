# Language Model Interface Library (LMI Lib)

## Concise React-style programming

```python
@lmi.component
def MyButton(text, on_click):
    if len(text) > 10:
        raise ValueError("Text is too long")

    return lmi.Button(text, on_click=on_click)

@lmi.app
def app():
    return lmi.Stack([
        lmi.Label("Hello, world!"),
        MyButton("Click me!", on_click=lambda: print("Clicked!"))
    ])
```

## Rapid dev and deployment

```python
app.cli() # experience the app yourself in the terminal
```

```python
app.run(agent) # agent is a langchain (str)->str agent
```

```python
app.serve(8080)
```

## GUI metaphors

- type
- click
- drag
- drop

## Python = GUI

## Layout protocol

Layout happens during the render(self, size) call, from top to bottom:

1. The child should indicate its preferred_size, max_size, and min_size
2. The parent should call render on each of its children, ideally it passes their preferred_size as the size argument, but it can pass any size between min_size and max_size. Children may raise an exception if the size is outside of their min_size and max_size.
3. The parent should truncate its output before returning the rendered content.

## TODO

[] the DisplayService, KeyboardService, MouseService, etc. need to be de-globalized. Instead the App should walk the component tree for any components with event handlers for those modalities and then provide the approrpriate option for that modality's tool (Yes, there is only one tool per modality.) However you can add more tools if you want.
