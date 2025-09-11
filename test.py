import flet as ft
import asyncio

def main(page: ft.Page):
	page.title = "한율이는이쁘다"
	page.horizontal_alignment = "center"
	page.vertical_alignment = "center"
	page.bgcolor = "#492158"

	def make_fade_slide(widget, w, h, start_top=24):
		inner = ft.Container(
			content=widget,
			top=start_top, left=0, opacity=0,
			animate_position=ft.Animation(400, "ease_out"),
			animate_opacity=ft.Animation(400, "ease_out"),
			alignment=ft.alignment.center,
		)
		host = ft.Container(ft.Stack([inner], width=w, height=h))
		return host, inner

	title_host, title_in = make_fade_slide(
		ft.Text("파이썬 프로젝트 모음", size=48, color="#FAFAFA", weight="bold"),
		w=720, h=80
	)
	desc_host, desc_in = make_fade_slide(
		ft.Text("블로그 + 욕설 필터링 + 파이썬 퀴즈", size=14, color="#BEBEBE"),
		w=720, h=40
	)
	btns = ft.Row(
		[ft.FilledButton("회원가입"), ft.OutlinedButton("로그인")],
		alignment="center", spacing=12
	)
	btn_host, btn_in = make_fade_slide(btns, w=720, h=80)

	page.add(
		ft.Container(
			content=ft.Column(
				[title_host, desc_host, btn_host],
				spacing=8, horizontal_alignment="center", alignment="center"
			),
			padding=50
		)
	)

	async def intro():
		await asyncio.sleep(0.05)
		title_in.top = 0; title_in.opacity = 1; page.update()
		await asyncio.sleep(0.12)
		desc_in.top = 0; desc_in.opacity = 1; page.update()
		await asyncio.sleep(0.12)
		btn_in.top = 0; btn_in.opacity = 1; page.update()

	page.run_task(intro)

ft.app(target=main)