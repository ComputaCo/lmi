## Components

Component
- size
: Text
  - content: str
  - selectable: bool
: TextInput : KeyboardEventHandler
  - on_change: () -> None
: Button : ClickEventHandler
  - on_click: () -> None
: ScrollView
: Stack
  - children
: AbstractItemList : Stack
  - items
  - bullet_generator
  : OrderedList
  : UnorderedList
  : OptionList
  : CheckList
: MenuList : Stack
  # a stack of the open/close Button and the menu items sub-Stack (when open)
  - items
: ComboBox : MenuList
  : multiple_select
: PythonComponent : Text
  # displays a string representation of the object / function / code / class / module
  : PythonObject
    - hide_private_attributes
    - show_methods
  : PythonFunction # just function signature
  : PythonCode # function signature and body
  : PythonClass
    - hide_attributes
    - hide_methods
    - hide_classes
    - show_private_members
    - show_inherited_members
  : PythonModule
    - hide_variables
    - hide_functions
    - hide_classes
    - show_internal
: Dialog
: Description : Text
  : Image
  : Video
  : Audio