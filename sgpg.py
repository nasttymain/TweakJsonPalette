import pygame
import pygame.locals
import time

class sgpg:
    def __init__(self) -> None:
        pygame.init()
        self.xpos = 0
        self.ypos = 0
        self.fontsize = 16
        self.colorv = [0, 0, 0]
        self.xalign = 0
        self.eventclbk = dict()
        self.pginfo = {
            "screen_xsize": 0,
            "screen_ysize": 0,
        }
        self.fontfamily = None
        self.drawlasttime = time.time_ns() // 1000000 
    def screen(self, screen_id: int, xsize: int, ysize: int, window_mode: int = 0) -> int:
        if screen_id != 0:
            return 1
        option = 0
        if (window_mode & 32) == 32:
            option += pygame.DOUBLEBUF + pygame.RESIZABLE
        self.surface = pygame.display.set_mode((xsize,ysize), option)
        self.surface.fill([255,255,255])
        self.pginfo["screen_xsize"] = self.surface.get_width()
        self.pginfo["screen_ysize"] = self.surface.get_height()
        return 0
    
    def pos(self, xposition: int, yposition: int) -> None:
        self.xpos = xposition
        self.ypos = yposition
    
    def font(self, font_name:str) -> None:
        self.fontfamily = font_name

    def text(self, message) -> None:
        for tline in str(message).splitlines():
            if self.fontfamily == None:
                t = pygame.font.SysFont(None, self.fontsize).render(tline, True, self.colorv)
            else:
                t = pygame.font.Font(self.fontfamily, self.fontsize).render(tline, True, self.colorv)
            #pygame.draw.rect(self.surface, [255,192,192], (self.xpos, self.ypos, t.get_width(), t.get_height()), 0)
            if self.xalign == 0:
                #LEFT
                self.surface.blit(t, (self.xpos, self.ypos))
            elif self.xalign == 1:
                #CENTER
                self.surface.blit(t, (self.xpos - t.get_width() / 2, self.ypos - t.get_height() / 2))
            self.ypos += t.get_height()

    def align(self, alignment_value: str = "left") -> None:
        for av in alignment_value.split():
            if av == "left":
                self.xalign = 0
            elif av == "center":
                self.xalign = 1

    def color(self, red: int, green: int, blue: int) -> None:
        self.colorv = [red, green, blue]
    def rgbcolor(self, rgb: int) -> None:
        self.colorv = [rgb // 65536, rgb % 65536 // 256, rgb % 256]

    def line(self, x1: int|float, y1: int|float, x2: int|float, y2: int|float, line_width: int = 1) -> None:
        pygame.draw.line(self.surface, self.colorv, (x1, y1), (x2, y2), line_width)

    def box(self, x1: int|float, y1: int|float, x2: int|float, y2: int|float, boxline_width: int = 1) -> None:
        pygame.draw.rect(self.surface, self.colorv, (x1, y1, x2 - x1, y2 - y1), boxline_width)

    def clear(self) -> None:
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, self.surface.get_width(), self.surface.get_height()))

    def fill(self, x1: int|float, y1: int|float, x2: int|float, y2: int|float) -> None:
        self.box(x1, y1, x2, y2, 0)

    def neweventhandler(self, event_name: str, function_pointer: callable) -> None:
        self.eventclbk[event_name] = function_pointer

    def stop(self) -> None:
        game_close = 0
        pygame.display.flip()
        while game_close == 0:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    game_close = 1
                elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #LEFT
                        if self.eventclbk.get("PG_MBUTTONDOWN") != None:
                            self.eventclbk["PG_MBUTTONDOWN"](event.pos[0], event.pos[1])
                elif event.type == pygame.locals.WINDOWRESIZED:
                    if self.eventclbk.get("PG_WINDOWRESIZED") != None:
                        self.eventclbk["PG_WINDOWRESIZED"](self.surface.get_width(), self.surface.get_height())
            if self.eventclbk.get("PG_TICK") != None:
                self.eventclbk["PG_TICK"]()
#            if (time.time_ns() // 1000000) - self.drawlasttime >= 33:
                #frame
#                self.drawlasttime = time.time_ns() // 1000000
#                pygame.display.flip()
            pygame.time.wait(10)
            pygame.display.flip()

    def title(self, title_text: str = "") -> None:
        pygame.display.set_caption(title_text)
        pass
    def redraw_now(self) -> None:
        pygame.display.flip()

    def end(self):
        pygame.quit()

