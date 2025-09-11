from nicegui import ui, app; import platform

# setup
app.native.window_args['width'] = 960
app.native.window_args['height'] = 600
if platform.system() == "Windows":
	app.native.start_args['gui'] = 'edgechromium'

# header
with ui.header().style('background: linear-gradient(to right, #9333ea, #3b82f6); color: white;'):
	ui.label('14기 프로젝트 모음집').style('color: white; font-weight: bold;')

ui.run(title='한율이는 이쁘다', native=True, reload=False)