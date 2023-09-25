import pygame, datetime
pygame.init()
screen = pygame.display.set_mode((512, 128))
clock = pygame.time.Clock()

counter, text = 10, '10'.rjust(3)
# pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)

def time_to_str(time_delta):
    # 表示したい形式に変換（小数点第２位までに変換）
    mm, ss = divmod(time_delta.seconds, 60)
    hh, mm = divmod(mm, 60)
    if 0 < hh:
        raise Exception("時間がオーバーしました")
    s = "%02d:%02d" % (mm, ss)
    if time_delta.days:
        def plural(n):
            return n, abs(n) != 1 and "s" or ""
        s = ("%d day%s, " % plural(time_delta.days)) + s
    if time_delta.microseconds:
        s = s + ".%03d" % (time_delta.microseconds / 1000)
    return s

start_time = datetime.datetime.now()

run = True
while run:
    for e in pygame.event.get():
        # if e.type == pygame.USEREVENT:
        #     counter -= 1
        #     text = str(counter).rjust(3) if counter > 0 else 'boom!'
            # text = str(clock.get_time())
            # pygame.time.set_timer(pygame.USEREVENT)
            # print(pygame.time.get_ticks())
        if e.type == pygame.QUIT: 
            run = False
    text = time_to_str(datetime.datetime.now() - start_time)
    screen.fill((255, 255, 255))
    screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
    pygame.display.flip()
    # clock.tick(60)
