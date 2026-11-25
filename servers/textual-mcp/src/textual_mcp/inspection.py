"""Bounded observations; private Textual compatibility points are kept explicit."""

import inspect
import math
from typing import Any

from textual.app import App
from textual.geometry import Region
from textual.widget import Widget


def value_of(value: Any, depth: int = 0) -> Any:
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    if isinstance(value, str):
        return value[:2000] + ("… [truncated]" if len(value) > 2000 else "")
    if depth >= 3:
        return f"<{type(value).__name__}>"
    if isinstance(value, (tuple, list)):
        result = [value_of(v, depth + 1) for v in value[:30]]
        if len(value) > 30:
            result.append(f"… {len(value) - 30} more")
        return result
    if isinstance(value, dict):
        return {str(k): value_of(v, depth + 1) for k, v in list(value.items())[:30]}
    if isinstance(value, Widget):
        return identity(value)
    # Do not invoke arbitrary application __repr__ methods during inspection.
    return f"<{type(value).__module__}.{type(value).__qualname__}>"


def identity(widget: Any) -> str | None:
    if widget is None:
        return None
    widget_id = getattr(widget, "id", None)
    return f"#{widget_id}" if widget_id else type(widget).__name__


def source_of(obj: Any) -> dict[str, Any]:
    try:
        return {
            "file": inspect.getsourcefile(obj),
            "line": inspect.getsourcelines(obj)[1],
            "qualified_name": f"{obj.__module__}.{obj.__qualname__}",
        }
    except (TypeError, OSError, AttributeError):
        return {"qualified_name": getattr(obj, "__qualname__", type(obj).__name__)}


def visible_region(widget: Widget) -> Region:
    if not widget.display or not widget.visible:
        return Region()
    try:
        geometry = widget.screen.find_widget(widget)
    except Exception:
        return Region()
    return geometry.region.intersection(geometry.clip).intersection(widget.screen.size.region)


def handlers_of(cls: type) -> dict:
    return {
        name: source_of(method)
        for name, method in inspect.getmembers(cls, inspect.isfunction)
        if name.startswith(("on_", "action_", "watch_")) or hasattr(method, "_textual_on")
    }


def text_of(widget: Widget) -> str:
    """Rendered widget content, bounded to the first 30 local content lines."""
    if getattr(widget, "password", False):
        return "[password input]"
    return "\n".join(widget.render_line(y).text for y in range(min(widget.size.height, 30)))[:4000]


def unique_widget(app: App, selector: str) -> Widget:
    matches = list(app.screen.query(selector))
    if not matches:
        raise ValueError(f"No widget matches {selector!r} on the active screen. Inspect first.")
    if len(matches) != 1:
        raise ValueError(
            f"Selector {selector!r} matches {len(matches)} widgets; use a unique selector."
        )
    return matches[0]


def snapshot(app: App) -> dict[str, Any]:
    return {
        "size": {"width": app.size.width, "height": app.size.height},
        "screen": identity(app.screen),
        "screen_stack": [identity(screen) for screen in app.screen_stack],
        "focus": identity(app.focused),
        "theme": app.theme,
        "running": app.is_running,
    }


def inspect_app(
    app: App,
    selector: str | None = None,
    limit: int = 50,
    offset: int = 0,
    details: bool = False,
) -> dict[str, Any]:
    widgets = list(app.screen.query(selector)) if selector else list(app.screen.walk_children())
    output = []
    for widget in widgets[offset : offset + limit]:
        if not isinstance(widget, Widget):
            continue
        row = {
            "widget": identity(widget),
            "type": f"{type(widget).__module__}.{type(widget).__qualname__}",
            "id": widget.id,
            "classes": sorted(widget.classes),
            "parent": identity(widget.parent),
            "region": widget.region._asdict(),
            "visible_region": visible_region(widget)._asdict(),
            "display": widget.display,
            "visible": widget.visible,
            "disabled": widget.disabled,
            "effective_disabled": widget.is_disabled,
            "focused": widget.has_focus,
            "can_focus": widget.can_focus,
        }
        try:
            row["text"] = text_of(widget)
        except Exception as error:
            row["text_error"] = str(error)
        state = {}
        attributes = {"value", "text", "placeholder", "scroll_x", "scroll_y"}
        if details:
            attributes.update(getattr(type(widget), "_reactives", {}))
        for name in sorted(attributes):
            if name.startswith("_"):
                continue
            try:
                if getattr(widget, "password", False) and name in {"value", "text"}:
                    state[name] = "[redacted]"
                elif hasattr(widget, name):
                    state[name] = value_of(getattr(widget, name))
            except Exception as error:
                state[name] = {"error": str(error)}
        row["state"] = state
        if details:
            row["source"] = source_of(type(widget))
            row["styles"] = widget.styles.css[:6000]
            row["handlers"] = handlers_of(type(widget))
        output.append(row)
    result = {**snapshot(app), "widgets": output, "total": len(widgets)}
    result["next_offset"] = offset + limit if len(widgets) > offset + limit else None
    if details:
        result["app_source"] = source_of(type(app))
        result["css_paths"] = [str(path) for path in app.css_path]
        result["bindings"] = [
            {
                "key": key,
                "action": binding.binding.action,
                "description": binding.binding.description,
            }
            for key, binding in app.screen.active_bindings.items()
        ]
        result["app_handlers"] = handlers_of(type(app))
        result["workers"] = [
            {"name": worker.name, "state": worker.state.name, "error": str(worker.error)}
            for worker in app.workers
        ]
    return result
