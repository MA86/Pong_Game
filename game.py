import sdl2
import ctypes


class Game(object):
    def __init__(self):
        self.window = None
        self.renderer = None
        self.running = True
        self.thick = 15

    # Public methods:

    def initialize(self) -> bool:
        # Initialize graphics subsystem
        result = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        if result != 0:
            sdl2.SDL_Log("Graphics initialization failed: ",
                         sdl2.SDL_GetError())
            return False

        # Create window
        self.window = sdl2.SDL_CreateWindow(b"Pong",
                                            sdl2.SDL_WINDOWPOS_CENTERED,
                                            sdl2.SDL_WINDOWPOS_CENTERED, 1024, 768, 0)
        if self.window == None:
            sdl2.SDL_Log("Window failed: ", sdl2.SDL_GetError())
            return False

        # Create renderer
        self.renderer = sdl2.SDL_CreateRenderer(self.window,
                                                -1,
                                                sdl2.SDL_RENDERER_ACCELERATED |
                                                sdl2.SDL_RENDERER_PRESENTVSYNC)
        if self.renderer == None:
            sdl2.SDL_Log("Renderer failed: ", sdl2.SDL_GetError())
            return False

        return True

    def run_loop(self) -> None:
        while self.running:
            self._process_input()
            self._process_update()
            self._process_output()

    def shutdown(self) -> None:
        # Shutdown in reverse
        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()

    # Helper methods:

    def _process_input(self) -> None:
        event = sdl2.SDL_Event()
        # Process events-queue
        while sdl2.SDL_PollEvent(event):
            if event.type == sdl2.SDL_QUIT:
                self.running = False

        # Process keyboard state
        keyb_state = sdl2.SDL_GetKeyboardState(None)
        if keyb_state[sdl2.SDL_SCANCODE_ESCAPE]:
            self.running = False

    def _process_update(self) -> None:
        pass

    def _process_output(self) -> None:
        # Clear color-buffer to blue
        sdl2.SDL_SetRenderDrawColor(self.renderer, 105, 105, 105, 255)
        sdl2.SDL_RenderClear(self.renderer)

        # Draw scene to color-buffer:
        sdl2.SDL_SetRenderDrawColor(self.renderer, 192, 192, 192, 255)  # Color
        top_wall = sdl2.SDL_Rect(0, 0, 1024, self.thick)    # Shapes
        bot_wall = sdl2.SDL_Rect(0, 768-self.thick, 1024, self.thick)
        right_wall = sdl2.SDL_Rect(1024-self.thick, 0, self.thick, 1024)
        sdl2.SDL_RenderFillRect(self.renderer, top_wall)    # Draws
        sdl2.SDL_RenderFillRect(self.renderer, bot_wall)
        sdl2.SDL_RenderFillRect(self.renderer, right_wall)

        # Swap color-buffer to update screen
        sdl2.SDL_RenderPresent(self.renderer)
