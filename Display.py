"""test display"""
import datetime
import pygame  # pylint: disable=E0401


pygame.init()  # pylint: disable=E1101
screen = pygame.display.set_mode((512, 128))
clock = pygame.time.Clock()

counter, text = 10, '10'.rjust(3)
# pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)


def time_to_str(time_delta):
    """timedalta to str."""
    # 表示したい形式に変換（小数点第２位までに変換）
    minutes, seconds = divmod(time_delta.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if 0 < hours:
        raise OverflowError("時間がオーバーしました")
    result_str = f"{minutes:02d}:{seconds:02d}"
    if time_delta.microseconds != 0:
        microseconds = int(time_delta.microseconds/1000)
        result_str = result_str + f".{microseconds:03d}"
    return result_str


start_time = datetime.datetime.now()

RUN = True
while RUN:
    for e in pygame.event.get():
        # if e.type == pygame.USEREVENT:
        #     counter -= 1
        #     text = str(counter).rjust(3) if counter > 0 else 'boom!'
        # text = str(clock.get_time())
        # pygame.time.set_timer(pygame.USEREVENT)
        # print(pygame.time.get_ticks())
        if e.type == pygame.QUIT:  # pylint: disable=E1101
            RUN = False
    text = time_to_str(datetime.datetime.now() - start_time)
    screen.fill((255, 255, 255))
    screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
    pygame.display.flip()
    # clock.tick(60)
