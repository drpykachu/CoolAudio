import pygame
import numpy as np
import sys
import wave
import os

# Initialize Pygame
pygame.init()

# Constants
x = 900
y = 45
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
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

chunk_size = 1024
pertubation = 10

def circle(radius):
    theta = np.linspace(0,2*3.14,chunk_size)
    x_circ = radius*np.cos(theta) + WIDTH/2
    y_circ = radius*np.sin(theta) + HEIGHT/2
    return [x_circ,y_circ]
    
def square(length):
    
    x1 = list(np.linspace(0,length,int(chunk_size/4)))
    x2 = list(np.zeros(int(chunk_size/4))+length)
    x3 = list(np.linspace(length,0,int(chunk_size/4)))
    x4 = list(np.zeros(int(chunk_size/4)))
    
    y1 = list(np.zeros(int(chunk_size/4)))
    y2 = list(np.linspace(0,length,int(chunk_size/4)))
    y3 = list(np.zeros(int(chunk_size/4))+length)
    y4 = list(np.linspace(length,0,int(chunk_size/4)))

    return [np.array(x1+x2+x3+x4)+WIDTH/2-length/2,np.array(y1+y2+y3+y4)+HEIGHT/2-length/2]

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def shape(widther, heighter, points):
    angle = 360
    x = [0]
    y = [0]
    angle = np.linspace(0,2*3.14,points+1)
    

    separation = list(split(range(chunk_size), points))


    for i in range(0,points):
        
        x = x + list(np.cos(angle[i])*np.linspace(0,widther,len(separation[i]))+x[-1])
        y = y + list(np.sin(angle[i])*np.linspace(0,heighter,len(separation[i]))+y[-1])
    
    return [np.array(x)-(np.max(x)+np.min(x))/2+WIDTH/2,np.array(y)-(np.max(y)+np.min(y))/2+HEIGHT/2]


signal = np.array(shape(300,300,6))

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
    for i in range(len(left_channel_normalized) - 1):
        x1 = np.array((left_channel_normalized[i]) * WIDTH / 2 / pertubation) + signal[0][i]  # Scale x1 to fit within screen
        x2 = np.array((left_channel_normalized[i + 1]) * WIDTH / 2 / pertubation) + signal[0][i + 1]  # Scale x2 to fit within screen
        y1 = np.array((right_channel_normalized[i]) * HEIGHT / 2 / pertubation) + signal[1][i]  # Scale y1 to fit within screen
        y2 = np.array((right_channel_normalized[i + 1]) * HEIGHT / 2 / pertubation) + signal[1][i + 1]  # Scale y2 to fit within screen
        
        pygame.draw.line(screen, (255, 0, 0), (int(x1), int(y1)), (int(x2), int(y2)), 3)  # Draw a line between consecutive points
        pygame.draw.circle(screen, (240, 240, 240), (int(signal[0][i]), int(signal[1][i])), 1)  # Draw a point for each sample

     # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
    
pygame.quit()



sys.exit()

