import gui
import model

height = 60
width = 100
kaart = "schelde2.png"

model = model.Model(height, width)
window = gui.Window(height, width, kaart, model=model)
window.mainloop()