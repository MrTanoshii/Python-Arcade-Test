"""
Basic Window

User interaction:
Input           |   Effect
----------------|------------------------------------------------------------
1-3             |   Resize & center window
Left click      |   Set random window background color
Scroll          |   Increase/Decrease red channel of window background color
"""
import arcade
import random

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "01 Basic Window"


class TestGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        background_color = [random.randrange(0, 256), random.randrange(
            0, 256), random.randrange(0, 256)]
        arcade.set_background_color(background_color)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here

    def on_key_press(self, key, modifiers):
        """Handle key press."""
        current_window = arcade.get_window()
        if key == arcade.key.KEY_1:
            arcade.Window.set_size(current_window, 400, 400)
        elif key == arcade.key.KEY_2:
            arcade.Window.set_size(current_window, 1280, 720)
        elif key == arcade.key.KEY_3:
            arcade.Window.set_size(current_window, 1920, 1080)
        arcade.Window.center_window(current_window)

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse press."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            new_color = [random.randrange(0, 256), random.randrange(
                0, 256), random.randrange(0, 256)]
            print(new_color)
            self.background_color = new_color
            arcade.set_background_color(self.background_color)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            arcade.exit()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """Handle mouse scroll."""
        print(x, y, scroll_x, scroll_y, self.background_color)
        if (self.background_color[0] + scroll_y >= 0) and (self.background_color[0] + scroll_y <= 255):
            self.background_color[0] = self.background_color[0] + scroll_y
            arcade.set_background_color(self.background_color)


def main():
    """Main function"""
    window = TestGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
