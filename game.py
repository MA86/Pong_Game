import sdl2
from vector2d import *


class Game(object):
    def __init__(self):
        self._window = None
        self._renderer = None
        self._running = True
        self._time_then = 0.0

        # Variables for scene
        self._thick = 15
        self._paddle_pos = Vector2(10.0, 768.0/2.0)
        self._ball_pos = Vector2(1024.0/2.0, 768.0/2.0)
        self._paddle_h = 100.0

        # Variables for movement
        self._paddle_dir = 0

    # These are public methods:

    def initialize(self) -> bool:
        # Initialize graphics subsystem
        result = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        if result != 0:
            sdl2.SDL_Log("Graphics initialization failed: ",
                         sdl2.SDL_GetError())
            return False

        # Create window
        self._window = sdl2.SDL_CreateWindow(b"Pong",
                                             sdl2.SDL_WINDOWPOS_CENTERED,
                                             sdl2.SDL_WINDOWPOS_CENTERED, 1024, 768, 0)
        if self._window == None:
            sdl2.SDL_Log("Window failed: ", sdl2.SDL_GetError())
            return False

        # Create renderer
        self._renderer = sdl2.SDL_CreateRenderer(self._window,
                                                 -1,
                                                 sdl2.SDL_RENDERER_ACCELERATED |
                                                 sdl2.SDL_RENDERER_PRESENTVSYNC)
        if self._renderer == None:
            sdl2.SDL_Log("Renderer failed: ", sdl2.SDL_GetError())
            return False

        return True

    def run_loop(self) -> None:
        while self._running:
            self._process_input()
            self._process_update()
            self._process_output()

    def shutdown(self) -> None:
        # Shutdown in reverse
        sdl2.SDL_DestroyRenderer(self._renderer)
        sdl2.SDL_DestroyWindow(self._window)
        sdl2.SDL_Quit()

    # These are helper methods:

    def _process_input(self) -> None:
        event = sdl2.SDL_Event()
        # Process events-queue
        while sdl2.SDL_PollEvent(event):
            if event.type == sdl2.SDL_QUIT:
                self._running = False

        # Process keyboard state
        keyb_state = sdl2.SDL_GetKeyboardState(None)
        if keyb_state[sdl2.SDL_SCANCODE_ESCAPE]:
            self._running = False

        # Update paddlie direction based on W/S keys
        self._paddle_dir = 0
        if keyb_state[sdl2.SDL_SCANCODE_W]:
            self._paddle_dir -= 1
        if keyb_state[sdl2.SDL_SCANCODE_S]:
            self._paddle_dir += 1

    def _process_update(self) -> None:
        # Wait 16ms (for frame limiting)
        sdl2.SDL_Delay(16)

        time_now = sdl2.SDL_GetTicks()
        delta_time = (time_now - self._time_then) / 1000.0

        # Clamp max delta time (for debugging)
        if delta_time > 0.05:
            delta_time = 0.05

        # Time now is time then
        self._time_then = sdl2.SDL_GetTicks()

        # Update paddle pos based on direction
        if self._paddle_dir != 0:
            self._paddle_pos.y += self._paddle_dir * 300.0 * delta_time
            # Clip paddle to screen
            if self._paddle_pos.y < (self._paddle_h/2.0 + self._thick):
                self._paddle_pos.y = self._paddle_h/2.0 + self._thick
            elif self._paddle_pos.y > (768.0 - self._paddle_h/2.0 - self._thick):
                self._paddle_pos.y = 768.0 - self._paddle_h/2.0 - self._thick

        # TODO: ball...

    def _process_output(self) -> None:
        # Clear color-buffer to blue
        sdl2.SDL_SetRenderDrawColor(self._renderer, 105, 105, 105, 255)
        sdl2.SDL_RenderClear(self._renderer)

        # Draw scene to color-buffer:
        sdl2.SDL_SetRenderDrawColor(
            self._renderer, 192, 192, 192, 255)              # Color
        top_wall = sdl2.SDL_Rect(0, 0, 1024, self._thick)    # Shapes
        bot_wall = sdl2.SDL_Rect(0, 768-self._thick, 1024, self._thick)
        right_wall = sdl2.SDL_Rect(1024-self._thick, 0, self._thick, 1024)
        paddle = sdl2.SDL_Rect(int(self._paddle_pos.x),
                               int(self._paddle_pos.y-self._paddle_h/2),
                               int(self._thick),
                               int(self._paddle_h))
        ball = sdl2.SDL_Rect(int(self._ball_pos.x-self._thick/2),
                             int(self._ball_pos.y-self._thick/2),
                             int(self._thick),
                             int(self._thick))
        sdl2.SDL_RenderFillRect(self._renderer, top_wall)    # Draws
        sdl2.SDL_RenderFillRect(self._renderer, bot_wall)
        sdl2.SDL_RenderFillRect(self._renderer, right_wall)
        sdl2.SDL_RenderFillRect(self._renderer, paddle)
        sdl2.SDL_RenderFillRect(self._renderer, ball)

        # Swap color-buffer to update screen
        sdl2.SDL_RenderPresent(self._renderer)
