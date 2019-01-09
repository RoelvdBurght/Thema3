import tkinter as tk
import model
import numpy as np

class Window(tk.Frame):
	"""
		Input: model_height and model_width define the number of gridpoints
			   model should be a model object filled with points
	"""
	def __init__(self, model_height, model_width, kaart, model=None, root=None):
		tk.Frame.__init__(self, root)
		self.grid()
		self.model = model
		self.picture = tk.PhotoImage(file=kaart)
		self.canvas_height = self.picture.height()
		self.canvas_width = self.picture.width()
		self.stored_up = None
		self.stored_down = None
		self.stored_right = None
		self.stored_left = None
		self.stored_self = None

		# Display image as canvas widget
		self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
		self.canvas.create_image(0,0, anchor=tk.NW, image=self.picture)
		self.canvas.bind('<Button-1>', self.grid_listener)
		self.canvas.grid(row=0, column=0)

		# Create the input forms frame and reset button
		self.uplabel = tk.Label(root, text="P up")
		self.uplabel.grid(row=1,column=0)
		self.upinput = tk.Entry(root)
		self.upinput.grid(row=1, column=1)

		self.downlabel = tk.Label(root, text="P down")
		self.downlabel.grid(row=2,column=0)
		self.downinput = tk.Entry(root)
		self.downinput.grid(row=2, column=1)
		
		self.rightlabel = tk.Label(root, text="P right")
		self.rightlabel.grid(row=3,column=0)
		self.rightinput = tk.Entry(root)
		self.rightinput.grid(row=3, column=1)

		self.leftlabel = tk.Label(root, text="P left")
		self.leftlabel.grid(row=4,column=0)
		self.leftinput = tk.Entry(root)
		self.leftinput.grid(row=4, column=1)

		self.selflabel = tk.Label(root, text="P self")
		self.selflabel.grid(row=5,column=0)
		self.selfinput = tk.Entry(root)
		self.selfinput.grid(row=5, column=1)		

		self.reset = tk.Button(root, command=self.reset_listener, height=25, width=25,
								text="reset values")
		self.reset.grid(row=0, column=1)

		# Create save entry and button and entry label etc
		self.save_button = tk.Button(root, text="Save transition states",
											command=model.save_transition_chances,
											width=25, height=25)
		self.save_button.grid(row=0, column=2)

		# filename buttons etc
		self.filenamelabel = tk.Label(root, text="Filename")
		self.filenamelabel.grid(row=6,column=0)
		self.filenameinput = tk.Entry(root)
		self.filenameinput.grid(row=6, column=1)

		# Create gridlines
		self.spacing_x = np.linspace(0, self.canvas_width, model_width+1)
		self.spacing_y = np.linspace(0, self.canvas_height, model_height+1)
		for x in self.spacing_x:
			self.canvas.create_line(x, 0, x, self.canvas_height, fill="black")
		for y in self.spacing_y:
			self.canvas.create_line(0, y, self.canvas_width, y, fill="black")

	def grid_listener(self, event):
		# Translate picture coordinates to grid/model coordinates
		# and updates the transition chances in the clicked point
		x_grid = 0
		y_grid = 0
		for counter, x in enumerate(self.spacing_x):
			if x <= event.x:
				x_grid = counter
		for counter, y in enumerate(self.spacing_y):
			if y <= event.y:
				y_grid = counter
		self.model.set_chances(x_grid, y_grid, self.stored_up,
											 self.stored_down,
											 self.stored_right,
											 self.stored_left,
											 self.stored_self)
	
	# Sets the stored values to the ones currently in the entryboxes
	def reset_listener(self):
		self.stored_up = self.upinput.get()
		self.stored_down = self.downinput.get()
		self.stored_right = self.rightinput.get()
		self.stored_left = self.leftinput.get()
		self.stored_self = self.selfinput.get()
		model.filename = self.filenameinput.get()



# height = 25
# width = 25

# model = model.Model(height, width)
# model.read_transition_states('test')
# print(model.grid[0][0].p_up)
# window = Window(height, width, model=model)
# window.mainloop()