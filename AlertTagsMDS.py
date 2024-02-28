import cv2
import numpy as np
import pyautogui
import pygame
import time

# Coordenadas y dimensiones del área de captura
x1, y1, width, height = 90, 490, 230, 300
color = (0, 0, 255)

# Inicializar pygame y la pantalla
pygame.init()
screen = pygame.display.set_mode((450, 150))
pygame.display.set_caption("Control de Sonido")

# Cargar las imágenes de parlante encendido y apagado
img_sound_on = pygame.transform.scale(pygame.image.load('prtON.png'), (203, 128))
img_sound_off = pygame.transform.scale(pygame.image.load('prtOFF.png'), (203, 128))
img_sound_rect = img_sound_on.get_rect()
img_sound_rect.topleft = (150, 10)


# Estado inicial del sonido
muted = False

initial_screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
initial_image = np.array(initial_screenshot)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cv2.destroyAllWindows()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si el clic fue dentro del botón de sonido
            if img_sound_rect.collidepoint(event.pos):
                muted = not muted

    current_screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    current_image = np.array(current_screenshot)

    if not np.array_equal(initial_image, current_image):
        print("¡Alerta! Se ha detectado una notificación.")
        if not muted:
            pygame.mixer.Sound('beep.mp3').play()

        color = (0, 255, 0)
        initial_image = current_image
    else:
        color = (0, 0, 255)

    img_with_rectangle = cv2.rectangle(current_image, (x1, y1), (x1 + width, y1 + height), color, 2)

    # Mostrar la imagen de parlante según el estado de silencio
    screen.fill((255, 255, 255))
    if not muted:
        screen.blit(img_sound_on, img_sound_rect)
    else:
        screen.blit(img_sound_off, img_sound_rect)
    pygame.display.flip()

    cv2.imshow('Monitoreo de pantalla', img_with_rectangle)

    key = cv2.waitKey(1000)
    if key == 27:
        break

    time.sleep(0.1)

pygame.quit()
cv2.destroyAllWindows()
