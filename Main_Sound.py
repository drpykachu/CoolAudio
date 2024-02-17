import pygame
import numpy as np
import sys
import wave
import os
from math import sin, cos, radians
from Audio_Functions import *


# Initialize Pygame
pygame.init()

# Constants
x = 200
y = 45

chunk_size = 1024
pertubation = 35
rotation_speed = 0.5


WIDTH, HEIGHT = 800, 800
FPS = 60



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



signal = np.array(shape(300,4))
# signal = np.array(circle(300))


        


# Main loop
running = True
rotation_counter = 1

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Get current playback position
    pos = pygame.mixer.music.get_pos() / 1000  # Convert to seconds

    # Read a chunk of audio data corresponding to the current playback position
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


    x_axis = np.array((left_channel_normalized) * WIDTH / 2 / pertubation) + signal[0]
    y_axis = np.array((right_channel_normalized) * HEIGHT / 2 / pertubation) + signal[1]
    
    x_axis, y_axis = rotation([x_axis,y_axis],'x-y',rotation_speed*rotation_counter,direction = 'cw')
    x_signal,y_signal = rotation([signal[0],signal[1]],'x-y',rotation_speed*rotation_counter,direction = 'cw')
    
    # Draw waveform
    for i in range(len(left_channel_normalized) - 1):
        
        x1 = x_axis[i]
        x2 = x_axis[i+1]
        y1 = y_axis[i]
        y2 = y_axis[i+1]
        
        
        pygame.draw.line(screen, (240, 0, 240), (x1, y1), (x2, y2), 5)  # Draw a line between consecutive points
        pygame.draw.circle(screen, (240, 240, 240), (x_signal[i], y_signal[i]), 2)  # Draw a point for each sample
        pygame.draw.circle(screen, (240, 240, 240), (WIDTH/2, HEIGHT/2), 1)  # Draw a point for each sample
    
    pygame.draw.line(screen, (240, 0, 240), (x_axis[0], y_axis[0]), (x_axis[-1], y_axis[-1]), 5)  # closes the drawn loop

     # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
    rotation_counter = rotation_counter + 1
pygame.quit()



sys.exit()





