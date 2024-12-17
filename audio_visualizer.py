import math
import pygame
from scipy.io import wavfile
from variables import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
import math
import pygame
from scipy.io import wavfile

class AudioVisualizer:
    def __init__(self, audio_file):
        """
            Inicializa el visualizador con un archivo de audio .wav
        """
        self.audio_file = audio_file
        self.samplerate, self.data = wavfile.read(audio_file)
        print(f"samplerate: {self.samplerate}")
        print(f"data: {self.data}")
        
        # asegurarse de que el audio es mono, si no, usar solo un canal
        try:
            _, num_channels = self.data.shape
            if num_channels > 1:
                self.data = self.data[:, 0]  # usar solo el canal izquierdo
        except ValueError:
            pass
        
        # normalizar datos para evitar overflow
        # divide todas las amplitudes por el valor maximo para que esten en el rango [-1, 1]
        # esto asegura que los valores sean proporcionales y faciles de escalar para la visualizacion
        self.data = self.data / max(abs(self.data))
        
        # variables de visualizacion
        self.position = 0  # indica el punto actual en el array de datos
        self.amplitude = 0 # almacena la amplitud calculada (RMS) en cada cuadro
        self.clock = pygame.time.Clock()
        
        # Configurar el audio con pygame.mixer con la misma tasa de muestreo del archivo de audio
        pygame.mixer.init(frequency=self.samplerate)
        pygame.mixer.music.load(audio_file)
    
    def update(self):
        """
            Actualiza la amplitud basada en la posicion actual del audio.
            Sincroniza la visualizacion con la reproduccion del audio.
        """
        if pygame.mixer.music.get_busy(): # checkar que el audio no se este reproduciendo
            # avanzar posicion en el audio
            samples_per_frame = self.samplerate // FPS
            self.position += samples_per_frame
            if self.position < len(self.data):
                # extrae un segmento (chunk) del array correspondiente al cuadro actual
                chunk = self.data[self.position:self.position + samples_per_frame]
                # print(f"chunk: {chunk}")
                # calcular RMS (https://es.wikipedia.org/wiki/Valor_eficaz) de las muestras actuales
                # para obtener una amplitud promedio
                self.amplitude = math.sqrt(sum(sample ** 2 for sample in chunk) / len(chunk))
                # print(f"amplitude: {self.amplitude}")
            else:
                self.amplitude = 0
        else:
            self.amplitude = 0  # el audio termino de reproducir
    
    def draw(self, screen):
        """
            Dibuja la onda sinusoidal en pantalla basada en la amplitud actual.
            Generación de Puntos:
                - Si la amplitud es significativa (> 0.01):
                    - Genera puntos (x, y) que forman una onda sinusoidal.
                    - x: Avanza de 0 a SCREEN_WIDTH.
                    - y: Oscila alrededor del centro vertical de la pantalla (SCREEN_HEIGHT / 2) proporcional a la amplitud actual.
                    - math.sin(x * 0.02): Crea una oscilación sinusoidal.
        """
        points = []
        if self.amplitude > 0.01:
            for x in range(SCREEN_WIDTH):
                y = SCREEN_HEIGHT / 2 + int(self.amplitude * 300 * math.sin(x * 0.02))
                points.append((x, y))
        else:
            points = [(0, SCREEN_HEIGHT / 2), (SCREEN_WIDTH, SCREEN_HEIGHT / 2)]
        
        # print(points)
        pygame.draw.lines(screen, (255, 0, 0), False, points, 6)