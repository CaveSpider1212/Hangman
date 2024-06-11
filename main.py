import pygame, sys, random, asyncio

# Processes
pygame.init()
clock = pygame.time.Clock()

# Window
screen_width, screen_height = 800, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hangman")

# Colors
WHITE = (255, 255, 255)
BROWN = (150, 75, 0)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.SysFont('roboto', 40)
FONT2 = pygame.font.SysFont('roboto', 80)

# Structure
base = pygame.Rect(100, 400, 100, 10)
upright = pygame.Rect(137.5, 150, 10, 250)
beam = pygame.Rect(137.5, 150, 175, 10)
hook = pygame.Rect(305, 150, 10, 40)

# Person
head = pygame.Rect(285, 180, 50, 50)
body = pygame.Rect(307.5, 230, 5, 80)
left_arm = pygame.Rect(270, 250, 40, 5)
right_arm = pygame.Rect(310, 250, 40, 5)

# Button/letter grid setup
button_size = 50
gap = 10
letters = []
A = 65
for i in range(26):
    x = 10 + (button_size + gap) * (i % 13)
    if i < 13:
        y = 500
    else:
        y = 560
    letters.append([x, y, chr(A + i), True])

# Main program
async def main():
    # Chooses the word
    wordlist = ["trophy", "basket", "library", "monitor", "computer", "mailbox", "headset", "develop", "charge", "keyboard"]
    word = random.choice(wordlist).upper()

    # Game variables
    status = 0
    guessed = []

    while True:
        # Processes
        pygame.display.update()
        clock.tick(60)
        
        # Setting display and structure
        screen.fill(WHITE)
        pygame.draw.rect(screen, BROWN, base)
        pygame.draw.rect(screen, BROWN, upright)
        pygame.draw.rect(screen, BROWN, beam)
        pygame.draw.rect(screen, BROWN, hook)

        # Draws word
        clue = ""
        for letter in word:
            if letter in guessed:
                clue += letter + " "
            else:
                clue += "_ "
        text = FONT2.render(clue, 1, BLACK)
        screen.blit(text, (375, 200))

        # Checks if word has been found
        word_withspaces = ""
        for letter in word:
            word_withspaces += letter + " "
        if clue == word_withspaces: # Win message
            won_message = FONT.render("You won!", 1, GREEN)
            screen.blit(won_message, (350, 75))

        # Draws buttons with letters
        for letter in letters:
            x, y, ltr, visible = letter
            if visible:
                button = pygame.Rect(x, y, button_size, button_size)
                pygame.draw.rect(screen, BLACK, button, width = 2)
                text = FONT.render(ltr, 1, BLACK)
                screen.blit(text, (x + 15, y + 10))

        # Drawing body
        for i in range(status + 1):
            if i == 1:
                pygame.draw.ellipse(screen, BLACK, head)
            if i == 2:
                pygame.draw.rect(screen, BLACK, body)
            if i == 3:
                pygame.draw.rect(screen, BLACK, left_arm)
            if i == 4:
                pygame.draw.rect(screen, BLACK, right_arm)
            if i == 5: # left leg
                pygame.draw.line(screen, BLACK, (310, 307.5), (270, 350), width = 7)
            if i == 6: # right leg, loss message
                pygame.draw.line(screen, BLACK, (310, 307.5), (350, 350), width = 7)
                loss_message = FONT.render(f"You lost. The word was {word}.", 1, RED)
                screen.blit(loss_message, (200, 75))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        if mouse_x > x and mouse_x < x + button_size and mouse_y > y and mouse_y < y + button_size:
                            letter[3] = False
                            if ltr in word:
                                guessed.append(ltr)
                            else:
                                status += 1
        
        await asyncio.sleep(0)

asyncio.run(main())