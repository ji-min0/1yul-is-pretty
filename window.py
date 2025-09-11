from __future__ import annotations

from typing import Callable, List, Optional, Sequence, Tuple, Union

import pygame; import os


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

def safe_load_image(img_path:str, rect=None, alpha=False):
        try:
            BASE_DIR = os.path.dirname(__file__)
            safe_paths = img_path.split("/") # 이미지 경로를 / 로 나눔
            full_safe_path = os.path.join(BASE_DIR, *safe_paths) # path join으로 안전하게 불러오기
            img = pygame.image.load(full_safe_path) # 이미지 로드
            img = img.convert_alpha() if alpha else img.convert()
            if rect:
                img_rect = pygame.Rect(rect)
                img = pygame.transform.scale(img, (img_rect.height,img_rect.width))
            return img
        except Exception as e:
            print(e)
            return None

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
    try:
        return pygame.font.Font(os.path.join("assets","font.ttf"), size)
    except:
        return pygame.font.Font(None, size)


# ---------- Core Widgets ----------


class BaseWidget:
    def __init__(self, rect: RectLike = (0,0,0,0), visible: bool = True, enabled: bool = True):
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

class Animation():
    def __init__(
            self,
            duration = 0.15
        ):
        self.progress = 0.0 # 0 ~ 1
        self.duration = duration
        self.current_duration = 0.0
        self.direction = 0
    def reset(self):
        self.progress = 0.0
        self.current_duration = 0
    def update(self,dt) -> float:
        if self.is_playing:
            self.current_duration += dt * self.direction
            self.progress = min(1, max(0, self.current_duration / self.duration))

class Image(BaseWidget):
    def __init__(
        self,
        image_path: str,
        rect: RectLike = None
        ):
        super().__init__()
        self._is_pressed = False
        self.img = safe_load_image(image_path,rect)
    def draw_self(self, surface = pygame.surface):
        surface.blit(self.img,self.rect.topleft)

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
        self.hover_anim = Animation()

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
            self.hover_anim.direction = 1
        else:
            self.hover_anim.direction = -1

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
    def print(self, text: str) -> None:
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

class TextInput(BaseWidget):
    def init(
        self,
        rect: RectLike,
        text: str = "",
        *,
        placeholder: str = "",
        font_size: int = 18,
        fg: Color = DEFAULT_FG,
        bg: Color = SURFACE,
        border_color: Color = BORDER,
        focus_color: Color = ACCENT,
        padding: int = 8,
        border_radius: int = 8,
        on_submit: Optional[Callable[["TextInput", str], None]] = None,
        ):
        super().init(rect)
        self.text = text
        self.placeholder = placeholder
        self.font_size = font_size
        self.fg = fg
        self.bg = bg
        self.border_color = border_color
        self.focus_color = focus_color
        self.padding = padding
        self.border_radius = border_radius
        self.on_submit = on_submit
        self._font = default_font(font_size)
        self._focused = False
        self._caret = len(text)
        self._blink_time = 0.0
        self._blink_visible = True
        self._blink_interval = 0.55
        self._scroll_px = 0  # v scroll

    def focus(self) -> None:
        self._focused = True
        self._blink_time = 0.0
        self._blink_visible = True
        try:
            pygame.key.start_text_input()
        except Exception:
            pass

    def blur(self) -> None:
        self._focused = False
        try:
            pygame.key.stop_text_input()
        except Exception:
            pass
# Text helpers
    def set_text(self, text: str) -> None:
        self.text = text
        self._caret = min(self._caret, len(self.text))
        self._ensure_caret_visible()

    def _insert_text(self, s: str) -> None:
        if not s:
            return
        self.text = self.text[: self._caret] + s + self.text[self._caret :]
        self._caret += len(s)
        self._ensure_caret_visible()

    def _backspace(self) -> None:
        if self._caret > 0:
            self.text = self.text[: self._caret - 1] + self.text[self._caret :]
            self._caret -= 1
            self._ensure_caret_visible()

    def _delete(self) -> None:
        if self._caret < len(self.text):
            self.text = self.text[: self._caret] + self.text[self._caret + 1 :]
            self._ensure_caret_visible()

    def _move_caret(self, delta: int) -> None:
        self._caret = int(_clamp(self._caret + delta, 0, len(self.text)))
        self._ensure_caret_visible()

    def _caret_home(self) -> None:
        self._caret = 0
        self._ensure_caret_visible()

    def _caret_end(self) -> None:
        self._caret = len(self.text)
        self._ensure_caret_visible()

    def _text_width(self, s: str) -> int:
        return self._font.size(s)[0]

    def _caret_px(self) -> int:
        return self._text_width(self.text[: self._caret])

    def _ensure_caret_visible(self) -> None:
        inner = self.abs_rect.inflate(-2 * self.padding, -2 * self.padding)
        caret_x = self._caret_px()
        if caret_x - self._scroll_px > inner.w - 2:
            self._scroll_px = caret_x - inner.w + 2
        if caret_x - self._scroll_px < 0:
            self._scroll_px = caret_x - 2
        self._scroll_px = max(0, self._scroll_px)

    # Events
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not (self.enabled and self.visible):
            return False

        if super().handle_event(event):
            return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            inside = self.contains_point(event.pos)
            if inside:
                self.focus()
                inner = self.abs_rect.inflate(-2 * self.padding, -2 * self.padding)
                cx = event.pos[0] - inner.x + self._scroll_px
                best_i, best_dx = 0, 1e9
                for i in range(len(self.text) + 1):
                    x = self._text_width(self.text[:i])
                    dx = abs(x - cx)
                    if dx < best_dx:
                        best_i, best_dx = i, dx
                self._caret = best_i
                self._ensure_caret_visible()
                return True
            else:
                if self._focused:
                    self.blur()
                return False

        if not self._focused:
            return False

        if event.type == getattr(pygame, "TEXTINPUT", None):
            self._insert_text(event.text)
            return True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self._backspace(); return True
            if event.key == pygame.K_DELETE:
                self._delete(); return True
            if event.key == pygame.K_LEFT:
                self._move_caret(-1); return True
            if event.key == pygame.K_RIGHT:
                self._move_caret(1); return True
            if event.key == pygame.K_HOME:
                self._caret_home(); return True
            if event.key == pygame.K_END:
                self._caret_end(); return True
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self.on_submit:
                    self.on_submit(self, self.text)
                return True
        return False

    # Update / Draw
    def update(self, dt: float) -> None:
        super().update(dt)
        if self._focused:
            self._blink_time += dt
            if self._blink_time >= self._blink_interval:
                self._blink_time -= self._blink_interval
                self._blink_visible = not self._blink_visible
        else:
            self._blink_visible = False

    def draw_self(self, surface: pygame.Surface) -> None:
        r = self.abs_rect
        inner = r.inflate(-2 * self.padding, -2 * self.padding)

        pygame.draw.rect(surface, self.bg, r, border_radius=self.border_radius)
        border_col = self.focus_color if self._focused else self.border_color
        pygame.draw.rect(surface, border_col, r, width=1, border_radius=self.border_radius)

        prev_clip = surface.get_clip()
        surface.set_clip(inner)

        txt_color = self.fg if (self.text or self._focused) else MUTED
        display_text = self.text if self.text else self.placeholder
        text_x = inner.x - self._scroll_px
        text_y = inner.centery - self._font.get_height() // 2
        ts = self._font.render(display_text, True, txt_color)
        surface.blit(ts, (text_x, text_y))

        if self._focused and self._blink_visible:
            caret_x = inner.x + self._caret_px() - self._scroll_px
            caret_y1 = inner.y + 3
            caret_y2 = inner.bottom - 3
            pygame.draw.line(surface, txt_color, (caret_x, caret_y1), (caret_x, caret_y2), 1)
        
        surface.set_clip(prev_clip)






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
    "TextInput",
    "Animation",
    "Image",
]
