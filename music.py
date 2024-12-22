import pygame

sound_enabled = True
def toggle_sound():
    """
    Toggle the sound state of the game (ON/OFF).

    """
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.pause()

sound_objects = {}
def load_sound(name, file_path, is_music=False):
    """
    Load a sound or music file and store it in a global sound object.

    Parameters
    ----------
    name : str
        The name identifier for the sound or music.
    file_path : str
        The file path of the sound or music file to load.
    is_music : bool, optional
        If True, the file is loaded as background music; otherwise, as a sound effect.
    """
    if is_music:
        sound_objects[name] = "music"
    else:
        sound_objects[name] = pygame.mixer.Sound(file_path)

def play_music(file_path, volume=0.5):
    """
    Play background music in a loop.

    Parameters
    ----------
    file_path : str
        The file path of the music file.
    volume : float, optional
        The volume of the music (default is 0.5).
    """
    if sound_enabled:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

def stop_music():
    """
    Stop the currently playing music.
    """
    pygame.mixer.music.stop()

def play_menu_music(file_path, volume=0.5):
    """
    Play menu background music in a loop.

    Parameters
    ----------
    file_path : str
        The file path of the menu music file.
    volume : float, optional
        The volume of the menu music.
    """
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

def play_sound(file_path, volume=1.0):
    """
    Play an individual sound effect.

    Parameters
    ----------
    file_path : str
        The file path of the sound effect.
    volume : float, optional
        The volume of the sound effect.
    """
    if sound_enabled:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(1)


def shooting(sound_file, volume=0.5):
    """
    Play a shooting sound effect.

    Parameters
    ----------
    sound_file : str
        The file path of the shooting sound effect.
    volume : float, optional
        The volume of the shooting sound (default is 0.5).
    """
    sound = pygame.mixer.Sound(sound_file)
    sound.set_volume(volume)
    sound.play()

def is_sound_enabled():
    """
    Check if sound is enabled.

    Returns:
    -------
    bool
        True if sound is enabled, False otherwise.
    """
    return sound_enabled

def play_background_music(music_file):
    """
    Play background music.

    Parameters
    ----------
    music_file : str
        The music file to be played.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
