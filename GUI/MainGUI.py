#Needed to import Server module
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

os.environ['KIVY_IMAGE'] = 'pil,sdl'

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.popup import Popup

import ResultGraph as Graph
from Server import PostgresqlDB as DB

#Initialize global variables with empty value
database = None
author_list = []
result_dict = None
graph = None

#The other global variables
screenManager = None
initializeDBScreen = None
inputAuthorNameScreen = None
displayResultScreen = None

#Screen classes definition
class InitializeDBScreen(Screen):

	def __init__(self, **kwargs):
		super(InitializeDBScreen, self).__init__(**kwargs)
		self.grid_layout = GridLayout(cols=2, rows=6)
		self.add_widget(self.grid_layout)
		self.grid_layout.cols = 2
		self.grid_layout.rows = 6
		#Database host
		self.grid_layout.add_widget(Label(text="Database Host"))
		self.database_host = TextInput(multiline=False)
		self.grid_layout.add_widget(self.database_host)
		#Database port
		self.grid_layout.add_widget(Label(text="Database Port"))
		self.database_port = TextInput(multiline=False)
		self.grid_layout.add_widget(self.database_port)
		#Database name
		self.grid_layout.add_widget(Label(text="Database Name"))
		self.database_name = TextInput(multiline=False)
		self.grid_layout.add_widget(self.database_name)
		#Username
		self.grid_layout.add_widget(Label(text="Username"))
		self.username = TextInput(multiline=False)
		self.grid_layout.add_widget(self.username)
		#Password
		self.grid_layout.add_widget(Label(text="Password"))
		self.password = TextInput(password=True, multiline=False)
		self.grid_layout.add_widget(self.password)
		#Establish connection button
		self.btn_establish_connection = Button(text="Connect")
		self.btn_establish_connection.bind(on_press=self.establish_connection)
		self.grid_layout.add_widget(self.btn_establish_connection)
		# Exit button
		self.btn_exit = Button(text="Exit")
		self.btn_exit.bind(on_press=self.exit)
		self.grid_layout.add_widget(self.btn_exit)

	def establish_connection(self, *args):
		database_name = self.database_name.text
		username = self.username.text
		password = self.password.text
		global database
		database = DB.DatabasePostgresql(database_name, username, password)
		if database.conn != None:
			screenManager.current = 'inputAuthorNameScreen'
		else:
			close_btn = Button(text="Cannot establish connection to database.\nClick to close.")
			popup = Popup(title="Connection error",
			              content=close_btn,
			              auto_dismiss=False,
			              size_hint=(0.4, 0.4))
			close_btn.bind(on_press=popup.dismiss)
			popup.open()

	def exit(self, *args):
		exit()

class InputAuthorNameScreen(Screen):

	def __init__(self, **kwargs):
		self.bind(on_pre_enter=self.empty_all_entries)
		super(InputAuthorNameScreen, self).__init__(**kwargs)
		self.grid_layout = GridLayout(cols=2, rows=6)
		self.add_widget(self.grid_layout)
		self.grid_layout.cols = 2
		self.grid_layout.rows = 9
		# Author 1
		self.grid_layout.add_widget(Label(text="Author 1 (Leave black if not used)"))
		self.author_1 = TextInput(multiline=False)
		self.grid_layout.add_widget(self.author_1)
		# Author 2
		self.grid_layout.add_widget(Label(text="Author 2 (Leave black if not used)"))
		self.author_2 = TextInput(multiline=False)
		self.grid_layout.add_widget(self.author_2)
		# Author 3
		self.grid_layout.add_widget(Label(text="Author 3 (Leave black if not used)"))
		self.author_3 = TextInput(multiline=False)
		self.grid_layout.add_widget(self.author_3)
		# Author 4
		self.grid_layout.add_widget(Label(text="Author 4 (Leave black if not used)"))
		self.author_4 = TextInput(multiline=False)
		self.grid_layout.add_widget(self.author_4)
		# Author 5
		self.grid_layout.add_widget(Label(text="Author 5 (Leave black if not used)"))
		self.author_5 = TextInput(multiline=False)
		self.grid_layout.add_widget(self.author_5)
		# Author 6
		self.grid_layout.add_widget(Label(text="Author 6 (Leave black if not used)"))
		self.author_6 = TextInput(multiline=False)
		self.grid_layout.add_widget(self.author_6)
		# Author 7
		self.grid_layout.add_widget(Label(text="Author 7 (Leave black if not used)"))
		self.author_7 = TextInput(multiline=False)
		self.grid_layout.add_widget(self.author_7)
		# Author 8
		self.grid_layout.add_widget(Label(text="Author 8 (Leave black if not used)"))
		self.author_8 = TextInput(multiline=False)
		self.grid_layout.add_widget(self.author_8)
		#Find connectivity button
		self.btn_find_connectivity = Button(text="Find Connectivity")
		self.btn_find_connectivity.bind(on_press=self.find_connectivity)
		self.grid_layout.add_widget(self.btn_find_connectivity)
		# Exit button
		self.btn_exit = Button(text="Exit")
		self.btn_exit.bind(on_press=self.exit)
		self.grid_layout.add_widget(self.btn_exit)

	def empty_all_entries(self, *args):
		self.author_1.text = ''
		self.author_2.text = ''
		self.author_3.text = ''
		self.author_4.text = ''
		self.author_5.text = ''
		self.author_6.text = ''
		self.author_7.text = ''
		self.author_8.text = ''

	def find_connectivity(self, *args):
		self.get_author_list()
		global author_list
		if database.conn != None:
			#need to create view first
			database.createPublicationCompleteView()
			author_list_returned = database.processListOfName(author_list)
			global result_dict
			#Temporarily hard-codeds
			result_dict = database.execute(author_list_returned)
			# database.closeDatabase()
		#After connectivity is available, draw the graph
		graph = None
		if result_dict != None:
			graph = Graph.get_graph_of(result_dict)
		if graph != None:
			Graph.get_drawing_of(graph)
			screenManager.current = 'displayResultScreen'

	def get_author_list(self, *args):
		#Do something
		global author_list
		author_list = []
		if self.author_1.text != '':
			author_list.append(self.author_1.text)
		if self.author_2.text != '':
			author_list.append(self.author_2.text)
		if self.author_3.text != '':
			author_list.append(self.author_3.text)
		if self.author_4.text != '':
			author_list.append(self.author_4.text)
		if self.author_5.text != '':
			author_list.append(self.author_5.text)
		if self.author_6.text != '':
			author_list.append(self.author_6.text)
		if self.author_7.text != '':
			author_list.append(self.author_7.text)
		if self.author_8.text != '':
			author_list.append(self.author_8.text)

	def exit(self, *args):
		exit()


class DisplayResultScreen(Screen):

	def __init__(self, **kwargs):
		super(DisplayResultScreen, self).__init__(**kwargs)
		self.grid_layout = GridLayout()
		self.grid_layout.cols = 1
		self.grid_layout.rows = 3
		self.add_widget(self.grid_layout)
		#Result image
		self.image_result = Image(source='diagram.png', size_hint_y=0.8)
		self.grid_layout.add_widget(self.image_result)
		# Try again button
		self.btn_try_again = Button(text="Try again", size_hint_y=0.1)
		self.btn_try_again.bind(on_press=self.try_again)
		self.grid_layout.add_widget(self.btn_try_again)
		# Exit button
		self.btn_exit = Button(text="Exit", size_hint_y=0.1)
		self.btn_exit.bind(on_press=self.exit)
		self.grid_layout.add_widget(self.btn_exit)

	def try_again(self, *args):
		screenManager.current = 'inputAuthorNameScreen'

	def exit(self, *args):
		exit()

#Define screen classes
initializeDBScreen = InitializeDBScreen(name='initializeDBScreen')
inputAuthorNameScreen = InputAuthorNameScreen(name='inputAuthorNameScreen')
displayResultScreen = DisplayResultScreen(name='displayResultScreen')

#Define screen manager
screenManager = ScreenManager()
screenManager.add_widget(initializeDBScreen)
screenManager.add_widget(inputAuthorNameScreen)
screenManager.add_widget(displayResultScreen)

class MainApp(App):
	def build(self):
		screenManager.current = 'initializeDBScreen'
		return screenManager

if __name__ == '__main__':
	MainApp().run()