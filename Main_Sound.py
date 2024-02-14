import pygame
import numpy as np
import sys
import wave

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Audio Visualizer")
clock = pygame.time.Clock()

# Take image as input 
img = pygame.image.load('rgbeat.png') 
  
# Set image as icon 
pygame.display.set_icon(img)

# Load audio file
audio_file = "left_audio.wav"  # Replace with your audio file path
wf = wave.open(audio_file, 'rb')
sample_width = wf.getsampwidth()
nchannels = wf.getnchannels()
framerate = wf.getframerate()
nframes = wf.getnframes()

# Play audio
pygame.mixer.init(frequency=framerate)
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play(-1)  # Play the music indefinitely

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Get current playback position
    pos = pygame.mixer.music.get_pos() / 1000  # Convert to seconds

    # Read a chunk of audio data corresponding to the current playback position
    chunk_size = 1024
    start_frame = int(pos * framerate)
    end_frame = min(start_frame + chunk_size, nframes)
    wf.setpos(start_frame)
    frames = wf.readframes(end_frame - start_frame)
    audio_data = np.frombuffer(frames, dtype=np.int16)

    # Extract left and right channel data
    if nchannels == 2:
        left_channel = audio_data[::2]  # Take every second element to get left channel
        right_channel = audio_data[1::2]  # Take every second element starting from the second to get right channel
    else:
        left_channel = audio_data
        right_channel = audio_data

    # Normalize audio data
    max_amplitude_left = np.max(np.abs(left_channel))
    max_amplitude_right = np.max(np.abs(right_channel))
    if max_amplitude_left > 0:
        left_channel_normalized = left_channel / max_amplitude_left
    else:
        left_channel_normalized = left_channel
    if max_amplitude_right > 0:
        right_channel_normalized = right_channel / max_amplitude_right
    else:
        right_channel_normalized = right_channel

    # Draw waveform
    for i in range(len(left_channel_normalized)):
        x = (left_channel_normalized[i] + 1) * WIDTH / 2  # Scale x to fit within screen
        y = HEIGHT - (right_channel_normalized[i] + 1) * HEIGHT / 2  # Scale y to fit within screen
        pygame.draw.circle(screen, WHITE, (int(x), int(y)), 1)  # Draw a point for each sample

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()

