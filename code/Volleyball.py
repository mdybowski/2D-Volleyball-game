from Game import Game


def open_settings(settings_path):
    try:
        with open(settings_path, 'r') as settings:
            f_line = settings.readline().split()
            window_size = (int(f_line[1].replace(',', '')), int(f_line[2]))
            fps = int(settings.readline().split()[1])
    except IOError:
        print("Can't load settings")
        print('Opening with settings: window_size = (1200, 650); fps = 60')
        window_size = (1200, 650)
        fps = 60

    return window_size, fps


def run_game():

    window_size, fps = open_settings(Game.SETTINGS)

    game = Game(window_size, fps)

    while True:

        game.interface()

        game.step()


if __name__ == '__main__':

    run_game()
