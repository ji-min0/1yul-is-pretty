"""
파이썬을 사용한 웹-like 디자인

Includes:
- Window: 레이어에 따라 그리고 이벤트를 처리
- Layer: z-indexed container of widgets
- BaseWidget: 간단한 위젯 클래스
- Button: 마우스를 가져다 올림 / 클릭을 처리하는 버튼
- TextLabel: 정적인 텍스트 라벨
- TextOutput: 스크롤 가능한 텍스트박스

예제
pygame.display.set_mode. Use from your main loop like:

    import pygame
    from window import Window, Layer, Button, TextLabel, TextOutput

    pygame.init()
    screen = pygame.display.set_mode((960, 600))
    clock = pygame.time.Clock()

    ui = Window(size=screen.get_size())
    base = ui.add_layer("base", z_index=0)
    overlays = ui.add_layer("overlays", z_index=10)

    btn = Button((24, 24, 160, 40), text="Click Me")
    out = TextOutput((24, 80, 600, 200))
    lbl = TextLabel((200, 24, 300, 40), text="Header")

    base.add(btn)
    base.add(lbl)
    base.add(out)

    btn.on_click = lambda b: out.append_line("Button clicked!")

    running = True
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                ui.handle_event(event)

        ui.update(dt)
        ui.draw(screen)
        pygame.display.flip()

"""

from __future__ import annotations

from typing import Callable, List, Optional, Sequence, Tuple, Union

import pygame


Color = Tuple[int, int, int]
RectLike = Union[pygame.Rect, Tuple[int, int, int, int]]


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def lighten(color: Color, amount: float) -> Color:
    r, g, b = color
    return (
        int(_clamp(r + (255 - r) * amount, 0, 255)),
        int(_clamp(g + (255 - g) * amount, 0, 255)),
        int(_clamp(b + (255 - b) * amount, 0, 255)),
    )


def darken(color: Color, amount: float) -> Color:
    r, g, b = color
    return (
        int(_clamp(r * (1 - amount), 0, 255)),
        int(_clamp(g * (1 - amount), 0, 255)),
        int(_clamp(b * (1 - amount), 0, 255)),
    )


DEFAULT_BG: Color = (245, 246, 248)
DEFAULT_FG: Color = (28, 30, 33)
ACCENT: Color = (31, 119, 180)
MUTED: Color = (200, 205, 210)
BORDER: Color = (180, 185, 190)
SURFACE: Color = (255, 255, 255)


def ensure_font_initialized() -> None:
    if not pygame.font.get_init():
        pygame.font.init()


def default_font(size: int = 16) -> pygame.font.Font:
    ensure_font_initialized()
    return pygame.font.Font(None, size)


# ---------- Core Widgets ----------


class BaseWidget:
    
    #자식 클래스를 만들어 오버라이드가 필요합니다

    def __init__(self, rect: RectLike, visible: bool = True, enabled: bool = True):
        self.rect: pygame.Rect = pygame.Rect(rect)
        self.visible: bool = visible
        self.enabled: bool = enabled
        self.children: List[BaseWidget] = []
        self.parent: Optional[BaseWidget] = None
        self.hovered: bool = False

    def add(self, widget: "BaseWidget") -> "BaseWidget":
        widget.parent = self
        self.children.append(widget)
        return widget

    def remove(self, widget: "BaseWidget") -> None:
        if widget in self.children:
            self.children.remove(widget)
            widget.parent = None

    @property
    def abs_rect(self) -> pygame.Rect:
        if self.parent is None:
            return self.rect.copy()
        p = self.parent.abs_rect
        r = self.rect.copy()
        r.x += p.x
        r.y += p.y
        return r

    def contains_point(self, pos: Tuple[int, int]) -> bool:
        return self.abs_rect.collidepoint(pos)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not (self.enabled and self.visible):
            return False

        for child in reversed(self.children):
            if child.handle_event(event):
                return True
        return False

    def update(self, dt: float) -> None:
        for c in self.children:
            c.update(dt)

    def draw_self(self, surface: pygame.Surface) -> None:

        pass

    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        self.draw_self(surface)
        for c in self.children:
            c.draw(surface)


class TextLabel(BaseWidget):
    def __init__(
        self,
        rect: RectLike,
        text: str = "",
        font_size: int = 18,
        color: Color = DEFAULT_FG,
        bg: Optional[Color] = None,
        align: str = "left",
    ):
        super().__init__(rect)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.bg = bg
        self.align = align  # 정렬 "left", "center", "right"
        self._font = default_font(font_size)

    def set_text(self, text: str) -> None:
        self.text = text

    def draw_self(self, surface: pygame.Surface) -> None:
        r = self.abs_rect
        if self.bg is not None:
            pygame.draw.rect(surface, self.bg, r, border_radius=6)
        if not self.text:
            return
        ensure_font_initialized()
        if self._font.get_height() != default_font(self.font_size).get_height():
            self._font = default_font(self.font_size)
        ts = self._font.render(self.text, True, self.color)
        tx = r.x + 10
        if self.align == "center":
            tx = r.centerx - ts.get_width() // 2
        elif self.align == "right":
            tx = r.right - ts.get_width() - 10
        ty = r.centery - ts.get_height() // 2
        surface.blit(ts, (tx, ty))


class Button(BaseWidget):
    def __init__(
        self,
        rect: RectLike,
        text: str = "   ",
        on_click: Optional[Callable[["Button"], None]] = None,
        *,
        font_size: int = 18,
        bg: Color = ACCENT,
        fg: Color = (255, 255, 255),
        hover: Optional[Color] = None,
        pressed: Optional[Color] = None,
        border_radius: int = 10,
    ):
        super().__init__(rect)
        self.text = text
        self.on_click = on_click
        self.font_size = font_size
        self.bg = bg
        self.fg = fg
        self.hover_bg = hover or lighten(bg, 0.12)
        self.pressed_bg = pressed or darken(bg, 0.12)
        self.border_radius = border_radius
        self._font = default_font(font_size)
        self._is_pressed = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not (self.enabled and self.visible):
            return False

        consumed = super().handle_event(event)
        if consumed:
            return True

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.contains_point(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.contains_point(event.pos):
                self._is_pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self._is_pressed
            self._is_pressed = False
            if was_pressed and self.contains_point(event.pos):
                if self.on_click:
                    self.on_click(self)
                return True
        return False

    def draw_self(self, surface: pygame.Surface) -> None:
        r = self.abs_rect
        bg = self.bg
        if self._is_pressed:
            bg = self.pressed_bg
        elif self.hovered:
            bg = self.hover_bg

        pygame.draw.rect(surface, bg, r, border_radius=self.border_radius)
        pygame.draw.rect(surface, darken(bg, 0.28), r, width=1, border_radius=self.border_radius)

        ensure_font_initialized()
        if self._font.get_height() != default_font(self.font_size).get_height():
            self._font = default_font(self.font_size)
        ts = self._font.render(self.text, True, self.fg)
        surface.blit(ts, (r.centerx - ts.get_width() // 2, r.centery - ts.get_height() // 2))


class TextOutput(BaseWidget):
    def __init__(
        self,
        rect: RectLike,
        *,
        font_size: int = 16,
        text_color: Color = DEFAULT_FG,
        bg_color: Color = SURFACE,
        border_color: Color = BORDER,
        padding: int = 8,
        max_lines: int = 1000,
        border_radius: int = 8,
    ):
        super().__init__(rect)
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.padding = padding
        self.max_lines = max_lines
        self.border_radius = border_radius
        self._font = default_font(font_size)
        self._lines: List[str] = []
        self._scroll: int = 0  # in pixels, 0 means bottom-most (auto)

    # ----- API -----
    def append_line(self, text: str) -> None:
        self._lines.append(text)
        if len(self._lines) > self.max_lines:
            overflow = len(self._lines) - self.max_lines
            self._lines = self._lines[overflow:]
        # auto-scroll to bottom
        self._scroll = 0

    def clear(self) -> None:
        self._lines.clear()
        self._scroll = 0

    # ----- Events -----
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not (self.enabled and self.visible):
            return False
        consumed = super().handle_event(event)
        if consumed:
            return True
        if event.type == getattr(pygame, "MOUSEWHEEL", None):
            # positive y -> scroll up
            r = self.abs_rect
            mx, my = pygame.mouse.get_pos()
            if r.collidepoint(mx, my):
                line_h = self._font.get_linesize()
                self._scroll += -event.y * line_h * 2
                self._scroll = max(0, self._scroll)
                return True
        return False

    # ----- Draw -----
    def draw_self(self, surface: pygame.Surface) -> None:
        r = self.abs_rect
        pygame.draw.rect(surface, self.bg_color, r, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.border_color, r, width=1, border_radius=self.border_radius)

        # Compute text area
        inner = r.inflate(-2 * self.padding, -2 * self.padding)

        # Render visible lines from bottom up according to scroll
        line_h = self._font.get_linesize()
        max_lines_visible = max(1, inner.h // line_h)
        total_h = line_h * len(self._lines)
        # scrolled pixels from bottom; 0 means bottom aligned
        scroll_px = int(self._scroll)
        start_px = max(0, total_h - inner.h - scroll_px)

        # Determine first line index and pixel offset within that line
        first_idx = start_px // line_h
        offset_px = -(start_px % line_h)

        y = inner.y + offset_px
        idx = first_idx
        while idx < len(self._lines) and y < inner.bottom:
            txt = self._lines[idx]
            ts = self._font.render(txt, True, self.text_color)
            surface.blit(ts, (inner.x, y))
            y += line_h
            idx += 1


# ---------- Layer & Window ----------


class Layer:
    """A z-indexed container for widgets."""

    def __init__(self, name: str, z_index: int = 0, visible: bool = True):
        self.name = name
        self.z_index = z_index
        self.visible = visible
        self.widgets: List[BaseWidget] = []

    def add(self, widget: BaseWidget) -> BaseWidget:
        self.widgets.append(widget)
        return widget

    def remove(self, widget: BaseWidget) -> None:
        if widget in self.widgets:
            self.widgets.remove(widget)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible:
            return False
        for w in reversed(self.widgets):
            if w.handle_event(event):
                return True
        return False

    def update(self, dt: float) -> None:
        if not self.visible:
            return
        for w in self.widgets:
            w.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        for w in self.widgets:
            w.draw(surface)


class Window:

    def __init__(self, size: Tuple[int, int], background: Color = DEFAULT_BG):
        self.size = size
        self.background = background
        self._layers: List[Layer] = []

    # ----- Layers -----
    def add_layer(self, name: str, z_index: int = 0, visible: bool = True) -> Layer:
        if any(l.name == name for l in self._layers):
            raise ValueError(f"Layer with name '{name}' already exists")
        layer = Layer(name=name, z_index=z_index, visible=visible)
        self._layers.append(layer)
        self._sort_layers()
        return layer

    def get_layer(self, name: str) -> Optional[Layer]:
        for l in self._layers:
            if l.name == name:
                return l
        return None

    def remove_layer(self, name: str) -> None:
        self._layers = [l for l in self._layers if l.name != name]

    def _sort_layers(self) -> None:
        self._layers.sort(key=lambda l: l.z_index)

    # ----- Event / Update / Draw -----
    def handle_event(self, event: pygame.event.Event) -> bool:
        for layer in reversed(self._layers):  # top-most first
            if layer.handle_event(event):
                return True
        return False

    def update(self, dt: float) -> None:
        for layer in self._layers:
            layer.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        # fill background and draw layers bottom to top
        surface.fill(self.background)
        for layer in self._layers:
            layer.draw(surface)


__all__ = [
    "Window",
    "Layer",
    "BaseWidget",
    "Button",
    "TextLabel",
    "TextOutput",
]
