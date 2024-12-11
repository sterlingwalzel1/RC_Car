import keyboard

def get_key_input():
    valid_keys = ['up', 'down', 'left', 'right', 'space']
    for key in valid_keys:
        if keyboard.is_pressed(key):
            return key  # Return the key that was pressed
    return None  # If no key is pressed, return None

while True:
    key_pressed = get_key_input()
    if key_pressed:
        print(f"Key pressed: {key_pressed}")