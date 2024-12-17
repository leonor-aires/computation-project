import pygame, json, os

SAVE_FILE = "progress.json"

def save_progress(progress):
    """
    Save the player's progress to a file.

    Parameters:
        progress (dict): A dictionary containing player's progress data.
    """
    with open(SAVE_FILE, "w") as file:
        json.dump(progress, file)
    print("Progress saved successfully!")

def load_progress():
    """
    Load the player's progress from a file.

    Returns:
        dict: A dictionary containing player's progress data.
    """
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            progress = json.load(file)
        print("Progress loaded successfully!")
        return progress
    else:
        print("No save file found. Starting with default progress.")
        return {
            "level": 1,
            "coins": 0,
            "health": 100,
            "powerups": [],
        }
