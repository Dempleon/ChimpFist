import os
import pygame
from pygame.compat import geterror

import Chimp
import Fist

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

screen = pygame.display.set_mode((1920, 140))

# functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image')
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


def update_score(score_value, misses_value):
    text = pygame.font.SysFont('impact', 36)
    score = text.render('Money: $' + str(score_value), True, (10, 10, 10))
    misses = text.render('Misses: ' + str(misses_value), True, (10, 10, 10))
    screen.blit(score, (20, 20))
    screen.blit(misses, (20, 60))


def main():
    """This function is called when the program starts.
    It initializes everything it needs, then runs in a
    loop until the function returns"""
    # Initialize Everything
    pygame.init()
    pygame.display.set_caption('Chimp Fist')
    pygame.mouse.set_visible(False)

    # Create the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Put Text on the background, centered
    if pygame.font:
        font = pygame.font.SysFont('impact', 30)
        text = font.render('Pummel The Chimp And Win Money! Miss And Lose Money', True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        background.blit(text, textpos)

    # Display the background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare game objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    chimp = Chimp.Chimp()
    fist = Fist.Fist()
    allsprites = pygame.sprite.RenderPlain((fist, chimp))
    money = 0
    misses = 0

    # Main loop
    running = True
    while running:
        clock.tick(60)

        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()
                    chimp.punched()
                    money += 1
                else:
                    whiff_sound.play()
                    misses += 1
                    money -= 1
                    if money < 0:
                        money = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        # Draw everything

        screen.blit(background, (0, 0))
        update_score(money, misses)
        allsprites.draw(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
