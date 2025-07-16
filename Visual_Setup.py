import pygame
import random

#------------------Screen Logistics-------------------#
Screen_width = 800
Screen_height = 600


def initialize_screen():
    screen = pygame.display.set_mode((Screen_width, Screen_height))
    pygame.display.set_caption("My Game")
    return screen



#------------------Background Object------------------#

class Background:
    def __init__(self, background_image, width=1300, height=800):
        original = pygame.image.load(background_image).convert()
        scaled = pygame.transform.scale(original, (width, height))

        self.bg_image_1 = scaled
        self.bg_image_2 = pygame.transform.flip(scaled, True, False)  # Horizontal flip

        self.width = width
        self.height = height
        self.x = 0
        self.mirror_next = False  # Flip logic flag

    def update(self, speed):
        
        self.x -= speed
        if self.x <= -self.width:
            self.x = 0
            self.mirror_next = not self.mirror_next  # Toggle flip state

    def draw(self, screen):
        if self.mirror_next:
            screen.blit(self.bg_image_2, (self.x, 0))
            screen.blit(self.bg_image_1, (self.x + self.width, 0))
        else:
            screen.blit(self.bg_image_1, (self.x, 0))
            screen.blit(self.bg_image_2, (self.x + self.width, 0))


#-----------------Dinosaur Character------------------#

class Dino_Character(pygame.sprite.Sprite):

        def __init__(self, x, y, image, scale=(400, 300)):
            super().__init__()
            original_image = pygame.image.load(image).convert_alpha()
            self.dino_image = pygame.transform.scale(original_image, scale)
            self.image = self.dino_image
            self.rect = self.image.get_rect(topleft=(x, y))
            self.velocity_y = 0
            self.jump_force_easy = -20      # moderate upward push
            self.jump_force_difficult = -25 # slightly stronger for harder obstacles
            self.gravity = 0.7              # pulls dino down a bit quicker
            self.ground_y = self.rect.y



            self.running_frames = []
            self.jump_frames = []
            self.fall_frames = []
            self.frame_index = 0
            self.animation_speed = 0.15
            self.current_animation = []
            self.jumping = False
            self.falling = False

            self.speed = 8  
            self.moving = True  


        def animate(self, animation_list):
            if not animation_list:
                return 

            self.current_animation = animation_list
            self.frame_index += self.animation_speed

            if self.frame_index >= len(self.current_animation):
                self.frame_index = 0

            frame = self.current_animation[int(self.frame_index)]
            self.image = pygame.transform.scale(frame, self.rect.size)

        
        def jump_animation(self, jump_animation_list):
             #Animation character jump sequence (NO FRAMES YET)
            if self.jumping:
                self.jump_animation(self.jump_frames)
            elif self.falling:
                self.fall_animation(self.fall_frames)
            else:
                self.animate(self.running_frames)
        
        def fall_animation(self, fall_animation_list):
             #Animation character fall sequence (NO FRAMES YET)
             pass
        
        def jump(self, obstacle_difficulty):
            if not self.jumping and not self.falling:  # Prevent mid-air re-jumps
                if obstacle_difficulty == "easy":
                    self.velocity_y = self.jump_force_easy
                elif obstacle_difficulty == "difficult":
                    self.velocity_y = self.jump_force_difficult
                self.jumping = True

        def stop(self):
            self.moving = False

        def resume(self):
            self.moving = True
                  
        def draw(self,screen):
             screen.blit(self.image, self.rect)

             
        def update(self):
            if self.jumping or self.falling:
                self.velocity_y += self.gravity
                self.rect.y += self.velocity_y

                self.rect.x += 2  # Short forward leap

                if self.rect.y >= self.ground_y:
                    self.rect.y = self.ground_y
                    self.jumping = False
                    self.falling = False
                    self.velocity_y = 0
            elif self.moving:
                # Reset to base position if needed
                if self.rect.x > 0:  
                    self.rect.x -= 2  # Slide back to start after jump


#---------------------Obstacles-----------------------#

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, obstacle_type="easy", x=900, y=280, scale=(80, 120)):
        super().__init__()
        self.obstacle_type = obstacle_type

        if obstacle_type == "easy":
            img = pygame.image.load("easy.png").convert_alpha()
            scale = (300, 300)
        else:
            img = pygame.image.load("Difficult.png").convert_alpha()
            scale = (250, 250)

        self.image = pygame.transform.scale(img, scale)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.presses_required = 5 if obstacle_type == "easy" else 10

        self.made_jump = False

    def update(self, speed):
        self.rect.x -= speed  # move toward the player

    def character_detected(self, dino, detection_distance=400):
        # Checks if dino is close enough to interact
        # print(abs(self.rect.x - dino.rect.x) < detection_distance)
        return (abs(self.rect.x - dino.rect.x) < detection_distance) and self.made_jump == False

    @staticmethod
    def randomly_generate_obstacle():
        obstacle_type = random.choice(["easy", "difficult"])
        return Obstacles(obstacle_type)

#---------------------Button-------------------------#

class Button(pygame.sprite.Sprite):
     
     def button_pressed(self, button_function):
          #When button pressed, perform button function
          pass


#-------------------Progress Bar---------------------#
class Progress_Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, max_progress, bar_bg_image=None, fill_color=(0, 255, 0), fill_padding=100):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width          # Total width of the outer bar
        self.height = height
        self.max_progress = max_progress
        self.current_progress = 0
        self.fill_color = fill_color


        # Load background image if provided
        self.bg_image = None
        if bar_bg_image:
            self.bg_image = pygame.image.load(bar_bg_image).convert_alpha()
            self.bg_image = pygame.transform.scale(self.bg_image, (width, height))

        # Create image surface and rect
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update_progress(self, amount=1):
        self.current_progress += amount
        if self.current_progress > self.max_progress:
            self.current_progress = self.max_progress

    def reset(self):
        self.current_progress = 0

    def draw(self, screen):
        # Clear surface
        self.image.fill((0, 0, 0, 0))  # Transparent

        # Draw background of the bar
        if self.bg_image:
            self.image.blit(self.bg_image, (0, 0))
        else:
            pygame.draw.rect(self.image, (50, 50, 50), (0, 0, self.width, self.height), border_radius=4)

        # Padding inside the progress bar
        padding = 20
        inner_width = self.width - 2 * padding
        inner_height = self.height - 2 * padding

        # Calculate fill width (clamped to avoid overflow)
        fill_ratio = self.current_progress / self.max_progress
        fill_width = max(0, min(inner_width, int(fill_ratio * inner_width)))

        # Draw fill inside the bar's inner area
        if fill_width > 0:
            pygame.draw.rect(
                self.image,
                self.fill_color,
                (padding, padding, fill_width, inner_height),
                border_radius=2
            )

        # Blit to screen
        screen.blit(self.image, self.rect)

     


          
     
     


