import pygame
import random

pygame.init()

# Screen settings
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battle with Ghosts by Cyberchain")

# Fps
fps = 60
clock = pygame.time.Clock()


# Class game
class Game:
    def __init__(self, our_player, ours_ghosts):
        self.score = 0
        self.round_number = 0

        # Slow down cycle
        self.round_time = 0
        self.slow_down_cycle = 0

        # Player/Ghosts
        self.our_player = our_player
        self.ours_ghosts = ours_ghosts

        # Fonts
        self.title_font = pygame.font.Font("fonts/cartoon.ttf", 64)
        self.game_font = pygame.font.Font("fonts/cartoon.ttf", 30)

        # Background Picture
        self.bg_image = pygame.image.load("img/bg_image.jpg")
        self.bg_image_rect = self.bg_image.get_rect()
        self.bg_image_rect.topleft = (0, 0)

        # Pictures a ghosts
        white_ghost = pygame.image.load("img/ghost_white.png")
        blue_ghost = pygame.image.load("img/ghost_blue.png")
        green_ghost = pygame.image.load("img/ghost_green.png")
        red_ghost = pygame.image.load("img/ghost_red.png")
        purple_ghost = pygame.image.load("img/ghost_purple.png")
        self.ghosts_images = [white_ghost, blue_ghost, green_ghost, red_ghost, purple_ghost]

        # Generating ghost to catch in the top row
        self.ghost_catch_type = random.randint(0, 4)
        self.ghost_catch_image = self.ghosts_images[self.ghost_catch_type]

        # Rendering ghost
        self.ghost_catch_image_rect = self.ghost_catch_image.get_rect()
        self.ghost_catch_image_rect.centerx = width//2
        self.ghost_catch_image_rect.top = 35

        # Title Music
        pygame.mixer.music.load("media/music.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1, 0)

    # Slow down cycle
    def update(self):
        self.slow_down_cycle += 1
        if self.slow_down_cycle == fps:
            self.round_time += 1
            self.slow_down_cycle = 0

        self.check_collisions()

    # Rendering game
    def draw(self):
        dark_yellow = pygame.Color("#faf741")
        white = (240, 245, 241)
        blue = (44, 84, 171)
        green = (50, 168, 82)
        red = (163, 23, 28)
        purple = (129, 48, 191)
        colors = [white, blue, green, red, purple]

        # Catch text
        catch_text = self.game_font.render("Catch this ghost", True, dark_yellow)
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.centerx = width//2
        catch_text_rect.top = 5

        # Score text
        score_text = self.game_font.render(f"Score: {self.score}", True, dark_yellow)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (15, 3)

        # Lives text
        lives_text = self.game_font.render(f"Lives: {self.our_player.lives}", True, dark_yellow)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (15, 33)

        # Round text
        round_text = self.game_font.render(f"Round: {self.round_number}", True, dark_yellow)
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (15, 60)

        # Round time text
        time_text = self.game_font.render(f"Round Time: {self.round_time}", True, dark_yellow)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (980, 15)

        # Safe zone text
        safezone_text = self.game_font.render(f"Safe Zone: {self.our_player.enter_safezone}", True, dark_yellow)
        safezone_text_rect = safezone_text.get_rect()
        safezone_text_rect.topright = (980, 45)

        # Blit text
        screen.blit(catch_text, catch_text_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(lives_text, lives_text_rect)
        screen.blit(round_text, round_text_rect)
        screen.blit(time_text, time_text_rect)
        screen.blit(safezone_text, safezone_text_rect)

        # Blit ghost - catch
        screen.blit(self.ghost_catch_image, self.ghost_catch_image_rect)

        # Shape frame
        pygame.draw.rect(screen, colors[self.ghost_catch_type], (0, 100, width, height - 172), 4)

    # Check collisions between wizard and ghosts
    def check_collisions(self):
        collided_ghost = pygame.sprite.spritecollideany(self.our_player, self.ours_ghosts)
        if collided_ghost:
            if collided_ghost.type == self.ghost_catch_type:
                self.our_player.catch_sound.play()
                self.score += 10 * self.round_number
                collided_ghost.remove(self.ours_ghosts)
                if self.ours_ghosts:
                   self.choose_new_target()
                else:
                   self.our_player.reset()
                   self.start_new_round()
            else:
                self.our_player.wrong_sound.play()
                self.our_player.lives -= 1
                if self.our_player.lives <= 0:
                    pygame.mixer.music.stop()
                    self.our_player.gameover_sound.play()
                    self.pause_game(f"Your Score: {self.score}", "Game Over", "Press Enter, if you want play again.")
                    self.reset_game()
                self.our_player.reset()

    # Start new round with more ghosts and time bonus
    def start_new_round(self):
        self.score += int(10 * (self.round_number / (1 + self.round_time)))

        # Default values
        self.round_time = 0
        self.slow_down_cycle = 0
        self.round_number += 1
        self.our_player.enter_safezone += 1

        # Remove old ghosts group and New ghosts group
        for deleted_ghosts in self.ours_ghosts:
            self.ours_ghosts.remove(deleted_ghosts)

        # Add ghosts - index
        for i in range(self.round_number):
            self.ours_ghosts.add(Ghost(random.randint(0, width - 72), random.randint(100, height - 172),
            self.ghosts_images[0], 0))

            self.ours_ghosts.add(Ghost(random.randint(0, width - 72), random.randint(100, height - 172),
            self.ghosts_images[1], 1))

            self.ours_ghosts.add(Ghost(random.randint(0, width - 72), random.randint(100, height - 172),
            self.ghosts_images[2], 2))

            self.ours_ghosts.add(Ghost(random.randint(0, width - 72), random.randint(100, height - 172),
            self.ghosts_images[3], 3))

            self.ours_ghosts.add(Ghost(random.randint(0, width - 72), random.randint(100, height - 172),
            self.ghosts_images[4], 4))

            # Choose new ghost
            self.choose_new_target()

    # Choose new ghost with new color
    def choose_new_target(self):
        new_ghost_catch = random.choice(self.ours_ghosts.sprites())
        # New index ghost
        self.ghost_catch_type = new_ghost_catch.type
        self.ghost_catch_image = new_ghost_catch.image

    # Pause game/Start new game
    def pause_game(self, main_text, score_text, sub_text):

        # Global scope
        global lets_continue

        # Color text
        dark_yellow = pygame.Color("#c9c608")
        black = (0, 0, 0)

        # Start Text
        main_text_create = self.game_font.render(main_text, True, dark_yellow)
        main_text_create_rect = main_text_create.get_rect()
        main_text_create_rect.center = (width//2, height//2 - 45)

        score_text_create = self.title_font.render(score_text, True, dark_yellow)
        score_text_create_rect = score_text_create.get_rect()
        score_text_create_rect.center = (width//2, height//2)

        sub_text_create = self.game_font.render(sub_text, True, dark_yellow)
        sub_text_create_rect = sub_text_create.get_rect()
        sub_text_create_rect.center = (width//2, height//2 + 60)

        # Fill background
        screen.fill(black)

        # Blit text
        screen.blit(main_text_create, main_text_create_rect)
        screen.blit(score_text_create, score_text_create_rect)
        screen.blit(sub_text_create, sub_text_create_rect)

        pygame.display.update()

        # Paused game
        paused = True
        while paused:
            for one_event in pygame.event.get():
                if one_event.type == pygame.KEYDOWN:
                    if one_event.key == pygame.K_RETURN:
                        paused = False
                if one_event.type == pygame.QUIT:
                    paused = False
                    # Global scope
                    lets_continue = False

    # Gameover - Reset game to default
    def reset_game(self):
        self.score = 0
        self.round_number = 0

        self.our_player.lives = 5
        self.our_player.enter_safezone = 2
        self.start_new_round()

        pygame.mixer.music.play(-1, 0)


# Class Player - inheritance
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Inheritance
        super().__init__()

        # Picture wizard
        self.image = pygame.image.load("img/wizard.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width//2
        self.rect.bottom = height

        self.lives = 5
        self.enter_safezone = 2
        self.speed = 5

        # Game sound
        self.catch_sound = pygame.mixer.Sound("media/catch.wav")
        self.catch_sound.set_volume(0.1)
        self.wrong_sound = pygame.mixer.Sound("media/wrong.wav")
        self.wrong_sound.set_volume(0.1)
        self.gameover_sound = pygame.mixer.Sound("media/gameover.wav")
        self.gameover_sound.set_volume(0.3)

    # Move wizard
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < height - 100:
            self.rect.y += self.speed

    # Safe Zone
    def back_to_safezone(self):
        if self.enter_safezone > 0:
            self.enter_safezone -= 1
            self.rect.bottom = height

    # Reset wizard to safe zone
    def reset(self):
        self.rect.centerx = width//2
        self.rect.bottom = height


# Class Ghost - inheritance
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, image, ghosts_type):
        # Inheritance
        super().__init__()

        # Load image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.type = ghosts_type

        self.axis_x = random.choice([-1, 1])
        self.axis_y = random.choice([-1, 1])
        self.speed = random.randint(1, 2)

    # Speed ghost
    def update(self):
        self.rect.x += self.axis_x * self.speed
        self.rect.y += self.axis_y * self.speed

        # Bounce ghost
        if self.rect.left < 0 or self.rect.right > width:
            self.axis_x = -1 * self.axis_x
        if self.rect.top < 100 or self.rect.bottom > height - 100:
            self.axis_y = -1 * self.axis_y


ghosts_group = pygame.sprite.Group()

# Player group
player_group = pygame.sprite.Group()
one_player = Player()
player_group.add(one_player)

# Object Game
my_game = Game(one_player, ghosts_group)
my_game.pause_game("Welcome in", "Battle with Ghosts", "Press Enter, if you want play.")
my_game.start_new_round()

# Main Cycle
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                one_player.back_to_safezone()

    # Fill background
    screen.blit(my_game.bg_image, my_game.bg_image_rect)

    # Update
    ghosts_group.draw(screen)
    ghosts_group.update()

    player_group.draw(screen)
    player_group.update()

    my_game.update()
    my_game.draw()

    pygame.display.update()

    # Cycle Slowdown
    clock.tick(fps)

pygame.quit()


