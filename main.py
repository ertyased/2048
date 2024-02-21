import neat
from game2048 import Game2048, Move
import pygame
from pygame.locals import *
from time import sleep


def fitness_func(genomes, configuration):
    global font
    games = []
    networks = []
    moves = [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]
    for genome_id, genome in genomes:
        genome.fitness = 4.0
        game = Game2048()
        game.start()
        games.append(game)
        networks.append(neat.nn.FeedForwardNetwork.create(genome, config))

    while not all(map(lambda x: x.is_ended(), games)):
        maxim = [-1, -1]
        for i in range(len(games)):
            game = games[i]
            if game.is_ended():
                continue
            network = networks[i]
            result = network.activate(game.get_field_as_array())
            make_move = max(enumerate(result), key=lambda x: x[1])[0]
            game.move(moves[make_move])
            if maxim[1] < game.get_score():
                maxim[0] = i
                maxim[1] = game.get_score()
    maxim = [-1, -1]
    for i in range(len(games)):
        game = games[i]
        if maxim[1] < game.get_score():
            maxim[0] = i
            maxim[1] = game.get_score()
    draw_game2048(games[maxim[0]], font)
    print(maxim[1])

    for i in range(len(games)):
        game = games[i]
        genome = genomes[i][1]
        genome.fitness = game.get_score()


def draw_game2048(_game: Game2048, _font: pygame.font.SysFont):
    global width, height
    field = _game.get_field()
    screen.fill((255, 255, 255))
    for i in range(4):
        for j in range(4):
            lu_corner = [width // 4 * i, height // 4 * j]
            text = _font.render(str(field[i][j]), True, (0, 0, 0))
            screen.blit(text, (lu_corner[0] + width // 8 + text.get_height() // 2, lu_corner[1] + height // 8 +
                               text.get_width() // 2))
    pygame.display.update()
    pygame.display.flip()


if __name__ == "__main__":
    width = 720
    height = 720
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 60)

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'neat-config')
    pop = neat.population.Population(config)
    pop.run(fitness_function=fitness_func)

    pygame.quit()