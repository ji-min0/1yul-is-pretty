import flet as ft


def main(page: ft.Page):
	page.title = "한율이는이쁘다"
	page.horizontal_alignment = "center"
	page.vertical_alignment = "center"
	page.add(
		ft.Container(
            ft.Column(
                [ft.Text("파이썬 프로젝트 모음", size=48, color="#FAFAFA",weight="bold"),
                ft.Text("블로그 + 욕설 필터링 + 파이썬 퀴즈", size=12, color="#BEBEBE")],
                spacing=10,
                horizontal_alignment= "center"
            ),
			padding=50
        )
    )
	page.add(
        ft.Row(
            [ft.Button('로그인'),ft.Button('회원가입')],
			alignment="center"
        )
    )

ft.app(target=main)