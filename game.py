import sdl2
import ctypes


class Game(object):
    def __init__(self):
        self.window = None
        self.running = True

    # Public methods

    def initialize(self) -> bool:
        # Initialize video subsystem
        result = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        if result != 0:
            sdl2.SDL_Log("Initialization failed: ", sdl2.SDL_GetError())
            return False

        # Create window
        self.window = sdl2.SDL_CreateWindow(b"Pong",
                                            sdl2.SDL_WINDOWPOS_CENTERED,
                                            sdl2.SDL_WINDOWPOS_CENTERED, 1024, 768, 0)
        if self.window == None:
            sdl2.SDL_Log("Window failed: ", sdl2.SDL_GetError())
            return False
        return True

    def run_loop(self) -> None:
        while self.running:
            self._process_input()
            self._process_update()
            self._process_output()

    def shutdown(self) -> None:
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()

    # Helper methods

    def _process_input(self) -> None:
        event = sdl2.SDL_Event()
        # Process pending events in events-queue
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
        pass
