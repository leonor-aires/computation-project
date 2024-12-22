import pygame

sound_enabled = True
def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    print(f"[DEBUG] Toggling sound: {sound_enabled}")
    if sound_enabled:
        print("Sound is ON")
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play(-1)
    else:
        print("Sound is OFF")
        pygame.mixer.music.pause()

sound_objects = {}
def load_sound(name, file_path, is_music=False):
    if is_music:
        sound_objects[name] = "music"  # Placeholder for music
    else:
        sound_objects[name] = pygame.mixer.Sound(file_path)

def play_music(file_path, volume=0.5):
    """Play background music."""
    if sound_enabled:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

def stop_music():
    """Stop the music."""
    pygame.mixer.music.stop()

def play_menu_music(file_path, volume=0.5):
    """Play menu music."""
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

def stop_menu_music():
    """Stop the music."""
    pygame.mixer.music.stop()

def play_sound(file_path, volume=1.0):
    """Play an individual sound effect."""
    if sound_enabled:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(1)

def stop_sound(name):
    """Stop an individual sound effect."""
    pygame.mixer.music.stop()


def shooting(sound_file, volume=0.5):
    sound = pygame.mixer.Sound(sound_file)
    sound.set_volume(volume)
    sound.play()

def is_sound_enabled():
    """Return the current state of sound_enabled."""
    print(f"[DEBUG] is_sound_enabled: {sound_enabled}")
    return sound_enabled
