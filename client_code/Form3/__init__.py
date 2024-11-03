from ._anvil_designer import Form3Template
from anvil import *
import anvil.image
import json

class Form3(Form3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.selected_tile_x = None
        self.selected_tile_y = None
        self.draw_positions = {}
        self.is_drawing = False

    def canvas_1_show(self, **event_args):
        # loaded image is 192x600
        self.image = URLMedia('_/theme/TileEditorSpritesheet.2x_2.png')
        self.draw_canvas_1()

    def draw_canvas_1(self, x=None, y=None):
        canvas = self.canvas_1
        canvas.clear_rect(0, 0, canvas.get_width(), canvas.get_height())

        # loaded image is 192x600
        canvas.draw_image(self.image, 0, 0, 192, 600)
        
        # HIGHLIGHT CELL
        if x is not None and y is not None:
            canvas.stroke_style = "cyan"
            canvas.line_width = 3
            self.selected_tile_x = (x // 32) * 32
            self.selected_tile_y = (y // 32) * 32
            canvas.stroke_rect(self.selected_tile_x, self.selected_tile_y, 32, 32)
            
    def canvas_1_mouse_down(self, x, y, button, keys, **event_args):
        self.label_1.text = f"SELECTOR: {x}, {y}"
        self.draw_canvas_1(x, y)

    def draw_canvas_2(self):
        canvas = self.canvas_2
        canvas.clear_rect(0, 0, canvas.get_width(), canvas.get_height())

        # Draw all stored positions
        for pos in self.draw_positions.values():
            canvas.draw_image_part(
                self.image,
                pos['tile_x'], pos['tile_y'],
                32, 32,
                pos['canvas_x'], pos['canvas_y'],
                32, 32
            )

    def canvas_2_mouse_down(self, x, y, button, keys, **event_args):
        self.label_2.text = f"SELECTOR 2: {x}, {y}"
        self.is_drawing = True
        self.draw_tile(x, y)

    def draw_tile(self, x, y):
        if self.selected_tile_x is not None and self.selected_tile_y is not None:
            position_x = (x // 32) * 32
            position_y = (y // 32) * 32
            cell_key = f"{position_x},{position_y}"

            # Update the cell with the new tile
            self.draw_positions[cell_key] = {
                'tile_x': self.selected_tile_x,
                'tile_y': self.selected_tile_y,
                'canvas_x': position_x,
                'canvas_y': position_y
            }
            self.draw_canvas_2()

    def canvas_2_mouse_up(self, x, y, button, **event_args):
        self.is_drawing = False

    def canvas_2_mouse_move(self, x, y, **event_args):
        if self.is_drawing:
            self.draw_tile(x, y)

    def primary_color_1_click(self, **event_args):
        print(self.draw_positions)
        self.label_3.text = json.dumps(self.draw_positions)

    def primary_color_2_click(self, **event_args):
        canvas = self.canvas_2
        canvas.clear_rect(0, 0, canvas.get_width(), canvas.get_height())
        self.draw_positions = {}

    def primary_color_2_copy_click(self, **event_args):
        self.draw_positions = json.loads(self.text_area_1.text)
        # Convert string keys back to tuple keys
        self.draw_positions = {tuple(map(float, k.split(','))): v for k, v in self.draw_positions.items()}
        self.draw_canvas_2()
