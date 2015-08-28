from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty, BooleanProperty
from kivy.uix.label import Label 
from kivy.clock import Clock

from random import shuffle

COLOR_SET = [ 	[1,0,0,1],
				[0,1,0,1],
				[0,0,1,1],
				[1,1,0,1],
				[1,0,1,1],
				[0,1,1,1]] 
EMPTY_COLOR = [.5,.5,.5,1]
BOARD_SIZE = 25
BOARD_DIMENSION = 5
GOAL_SIZE = 9
GOAL_DIMENSION = 3

def getCoords(index):
	#coords start in br, go rl-bt direction
	return (BOARD_DIMENSION - (index % BOARD_DIMENSION), BOARD_DIMENSION - (index / BOARD_DIMENSION)) 

def areAdjacentCoords(c1,c2):
	return 	((c1[0] == c2[0] ) and ((c1[1] == c2[1] - 1 ) or (c1[1] == c2[1] + 1 ))) or ((c1[1] == c2[1] ) and ((c1[0] == c2[0] - 1 ) or (c1[0] == c2[0] + 1 )))

def areAdjacentIndices(i1, i2):
	return areAdjacentCoords(getCoords(i1),getCoords(i2))

def goalIndexToPlayerIndex(gi):
	return gi%GOAL_DIMENSION + BOARD_DIMENSION * (gi/GOAL_DIMENSION + 1) + 1 



class AppSpace(FloatLayout):
	pass

class ColorSquare(Widget):
	color = ListProperty([1,1,1,1])
	def __init__(self, color, **kw):
		super(ColorSquare, self).__init__(**kw)
		self.color = color


	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			self.parent.moveSquare(self)
		return super(ColorSquare, self).on_touch_down(touch)

class GoalColorSquare(Widget):
	color = ListProperty([1,1,1,1])
	def __init__(self, color, **kw):
		super(GoalColorSquare, self).__init__(**kw)
		self.color = color

class EmptySquare(Widget):
	color = ListProperty(EMPTY_COLOR)


class PlayerTimer(Label):
	seconds = NumericProperty(0)
	stopped = BooleanProperty(False)
	def __init__(self,**kw):
		super(PlayerTimer, self).__init__(**kw)
		Clock.schedule_interval(self.update, 1)

	def update(self, *args):
		if not self.stopped:
			self.seconds += 1

	def restart(self):
		self.seconds = 0
		self.stopped = False
		self.color = [1,1,1,1]

	def stop(self):
		self.stopped = True
		self.color = [0,1,0,1]

class PlayerBanner(Label):

	def restart(self):
		self.text = ''
	def display(self):
		self.text = 'Winner!'

class PlayerSpace(GridLayout):
	emptySquare = None
	def __init__(self, **kw):
		super(PlayerSpace, self).__init__(**kw)
		for i in range(4):
			for c in COLOR_SET:
				self.add_widget(ColorSquare(color = c))
		self.emptySquare = EmptySquare()
		self.add_widget(self.emptySquare)

#		self.shuffleSquares()

	def shuffleSquares(self):
		#Knuth shuffle of child squares
		shuffle(self.children)

	def copyBoard(self, player):
		self.clear_widgets()
		for c in player.children :
			if c == player.emptySquare :
				self.emptySquare = EmptySquare()
				self.add_widget(self.emptySquare)
			else :
				self.add_widget(ColorSquare(color = c.color))

		self.children.reverse()

	def swapIndices(self, i1, i2):
		temp = self.children[i1]
		self.children[i1] =  self.children[i2]
		self.children[i2] = temp

	def moveSquare(self, square):
		if self.myTimer.stopped :
			pass
		#if adjacent to EmptySquare
		sIndex = None
		eIndex = None
		i = 0
		for c in self.children:
			if c == self.emptySquare:
				eIndex = i
 			elif c == square:
				sIndex = i
			i += 1

		if areAdjacentIndices(sIndex,eIndex):
			self.swapIndices(sIndex,eIndex)
			if self.checkFinished(self.parent.goal):
				self.myTimer.stop()
				self.myBanner.display()

	def checkFinished(self, goal):

		for i in range(GOAL_SIZE):
			g = goal.children[i].color
			c = self.children[goalIndexToPlayerIndex(i)].color 
			if g != c:
				return False
		return True




class GoalSpace(GridLayout):
	pass
	def __init__(self, **kw):
		super(GoalSpace, self).__init__(**kw)
		self.randomGoal()

	def randomGoal(self):
		self.clear_widgets()

		colors = []
		for c in COLOR_SET:
			for i in range(4):
				colors.append(c)
		shuffle(colors)

		for i in range(GOAL_SIZE):
			self.add_widget(GoalColorSquare(color = colors.pop()))

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			if touch.is_double_tap :
				self.randomGoal()
				game = self.parent
				game.player1.shuffleSquares()
				game.player2.copyBoard(game.player1)
				game.player1timer.restart()
				game.player2timer.restart()
				game.player1banner.restart()
				game.player2banner.restart()

		return super(GoalSpace, self).on_touch_down(touch)

class ColorRaceApp(App):
	def build(self):
		pass


if __name__ == '__main__':
	ColorRaceApp().run()

