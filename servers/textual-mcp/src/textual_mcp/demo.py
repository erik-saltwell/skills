"""Small interactive app for trying every stage of a documentation workflow."""

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Input, Label, Static, Switch


class Help(ModalScreen):
    DEFAULT_CSS = """
    Help { align: center middle; background: $background 70%; }
    #help-box { width: 54; height: auto; padding: 1 2; border: round $accent; }
    """

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="help-box"):
            yield Label("Enter a name, then choose Greet.")
            yield Button("Close", id="close")

    @on(Button.Pressed, "#close")
    def close_help(self) -> None:
        self.dismiss()


class DemoApp(App):
    TITLE = "Textual MCP · Demo"
    CSS = """
    Screen { background: $background; }
    #body { padding: 1 2; }
    #intro { margin-bottom: 1; color: $text-muted; }
    #name { margin-bottom: 1; }
    #buttons { height: 3; margin-bottom: 1; }
    Button { margin-right: 2; }
    #result { border: round $success; padding: 1; min-height: 5; }
    #options { height: 3; align-vertical: middle; margin-top: 1; }
    #details { margin-top: 1; }
    """
    BINDINGS = [("f1", "help", "Help"), ("ctrl+q", "quit", "Quit")]

    def __init__(self, greeting: str = "Hello") -> None:
        super().__init__()
        self.greeting = greeting

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="body"):
            yield Label("Make a greeting and capture the result for a guide.", id="intro")
            yield Input(placeholder="Your name", id="name")
            with Horizontal(id="buttons"):
                yield Button("Greet", variant="primary", id="greet")
                yield Button("Help", id="help")
            yield Static("Your greeting will appear here.", id="result", markup=False)
            with Horizontal(id="options"):
                yield Label("Enthusiastic ")
                yield Switch(id="enthusiastic")
            yield Static("\n".join(f"Documentation note {n}" for n in range(1, 16)), id="details")
        yield Footer()

    @on(Button.Pressed, "#greet")
    @on(Input.Submitted, "#name")
    def greet(self) -> None:
        name = self.query_one("#name", Input).value or "friend"
        suffix = "!" if self.query_one("#enthusiastic", Switch).value else "."
        self.query_one("#result", Static).update(f"{self.greeting}, {name}{suffix}")
        print(f"Greeting updated for {name}")

    @on(Button.Pressed, "#help")
    def action_help(self) -> None:
        self.push_screen(Help())


if __name__ == "__main__":
    DemoApp().run()
