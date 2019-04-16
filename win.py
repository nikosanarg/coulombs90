		#===== COULOMBUS - NIKOS90 - SANDOBAL NICOLAS =====#
		#====== SIMULACION DE CARGAS ELECTRICAS BAJO ======#
		#===== EL ANÁLISIS MEDIANTE LA LEY DE COULOMB =====#
		#= permitida su reproducción y divulgación - 2019 =#
		#==================================================#

#""" #QUITAR EL "#" AL PRINCIPIO DE ESTA LÍNEA PARA CAMBIAR DE CÓDIGO

import pygame
import time
import math

full_screen = "ON" 	# PANTALLA COMPLETA ON/OFF
modo_oscuro = "ON" 	# MODO PANTALLA OSCURA ON/OFF
version = "v 1.3.1"
#v 1.3.0 primer release versionada en github

background_wh = pygame.image.load("images/background.jpg")
background_bl = pygame.image.load("images/backgroundblack.jpg")
background_wh_768 = pygame.image.load("images/background768.jpg")
background_bl_768 = pygame.image.load("images/backgroundblack768.jpg")

if full_screen == "ON":
	win_size = (widthf, heightf) = (1366, 768)
	origin = (orig_x, orig_y) = (round(widthf / 2), round(heightf/2))
	if modo_oscuro != "ON":
		color_base = (50, 50, 50)
		bg = background_wh_768
	else:
		color_base = (255, 255, 255)
		bg = background_bl_768
	win = pygame.display.set_mode(win_size, pygame.FULLSCREEN)
else:
	win_size = (width, height) = (600, 400)
	origin = (orig_x, orig_y) = (round(width / 2), round(height/2))
	if modo_oscuro != "ON":
		color_base = (50, 50, 50)
		bg = background_wh
	else:
		color_base = (255, 255, 255)
		bg = background_bl
	win = pygame.display.set_mode(win_size)
icon = pygame.image.load("images/coulomb.ico")

win.blit(bg, (0, 0))
pygame.display.flip()
pygame.display.set_caption("Coulombs ", version)
pygame.display.set_icon(icon)

# ===== Global Vars =================================================

fps = 60
time = 0
clock = pygame.time.Clock()
cargas = []
radio_q = 10
color = {
		"grey":(135, 135, 135),
		"red":(255, 40, 0), 
		"blue":(0, 128, 255)}
pygame.font.init()
font = pygame.font.SysFont("arial", 16, True, False)
font_f = pygame.font.SysFont("couriernew", 12, True, False)
coulomb_constant = 9 * (10 ** 9)
run = True

ver_etiquetas = True

f_is_pressed = False
m_is_pressed = False
c_is_pressed = False
p_is_pressed = False

# ===== Functions ===================================================

def redimensionar():
	global win, win_size, bg, full_screen, modo_oscuro, radio_q, orig_x, orig_y
	if full_screen == "ON":
		win_size = (widthf, heightf) = (1366, 768)
		origin = (orig_x, orig_y) = (round(widthf / 2), round(heightf/2))
		if modo_oscuro != "ON":
			bg = background_wh_768
		else:
			bg = background_bl_768
		win = pygame.display.set_mode(win_size, pygame.FULLSCREEN)
	else:
		win_size = (width, height) = (600, 400)
		origin = (orig_x, orig_y) = (round(width / 2), round(height/2))
		if modo_oscuro != "ON":
			bg = background_wh
		else:
			bg = background_bl
		win = pygame.display.set_mode(win_size)

def leer_teclas():
	global win, win_size, bg, full_screen, modo_oscuro, radio_q, orig_x, orig_y, ver_etiquetas
	global f_is_pressed, m_is_pressed, c_is_pressed, p_is_pressed
	global run, color_base, cargas

	keys = pygame.key.get_pressed()

	if keys[pygame.K_ESCAPE]:
		print("Saliendo de Coulombus ", version)
		run = False

	if keys[pygame.K_f]:
		if f_is_pressed == False:
			if full_screen == "ON": full_screen = "OFF"
			else: full_screen = "ON"
			f_is_pressed = True
	else: f_is_pressed = False

	if keys[pygame.K_m]:
		if m_is_pressed == False:
			if modo_oscuro == "ON": 
				modo_oscuro = "OFF"
				color_base = (50, 50, 50)
			else: 
				modo_oscuro = "ON"
				color_base = (255, 255, 255)
			m_is_pressed = True
	else: m_is_pressed = False

	if f_is_pressed or m_is_pressed: redimensionar()

	if keys[pygame.K_c]:
		if c_is_pressed == False:
			if ver_etiquetas == True: ver_etiquetas = False
			else: ver_etiquetas = True
			c_is_pressed = True
	else: c_is_pressed = False

	if keys[pygame.K_SPACE]:
		for q in cargas:
			q.move()

def actualizar_ventana():
	global time, clock, p_is_pressed, cargas

	win.blit(bg, (0, 0)) # actualizar el background (fundamental en cada iteracion)

	for q in cargas: 
		q.draw(win) # dibujar las cargas en el mapa
	
	"""
	if ver_etiquetas: # texto de tiempo, cargas, informacion, etc
		texto_tiempo = font.render("{:.0f} segundos".format(time), 1, color_base)
		win.blit(texto_tiempo, (20, 20))#"""

	pygame.display.update()

def calcular_distancia(q1, q2):
	a_metros = 10 ** (-2) # llevar de cm (centimetros) a m (metros)
	r = math.sqrt(((q2.x - q1.x )** 2) + ((q2.y - q1.y)** 2)) * a_metros # distancia
	return r

def calcular_versor(q1, q2):
	a_metros = 10 ** (-2) # llevar de cm (centimetros) a m (metros)
	r = calcular_distancia(q1, q2)
	versor = ((q1.x - q2.x) * a_metros / r, (q1.y - q2.y) * a_metros / r) # vector unitario
	return versor

def calcular_fuerza(q1, q2):
	global coulomb_constant
	a_uC = 10 ** (-6) # llevar de μC (microCoulombs) a C (Coulombs)
	r = calcular_distancia(q1, q2)
	#print(r)
	fuerza = (coulomb_constant * q1.carga * a_uC * q2.carga * a_uC) / (r ** 2) # fuerza
	return fuerza

def definir_color(carga = 0.0):
	if carga == 0:
		return color["grey"]
	elif carga > 0:
		return color["red"]
	else:
		return color["blue"]

def definir_signo(v = 0.0):
	if v >= 0:
		return 1
	else:
		return -1

class Carga():
	def __init__(self, posx=0.0, posy=0.0, carga=0.0, estatica=False):
		self.x = posx # puro, sin escalar x25 px
		self.y = posy # puro, sin escalar x25 px
		self.carga = carga
		self.color = definir_color(carga)
		self.estatica = estatica
		self.v = (0.0, 0.0)

	def move(self):
		global full_screen, fps
		if self.estatica == False:
			if full_screen == "OFF":
				maxx = 300
				maxy = 200
			else:
				maxx = 683
				maxy = 384 
			px = self.x + self.v[0] / fps
			py = self.y + self.v[1] / fps
			if px > (maxx / 25):
				self.x = maxx / 25
			elif px < (-maxx / 25):
				self.x = -maxx / 25
			else:
				self.x = px
			if py > (maxy / 25):
				self.y = maxy / 25
			elif self.y < (-maxy / 25):
				self.y = -maxy / 25
			else: self.y = py
		
	def draw(self, win):
		global orig_x, orig_y, color_base, ver_etiquetas, cargas, fps
		
		xint = round(self.x * 25) # se escalan x25 px las coordenadas x e y
		yint = -round(self.y * 25) # para dibujar correctamente las particulas
		pygame.draw.circle(win, definir_color(self.carga), (xint + orig_x, yint + orig_y), radio_q)
		
		if ver_etiquetas:
			if self.carga < 0:
				texto_carga = font.render("{:.0f}µC".format(self.carga), 1, color_base)
			else: 
				texto_carga = font.render("+{:.0f}µC".format(self.carga), 1, color_base)
			win.blit(texto_carga, (xint + orig_x - 17, yint + orig_y - 42))

		# se calcula el vector fuerza resultante
		self.v = (0.0, 0.0)
		for q in cargas:
			if q.x != self.x or q.y != self.y:
				fuerza = calcular_fuerza(self, q)
				versor = calcular_versor(self, q)
				self.v = (self.v[0]+(versor[0] * fuerza), self.v[1]+(versor[1] * fuerza))
		posi1 = (self.x * 25 + orig_x, -self.y * 25 + orig_y)
		# se calcula el versor resultante puro
		fuerza_total = math.sqrt((self.v[0])**2 + (self.v[1])**2)
		if fuerza_total == 0.0:
			versor = (0.0, 0.0)
		else:
			versor = (self.v[0] / fuerza_total, self.v[1] / fuerza_total)
		# se realiza la escala para no dibujar versores extremadamente grandes o pequeños
		escala = 10
		if fuerza_total * escala > 150:
			vecfx = 150 * versor[0] 
			vecfy = 150 * versor[1] 
		elif fuerza_total * escala < 10:
			vecfx = 10 * versor[0] 
			vecfy = 10 * versor[1]
		else:
			vecfx = versor[0] * fuerza_total * escala
			vecfy = versor[1] * fuerza_total * escala
		# se calcula la posicion final del vector fuerza y se lo dibuja
		posf1 = (round(vecfx + posi1[0]), round(-vecfy + posi1[1]))
		pygame.draw.line(win, color_base, posi1, posf1, 3)
		pygame.draw.circle(win, color_base, (posf1[0], posf1[1]), 5)
		if ver_etiquetas:
			fuerza_total = math.sqrt((self.v[0])**2 + (self.v[1])**2)
			texto_f = font_f.render("{:.2f}N".format(fuerza_total), 1, color_base)
			win.blit(texto_f, (posf1[0] - 15, posf1[1] - 20))

def agregar_carga(x, y, q = 0.0, e = False):
	global cargas
	q = Carga(x, y, q, e)
	cargas.append(q)

# ===== Variables de testeo =========================================

#""" #DISPOSICION TUNEL 
agregar_carga(3, 5, -1, True)
agregar_carga(3, -5, -1, True)
agregar_carga(0, 5, -1, True)
agregar_carga(0, -5, -1, True)
agregar_carga(-3, 5, -1, True)
agregar_carga(-3, -5, -1, True)
agregar_carga(-15, 0, -8.25, True)
agregar_carga(20, 0, 30)#"""

"""# DISPOSICION CUADRADO
agregar_carga(-2, -2, 1)
agregar_carga(-2, 2, 1)
agregar_carga(2, -2, 1)
agregar_carga(2, 2, 1)
agregar_carga(0, 6, -1, True)
agregar_carga(0, -6, -1, True)
agregar_carga(6, 0, -1, True)
agregar_carga(-6, 0, -1, True)#"""




# ===== Mainloop ====================================================

try:
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		clock.tick(fps)
		time += 1/fps
		leer_teclas()
		actualizar_ventana()
except SystemExit:
	#pygame.display.quit()
	pygame.quit()
