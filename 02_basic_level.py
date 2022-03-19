"""
Basic Level Platformer Game

User interaction:
Input           |   Effect
----------------|---------------------------------------
WASD/Arrow      |   Move player character
F               |   Toggle camera from following player
H               |   Toggle hitbox visibility
"""
import arcade
import random

# Window constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "02 Basic Level"

# Texture/Sprite constants
CHARACTER_SCALING = 1
TILE_SCALING = 1
CRATE_SCALING = 1.2

# Physics constants
GRAVITY = 1

# Player constants
RIGHT_FACING = 0
LEFT_FACING = 1
PLAYER_MOVEMENT_SPEED = 4
PLAYER_JUMP_SPEED = 11

# Scene layer constants
LAYER_NAME_PLAYER = "Player"

# Camera constants
CAMERA_MODE_DEFAULT = 0
CAMERA_MODE_FOLLOW = 1
CAMERA_SPEED = 0.3


class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):
        super().__init__()

        # Load idle animation textures
        self.idle_textures_left_facing = []
        self.idle_textures_right_facing = []
        for i in range(11):
            self.idle_textures_left_facing.append(arcade.load_texture(
                "assets/Pixel Adventure 1/Free/Main Characters/Mask Dude/Idle (32x32).png", 32*i, 0, 32, 32, True, hit_box_algorithm="Detailed", hit_box_detail=1))
            self.idle_textures_right_facing.append(arcade.load_texture(
                "assets/Pixel Adventure 1/Free/Main Characters/Mask Dude/Idle (32x32).png", 32*i, 0, 32, 32, hit_box_algorithm="Detailed", hit_box_detail=1))

        # Set initial texture
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.texture = self.idle_textures_right_facing[self.cur_texture]

    def update_animation(self, delta_time: float = 1 / 60):
        # Flip character left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        self.cur_texture += 1
        if self.cur_texture > 10:
            self.cur_texture = 0
        if self.character_face_direction == LEFT_FACING:
            self.texture = self.idle_textures_left_facing[self.cur_texture]
        else:
            self.texture = self.idle_textures_right_facing[self.cur_texture]

        # Calculate & set new hit box
        self.set_hit_box(
            arcade.calculate_hit_box_points_detailed(self.texture.image, 1))


class TestGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Scene & Camera
        self.scene = None
        self.camera = None
        self.camera_mode = CAMERA_MODE_DEFAULT

        # Player
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Hitbox
        self.enable_hitbox = False

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Initialize Scene & Camera
        self.scene = arcade.Scene()
        self.camera = arcade.Camera(self.width, self.height)

        # Create the Sprite lists
        self.scene.add_sprite_list(LAYER_NAME_PLAYER)
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up Player
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 16
        self.player_sprite.center_y = 64
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1500, 48):
            wall = arcade.Sprite(
                "assets/Pixel Adventure 1/Free/Terrain/Terrain (16x16).png", TILE_SCALING, 16*6, 16*8, 48, 48, 24, 24)
            wall.center_x = x+24
            wall.center_y = 24
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        crate_coordinate_list = []
        for i in range(150):
            crate_coordinate_list.append(
                [random.randrange(0, SCREEN_WIDTH+1), random.randrange(0, SCREEN_HEIGHT+1)])
        for coordinate in crate_coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                "assets/Pixel Adventure 1/Free/Items/Boxes/Box1/Idle.png", CRATE_SCALING, 0, 0, 28, 24, 14, 12
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate Camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()
        if self.enable_hitbox == True:
            self.scene.draw_hit_boxes((255, 0, 0, 255), 1)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        # Handle WASD/Arrow keys for Player movement
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        # Handle F key for Camera control
        elif key == arcade.key.F:
            if self.camera_mode == CAMERA_MODE_DEFAULT:
                self.camera_mode = CAMERA_MODE_FOLLOW
            else:
                self.camera_mode = CAMERA_MODE_DEFAULT
        # Handle H key for hitbox toggle
        elif key == arcade.key.H:
            self.enable_hitbox = not self.enable_hitbox

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Update Physics Engine
        self.physics_engine.update()

        # Update Animations
        self.scene.update_animation(
            delta_time, [LAYER_NAME_PLAYER]
        )

        # Position Camera
        if self.camera_mode == CAMERA_MODE_FOLLOW:
            self.camera_follow_player()
        else:
            self.camera.move_to(
                [0, 0], CAMERA_SPEED)

    def camera_follow_player(self):
        """Centers Camera onto Player"""
        screen_center_x = self.player_sprite.center_x - \
            (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - \
            (self.camera.viewport_height / 2)

        self.camera.move_to(
            [screen_center_x, screen_center_y], CAMERA_SPEED)


def main():
    """Main function"""
    window = TestGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
