"""Validated wire models, shared by MCP tools and isolated workers."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Launch(Model):
    target: str = Field(description="Importable module or path to a .py file.")
    factory: str = Field(default="App", description="App instance, class, or synchronous factory.")
    cwd: str | None = None
    kwargs: dict[str, Any] = Field(default_factory=dict)
    width: int = Field(default=100, ge=10, le=300)
    height: int = Field(default=30, ge=5, le=150)
    seed: int = Field(default=0, ge=0, le=4294967295)
    tooltips: bool = True
    notifications: bool = True


class Press(Model):
    kind: Literal["press"]
    keys: list[str] = Field(min_length=1, max_length=256)


class Paste(Model):
    kind: Literal["paste"]
    text: str = Field(max_length=100_000)


class Mouse(Model):
    kind: Literal["click", "hover", "mouse_down", "mouse_up", "mouse_move", "scroll"]
    selector: str | None = Field(
        default=None, description="Unique CSS selector, or screen coordinates."
    )
    x: int = Field(default=0, description="Cell offset from the widget or screen origin.")
    y: int = 0
    button: int = Field(default=1, ge=0, le=3)
    shift: bool = False
    control: bool = False
    meta: bool = False
    times: int = Field(default=1, ge=1, le=3)
    direction: Literal["up", "down", "left", "right"] = "down"
    amount: int = Field(default=1, ge=1, le=100)


class Focus(Model):
    kind: Literal["focus"]
    selector: str


class Resize(Model):
    kind: Literal["resize"]
    width: int = Field(ge=10, le=300)
    height: int = Field(ge=5, le=150)


class Pause(Model):
    kind: Literal["pause"]
    seconds: float = Field(default=0.05, ge=0, le=10)


class Wait(Model):
    kind: Literal["wait"]
    selector: str
    condition: Literal["exists", "absent", "visible", "focused", "enabled", "text", "attribute"]
    value: Any = None
    attribute: str | None = None
    timeout: float = Field(default=5, gt=0, le=30)

    @model_validator(mode="after")
    def check_condition(self) -> "Wait":
        if self.condition == "attribute" and (not self.attribute or self.attribute.startswith("_")):
            raise ValueError("attribute waits require a public attribute name")
        if self.condition == "text" and not isinstance(self.value, str):
            raise ValueError("text waits require a string value (substring match)")
        return self


class AppAction(Model):
    kind: Literal["action"]
    action: str = Field(description="Textual action expression, e.g. app.show_help.")


class Capture(Model):
    kind: Literal["capture"]
    label: str = Field(default="Screenshot", max_length=200)
    selector: str | None = Field(default=None, description="Crop to the widget's visible region.")
    padding: int = Field(default=1, ge=0, le=10)


Action = Annotated[
    Press | Paste | Mouse | Focus | Resize | Pause | Wait | AppAction | Capture,
    Field(discriminator="kind"),
]
actions_adapter = TypeAdapter(Annotated[list[Action], Field(min_length=1, max_length=100)])


class Scenario(Model):
    version: Literal[1] = 1
    launch: Launch
    actions: list[Action] = Field(default_factory=list, max_length=2000)
