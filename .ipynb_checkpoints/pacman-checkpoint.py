import pygame
import math
import random
import sys

# 2. Constantes do Jogo (Cores, Tamanhos, Velocidades, etc.)
# Cores Gerais (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0) # Cor do Pac-Man
RED = (255, 0, 0)

# Configurações do Labirinto
CELL_SIZE = 25 # Tamanho de cada célula (bloco) em pixels
WALL_LINE_THICKNESS = 4

# Configurações do Pac-Man
PACMAN_RADIUS = int(CELL_SIZE * 0.4)
PACMAN_SPEED = 2 # Velocidade em pixels por frame

# Configurações da Pílula de Poder
POWER_PILL_DURATION = 8 * 1000 # Duração do efeito da pílula de poder em milissegundos (8 segundos)
POWER_PILL_SCORE = 50 # Pontos ganhos por comer uma pílula de poder

# Configurações dos Fantasmas (opcional, pode ser adicionado depois)
GHOST_RADIUS = int(CELL_SIZE * 0.4)
GHOST_SPEED_NORMAL = 2
GHOST_SPEED_FRIGHTENED = 1 # Quando o Pacman comer a pílula
GHOST_SPEED_EATEN = 4
GHOST_EATEN_SCORE = 200 # Quando o Fantasma for comido

# Constantes para os Estados dos Fantasmas
GHOST_PHASE_SCATTER = "scatter"
GHOST_PHASE_CHASE = "chase"
GHOST_PHASE_FRIGHTENED = "frightened"
GHOST_PHASE_EATEN = "eaten"

# Duração das fases em milissegundos (baseado no jogo original, podem ser ajustadas)
SCATTER_PHASE_DURATION = 7 * 1000  # segundos em modo de dispersão
CHASE_PHASE_DURATION = 15 * 1000   # segundos em modo de perseguição
GHOST_RESPAWN_DELAY = 3 * 1000

# Cores dos fantasmas (RGB)
# No Pac-Man original, são Blinky (vermelho), Pinky (rosa), Inky (ciano), Clyde (laranja)
GHOST_BLINKY_COLOR = (255, 0, 0)      # Vermelho
GHOST_PINKY_COLOR = (255, 192, 203)   # Rosa
GHOST_INKY_COLOR = (0, 255, 255)      # Ciano
GHOST_CLYDE_COLOR = (255, 165, 0)     # Laranja
GHOST_FRIGHTENED_COLOR = (0, 0, 255)  # Azul (quando assustado)
GHOST_EATEN_COLOR = (128, 128, 128)   # Cinza (quando está voltando para a casa)

# Posições iniciais dos fantasmas (coordenadas do grid)
# Essas são posições aproximadas da "casa" dos fantasmas no labirinto
GHOST_START_POSITIONS = {
    "blinky": (13, 13), # Blinky geralmente começa fora da casa ou na porta
    "pinky": (13, 14),  # Pinky no meio da casa
    "inky": (12, 14),   # Inky à esquerda da casa
    "clyde": (14, 14),  # Clyde à direita da casa
}

# Coordenadas dos cantos do labirinto
SCATTER_TARGETS = {
    "blinky": (25, 0),
    "pinky": (5, 0),
    "inky": (27, 30),
    "clyde": (0, 30),
}

# Alvo para o Fantasma ir ao Sair da Casa
GHOST_EXIT_TARGET = (13,11)

# Alvo para o fantasma ir quando está comido e voltando para a casa
GHOST_CENTER_HOUSE_TARGET = (13, 13) # Um ponto central dentro da casa para onde fantasmas comidos retornam

# Constantes para a Casa dos Fantasmas
# Estas são as coordenadas do grid que definem a ÁREA da casa dos fantasmas (incluindo porta e interior)
GHOST_HOUSE_DOOR_ROW = 12             # A linha Y do grid onde a porta (4) está localizada
GHOST_HOUSE_DOOR_COL_START = 13       # A coluna X inicial do grid da porta (4)
GHOST_HOUSE_DOOR_COL_END = 14         # A coluna X final do grid da porta (4)

GHOST_HOUSE_INTERIOR_MIN_X = 12       # Coluna inicial (X) da área interna de movimentação dos fantasmas (onde há '0's dentro da casa)
GHOST_HOUSE_INTERIOR_MAX_X = 15       # Coluna final (X) da área interna
GHOST_HOUSE_INTERIOR_MIN_Y = 13       # Linha inicial (Y) da área interna
GHOST_HOUSE_INTERIOR_MAX_Y = 14       # Linha final (Y) da área interna

# --- 3. Definição do Labirinto (Matriz 2D) ---
# Convenções para a matriz:
# 0 = Caminho vazio (onde o Pac-Man e fantasmas podem andar)
# 1 = Parede (obstáculo)
# 2 = Pílula (pequeno ponto comestível)
# 3 = Pílula de Poder (ponto grande, deixa fantasmas vulneráveis)
# 4 = Porta da casa dos fantasmas (apenas fantasmas podem atravessar)

level = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 4, 4, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],# Linha da porta dos fantasmas
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],  # Túnel lateral
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
# Calcular as dimensões da tela com base no labirinto
SCREEN_WIDTH = len(level[0]) * CELL_SIZE
SCREEN_HEIGHT = len(level) * CELL_SIZE

# ---Contagem de Pílulas e Cópia do Labirinto Original ---
original_level = [row[:] for row in level]

total_pills = 0  # Inicialize a contagem
for r_idx, row in enumerate(original_level):
    for c_idx, cell in enumerate(row):
        if cell == 2 or cell == 3:  # Conta pílulas normais (2) e pílulas de poder (3)
            total_pills += 1

pills_left = total_pills
# depuracção print({pills_left})


def _is_in_ghost_house_area(r, c):
    return (r == GHOST_HOUSE_DOOR_ROW and GHOST_HOUSE_DOOR_COL_START <= c <= GHOST_HOUSE_DOOR_COL_END) or \
        (GHOST_HOUSE_INTERIOR_MIN_Y <= r <= GHOST_HOUSE_INTERIOR_MAX_Y and
         GHOST_HOUSE_INTERIOR_MIN_X <= c <= GHOST_HOUSE_INTERIOR_MAX_X)


# 4. Classes do Jogo (PacMan e Ghost)
# --- Classe PacMan ---
class PacMan:
    def __init__(self, start_x_grid, start_y_grid, radius, speed, cell_size):
        self.grid_x = start_x_grid
        self.grid_y = start_y_grid

        # Variáveis para a pílula de poder
        self.is_powered_up = False
        self.power_up_timer = 0  # Usaremos pygame.time.get_ticks() para gerenciar isso

        # Posição em pixels, centralizada na célula
        self.pixel_x = float(self.grid_x * cell_size + cell_size // 2)
        self.pixel_y = float(self.grid_y * cell_size + cell_size // 2)

        self.radius = radius
        self.color = YELLOW
        self.speed = speed
        self.cell_size = cell_size

        # Direção de movimento atual (pixels por frame)
        self.dx = 0
        self.dy = 0

        # Direção desejada (para viradas)
        self.desired_dx_val = 0  # Valor de -1, 0 ou 1
        self.desired_dy_val = 0  # Valor de -1, 0 ou 1

        # Animação da boca do Pac-Man
        self.mouth_open = True  # Começa com a boca aberta
        self.mouth_speed = 2.0  # Velocidade da animação da boca
        self.current_mouth_angle = 45  # Ângulo inicial da boca aberta (metade do ângulo total da boca)
        self.target_mouth_angle = 45  # Ângulo que a boca tenta alcançar
        self.closed_mouth_angle = 0  # Ângulo da boca fechada
        self.open_mouth_angle = 45  # Ângulo da boca totalmente aberta (metade do ângulo total da boca)

        # Direção para o desenho da boca (0=right, 90=up, 180=left, 270=down)
        self.facing_angle = 0  # Começa virado para a direita (0 graus)

        self.last_moved_direction = (1, 0)  # (dx, dy) para a última direção em que realmente se moveu

    def set_direction(self, dx_val, dy_val):
        """Define a direção desejada do Pac-Man."""
        self.desired_dx_val = dx_val
        self.desired_dy_val = dy_val

    def get_grid_pos(self):
        """Retorna a posição do Pac-Man no grid (inteiros)."""
        return int(self.pixel_x // self.cell_size), int(self.pixel_y // self.cell_size)

    def is_aligned_to_grid(self):
        """Verifica se o Pac-Man está aproximadamente no centro de uma célula."""
        # Margem de erro para alinhamento
        tolerance = self.speed // 2

        # Calcula a diferença entre a posição pixel e o centro da célula atual
        center_x_of_current_grid = self.grid_x * self.cell_size + self.cell_size // 2
        center_y_of_current_grid = self.grid_y * self.cell_size + self.cell_size // 2

        # Verifica se o pixel_x está próximo do centro horizontal da célula
        aligned_x = abs(self.pixel_x - center_x_of_current_grid) <= tolerance
        # Verifica se o pixel_y está próximo do centro vertical da célula
        aligned_y = abs(self.pixel_y - center_y_of_current_grid) <= tolerance

        return aligned_x and aligned_y

    def can_move_in_direction(self, dx_check, dy_check, game_level):
        """
        Verifica se é possível mover para a próxima célula na direção (dx_check, dy_check).
        Considera a próxima célula inteira.
        """
        current_grid_x, current_grid_y = self.get_grid_pos()

        target_grid_x = current_grid_x + dx_check
        target_grid_y = current_grid_y + dy_check

        # --- LÓGICA PARA TÚNEL: Permite movimento para fora do grid para teletransporte ---
        tunnel_row = 15  # <--- Defina esta constante para a linha do túnel (índice 15)

        # Se o Pac-Man está na linha do túnel E está tentando se mover para fora da tela
        if current_grid_y == tunnel_row:
            if (current_grid_x == 0 and dx_check < 0) or \
                    (current_grid_x == len(game_level[0]) - 1 and dx_check > 0):
                return True  # Permite o movimento "off-screen" para o túnel

        # Garante que a próxima célula está dentro dos limites do labirinto
        if not (0 <= target_grid_y < len(game_level) and 0 <= target_grid_x < len(game_level[0])):
            return False  # Fora dos limites, não pode mover

        # Verifica se a próxima célula é uma parede (1)
        if game_level[target_grid_y][target_grid_x] == 1:
            return False  # É uma parede, não pode mover

        # Adicione lógica para a porta dos fantasmas (4)
        # Pac-Man não pode atravessar a porta dos fantasmas
        if game_level[target_grid_y][target_grid_x] == 4:
            return False

        return True  # Pode mover

    def update(self, game_level):
        """Atualiza a posição do Pac-Man e lida com colisões, viradas, e animação."""

        # 1. Atualizar a posição do Pac-Man no grid (sempre no início do update)
        self.grid_x = int(self.pixel_x // self.cell_size)
        self.grid_y = int(self.pixel_y // self.cell_size)

        points_gained = 0  # Inicializa a pontuação ganha neste frame
        pill_eaten_this_frame = False  # Para saber se comeu algo

        # --- DEPURAÇÃO CRÍTICA: Posição do Pac-Man (SEMPRE ATIVO) ---
        # print(f"PacMan Grid: ({self.grid_x}, {self.grid_y}) | Pixel: ({self.pixel_x:.2f}, {self.pixel_y:.2f}) | DX: {self.dx}, DY: {self.dy}")

        # 2. Lógica de virada e movimento (com base na desired_direction)
        if self.desired_dx_val != 0 or self.desired_dy_val != 0:
            if self.is_aligned_to_grid():
                if self.can_move_in_direction(self.desired_dx_val, self.desired_dy_val, game_level):
                    self.dx = self.desired_dx_val * self.speed
                    self.dy = self.desired_dy_val * self.speed
                    self.pixel_x = float(self.grid_x * self.cell_size + self.cell_size // 2)
                    self.pixel_y = float(self.grid_y * self.cell_size + self.cell_size // 2)
                else:
                    self.desired_dx_val = 0
                    self.desired_dy_val = 0

        # 3. Aplicar movimento atual e tratar colisão com paredes
        if self.dx != 0 or self.dy != 0:
            if self.can_move_in_direction(self.dx // self.speed, self.dy // self.speed, game_level):
                self.pixel_x += self.dx
                self.pixel_y += self.dy
            else:
                self.dx = 0
                self.dy = 0
                self.pixel_x = float(self.grid_x * self.cell_size + self.cell_size // 2)
                self.pixel_y = float(self.grid_y * self.cell_size + self.cell_size // 2)

            # 4. Lógica de Consumo de Pílulas e Pílulas de Poder (Verifica na célula atual)
            # Re-calcula a posição no grid APÓS o movimento de pixel, para pegar a célula para a qual ele acabou de se mover
            current_grid_x_after_move = int(self.pixel_x // self.cell_size)
            current_grid_y_after_move = int(self.pixel_y // self.cell_size)

            # Garante que a posição está dentro dos limites do labirinto (especialmente útil para túneis)
            if 0 <= current_grid_y_after_move < len(game_level) and 0 <= current_grid_x_after_move < len(game_level[0]):
                cell_content_before_consumption = game_level[current_grid_y_after_move][
                    current_grid_x_after_move]  # <--- PEGA O CONTEÚDO ANTES DE MUDAR

                # Se a célula contém uma pílula ou pílula de poder
                if cell_content_before_consumption == 2 or cell_content_before_consumption == 3:
                    # Remove a pílula do labirinto (sempre)
                    game_level[current_grid_y_after_move][current_grid_x_after_move] = 0

                    # Define que uma pílula foi comida neste frame
                    pill_eaten_this_frame = True

                    # Atribui os pontos e o estado de poder
                    if cell_content_before_consumption == 2:  # Se for uma pílula normal
                        points_gained = 10

                    elif cell_content_before_consumption == 3:  # Se for uma pílula de poder
                        self.is_powered_up = True
                        self.power_up_timer = pygame.time.get_ticks()
                        points_gained = POWER_PILL_SCORE
                        print(f"Pac-Man Powered Up! Tempo: {self.power_up_timer}")

            # --- Lógica: Passagem pelo Túnel Lateral ---
            tunnel_row = 15  # A linha do grid onde o túnel está

            # --- DEPURAÇÃO: Verificando condições do túnel (agora ativadas se grid_y for 15) ---
            if self.grid_y == tunnel_row:  # Se Pac-Man está na linha do túnel
                # print(f"Tunnel Check: PacMan na linha {self.grid_y} (esperado {tunnel_row})") # DEPURAÇÃO ADICIONAL
                if self.grid_x == 0 and self.dx < 0:  # Se está na coluna 0 e tentando ir para a esquerda
                    self.pixel_x = float((len(game_level[0]) - 1) * self.cell_size + self.cell_size // 2)
                    self.grid_x = len(game_level[0]) - 1
                    print("TELEPORTE: Esquerda para Direita!")
                elif self.grid_x == len(
                        game_level[0]) - 1 and self.dx > 0:  # Se está na coluna 27 e tentando ir para a direita
                    self.pixel_x = float(0 * self.cell_size + self.cell_size // 2)
                    self.grid_x = 0
                    print("TELEPORTE: Direita para Esquerda!")
            # FIM DA LÓGICA DO TÚNEL

            # 5. Lógica de Animação da Boca
            self.last_moved_direction = (self.dx // self.speed, self.dy // self.speed)  # Normaliza

            if self.mouth_open:
                self.current_mouth_angle -= self.mouth_speed * 2
                if self.current_mouth_angle <= self.closed_mouth_angle:
                    self.mouth_open = False
            else:
                self.current_mouth_angle += self.mouth_speed * 2
                if self.current_mouth_angle >= self.open_mouth_angle:
                    self.mouth_open = True
        else:  # Pac-Man está parado
            if self.current_mouth_angle > self.closed_mouth_angle:
                self.current_mouth_angle -= self.mouth_speed * 2
                if self.current_mouth_angle <= self.closed_mouth_angle:
                    self.current_mouth_angle = self.closed_mouth_angle

        # 6. Atualiza o ângulo de rotação da boca (sempre, mesmo parado)
        if self.last_moved_direction == (1, 0):  # Direita
            self.facing_angle = 0
        elif self.last_moved_direction == (-1, 0):  # Esquerda
            self.facing_angle = 180
        elif self.last_moved_direction == (0, -1):  # Cima
            self.facing_angle = 90
        elif self.last_moved_direction == (0, 1):  # Baixo
            self.facing_angle = 270

        # 7. Gerenciar o temporizador da Pílula de Poder (sempre, mesmo parado)
        was_powered_up = self.is_powered_up
        if self.is_powered_up:
            current_time = pygame.time.get_ticks()
            if current_time - self.power_up_timer > POWER_PILL_DURATION:
                self.is_powered_up = False
                self.power_up_timer = 0
                print("Pac-Man Power-Up Acabou!")

        # 8. Retornar os pontos ganhos
        return points_gained, pill_eaten_this_frame

    def draw(self, screen):
        """Desenha o Pac-Man na tela com animação da boca."""

        # Desenha o Pac-Man como um círculo (corpo)
        pygame.draw.circle(screen, self.color, (int(self.pixel_x), int(self.pixel_y)), self.radius)

        # Desenha o "buraco" da boca como um triângulo preto
        # (Lembrete: 'import math' deve estar no topo do seu arquivo)

        # Ponto 1 (centro do Pac-Man)
        point1 = (int(self.pixel_x), int(self.pixel_y))

        # Ponto 2 (borda superior da boca, ajustada pela direção)
        angle_rad_top = math.radians(self.facing_angle + self.current_mouth_angle)
        point2 = (int(self.pixel_x + self.radius * math.cos(angle_rad_top)),
                  int(self.pixel_y - self.radius * math.sin(angle_rad_top)))  # -sin porque Y cresce para baixo

        # Ponto 3 (borda inferior da boca, ajustada pela direção)
        angle_rad_bottom = math.radians(self.facing_angle - self.current_mouth_angle)
        point3 = (int(self.pixel_x + self.radius * math.cos(angle_rad_bottom)),
                  int(self.pixel_y - self.radius * math.sin(angle_rad_bottom)))  # -sin porque Y cresce para baixo

        # Desenha o triângulo preto que simula a boca aberta
        pygame.draw.polygon(screen, BLACK, [point1, point2, point3])


# --- Classe Ghost ---
class Ghost:
    def __init__(self, name, start_x_grid, start_y_grid, radius, speed, color, cell_size):
        self.name = name

        self.grid_x = start_x_grid
        self.grid_y = start_y_grid
        self.pixel_x = float(self.grid_x * cell_size + cell_size // 2)
        self.pixel_y = float(self.grid_y * cell_size + cell_size // 2)

        self.radius = radius
        self.cell_size = cell_size

        self.speed_normal = speed
        self.speed_frightened = GHOST_SPEED_FRIGHTENED
        self.speed_eaten = GHOST_SPEED_EATEN
        self.current_speed = self.speed_normal

        self.color_normal = color
        self.color_frightened = GHOST_FRIGHTENED_COLOR
        self.color_eaten = GHOST_EATEN_COLOR
        self.current_color = self.color_normal

        self.eaten_respawn_timer = 0

        self.scatter_target = SCATTER_TARGETS[name]
        self.exit_door_target = GHOST_EXIT_TARGET
        self.center_house_target = GHOST_CENTER_HOUSE_TARGET

        self.is_frightened = False
        self.is_eaten = False
        self.is_exiting_house = False
        self.is_entering_house = False
        self.released = False

        self.dx = 0
        self.dy = 0
        self.last_moved_direction = (0, 0)

        if self.name == "blinky":
            self.released = True
            self.grid_x = GHOST_EXIT_TARGET[0]
            self.grid_y = GHOST_EXIT_TARGET[1]  # Blinky começa na GHOST_EXIT_TARGET
            self.pixel_x = float(self.grid_x * cell_size + cell_size // 2)
            self.pixel_y = float(self.grid_y * cell_size + cell_size // 2)
            self.dx = 0  # Blinky pode começar se movendo para cima
            self.dy = -self.speed_normal
            self.last_moved_direction = (0, -1)
            self.is_exiting_house = True  # Blinky já começa no estado de saída
        else:
            self.grid_x = start_x_grid
            self.grid_y = start_y_grid
            self.pixel_x = float(self.grid_x * cell_size + cell_size // 2)
            self.pixel_y = float(self.grid_y * cell_size + cell_size // 2)
            self.dx = 0
            self.dy = 0
            self.last_moved_direction = (0, 0)
            self.is_exiting_house = False

        # print(f"DEBUG_GHOST_INIT_POS: {self.name} - Pos inicial: ({self.grid_x},{self.grid_y}) | is_exiting_house: {self.is_exiting_house} | released: {self.released}")

    def get_grid_pos(self):
        return int(self.pixel_x // self.cell_size), int(self.pixel_y // self.cell_size)

    # --- NOVO: can_move_in_direction com lógica simplificada e robusta ---
    def can_move_in_direction(self, dx_check, dy_check, game_level):
        current_grid_x, current_grid_y = self.get_grid_pos()
        target_grid_x = current_grid_x + dx_check
        target_grid_y = current_grid_y + dy_check

        maze_width = len(game_level[0])
        maze_height = len(game_level)

        # 1. VERIFICAÇÃO DE TÚNEL
        tunnel_row = 15
        if current_grid_y == tunnel_row:
            if (current_grid_x == 0 and dx_check < 0) or \
                    (current_grid_x == maze_width - 1 and dx_check > 0):
                return True

        # 2. VERIFICAÇÃO DE LIMITES GERAIS DO LABIRINTO (NÃO TÚNEL)
        if not (0 <= target_grid_y < maze_height and 0 <= target_grid_x < maze_width):
            return False

        target_cell_type = game_level[target_grid_y][target_grid_x]

        # FANTASMAS COMIDOS (is_eaten=True) IGNORAM PAREDES E PORTAS.
        # Eles não precisam de pathfinding, mas essa regra ainda é logicamente correta.
        if self.is_eaten:
            return True

        # Para fantasmas NÃO COMIDOS:
        # 3. VERIFICAÇÃO DE PAREDES SÓLIDAS (1)
        if target_cell_type == 1:
            return False

        # 4. Lógica da Casa dos Fantasmas (Porta 4 e Interior 0)
        is_current_in_house_area = _is_in_ghost_house_area(current_grid_y, current_grid_x)
        is_target_in_house_area = _is_in_ghost_house_area(target_grid_y, target_grid_x)

        if is_current_in_house_area:
            if not is_target_in_house_area:
                # Permite sair SOMENTE pela porta e para cima
                if current_grid_y == GHOST_HOUSE_DOOR_ROW and target_grid_y == (
                        GHOST_HOUSE_DOOR_ROW - 1) and dy_check < 0:
                    return True
                else:
                    return False
            else:  # Se o alvo também está dentro da casa
                # Não pode atravessar a porta horizontalmente (tipo 4)
                if current_grid_y == GHOST_HOUSE_DOOR_ROW and target_cell_type == 4 and dx_check != 0:
                    return False
                return True
        else:  # Se o fantasma está fora da casa
            if is_target_in_house_area:
                return False
            else:
                return True

        return True  # Fallback

    def update(self, game_level, pacman_instance, current_game_phase):
        """Atualiza a lógica de movimento do fantasma e seu estado visual."""

        # 1. Atualizar cor e velocidade com base no estado
        if self.is_eaten:
            self.current_color = self.color_eaten
            self.current_speed = GHOST_SPEED_EATEN
        elif self.is_frightened:
            self.current_color = self.color_frightened
            self.current_speed = GHOST_SPEED_FRIGHTENED
        else:
            self.current_color = self.color_normal
            self.current_speed = GHOST_SPEED_NORMAL

        # 2. Capturar posição atual no grid (ainda útil para outros estados)
        current_grid_x, current_grid_y = self.get_grid_pos()

        # O alinhamento ao grid ainda é importante para fantasmas que se movem ativamente
        tolerance = self.current_speed / 2
        center_x_of_current_grid = current_grid_x * self.cell_size + self.cell_size // 2
        center_y_of_current_grid = current_grid_y * self.cell_size + self.cell_size // 2

        aligned_x = abs(self.pixel_x - center_x_of_current_grid) <= tolerance
        aligned_y = abs(self.pixel_y - center_y_of_current_grid) <= tolerance

        # A lógica de re-cálculo da direção só ocorre quando o fantasma está alinhado
        # (mas não para fantasmas comidos, que são teleportados)
        if aligned_x and aligned_y and not self.is_eaten:  # Fantasmas comidos NÃO usam essa parte
            self.pixel_x = float(center_x_of_current_grid)
            self.pixel_y = float(center_y_of_current_grid)

            target_x, target_y = None, None
            direction_chosen = False

            # Prioridade 1: Fantasma SAINDO DA CASA (após respawn ou liberação inicial)
            if self.is_exiting_house:
                target_x, target_y = self.exit_door_target
                if (current_grid_x, current_grid_y) == self.exit_door_target:
                    self.is_exiting_house = False
                    self.last_moved_direction = (self.dx // self.current_speed if self.current_speed != 0 else 0,
                                                 self.dy // self.current_speed if self.current_speed != 0 else 0)

            # Prioridade 2: Fantasma ASSUSTADO - movimento de fuga (aleatório)
            elif self.is_frightened:
                possible_frightened_directions = []
                for d_x, d_y in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                    if self.can_move_in_direction(d_x, d_y, game_level):
                        possible_frightened_directions.append((d_x, d_y))

                if possible_frightened_directions:
                    chosen_dx, chosen_dy = random.choice(possible_frightened_directions)
                    self.dx = chosen_dx * self.current_speed
                    self.dy = chosen_dy * self.current_speed
                    self.last_moved_direction = (chosen_dx, chosen_dy)
                else:  # Encurralado
                    self.dx = 0
                    self.dy = 0
                    self.last_moved_direction = (0, 0)
                direction_chosen = True

            # Prioridade 3: Fantasma NÃO LIBERADO (FICAR PARADO DENTRO DA CASA)
            elif not self.released:
                self.dx = 0
                self.dy = 0
                self.last_moved_direction = (0, 0)
                direction_chosen = True

            # Prioridade 4: Fantasma normal (perseguir ou dispersar)
            else:
                if current_game_phase == GHOST_PHASE_SCATTER:
                    target_x, target_y = self.scatter_target
                elif current_game_phase == GHOST_PHASE_CHASE:
                    target_x, target_y = int(pacman_instance.pixel_x // self.cell_size), \
                        int(pacman_instance.pixel_y // self.cell_size)

            # Lógica para escolher a MELHOR direção (greedy)
            if not direction_chosen:
                directions_priority = [(0, -1), (-1, 0), (0, 1), (1, 0)]

                best_direction_found = None
                min_distance = float('inf')

                if target_x is not None and target_y is not None:
                    for d_x, d_y in directions_priority:
                        # Fantasmas normais não podem virar 180 graus.
                        # is_eaten, is_exiting_house e is_entering_house já estão fora desta lógica aqui.
                        if (d_x, d_y) == (-self.last_moved_direction[0], -self.last_moved_direction[1]):
                            continue

                        if self.can_move_in_direction(d_x, d_y, game_level):
                            next_x = current_grid_x + d_x
                            next_y = current_grid_y + d_y

                            distance_sq = (target_x - next_x) ** 2 + (target_y - next_y) ** 2

                            if distance_sq < min_distance:
                                min_distance = distance_sq
                                best_direction_found = (d_x, d_y)

                    if best_direction_found is not None:
                        self.dx = best_direction_found[0] * self.current_speed
                        self.dy = best_direction_found[1] * self.current_speed
                        self.last_moved_direction = best_direction_found
                    else:
                        # Fallback: Se não há outra direção válida, tenta reverter
                        reverse_dir = (-self.last_moved_direction[0], -self.last_moved_direction[1])
                        if self.can_move_in_direction(reverse_dir[0], reverse_dir[1], game_level):
                            self.dx = reverse_dir[0] * self.current_speed
                            self.dy = reverse_dir[1] * self.current_speed
                            self.last_moved_direction = reverse_dir
                        else:  # Completamente preso
                            self.dx = 0
                            self.dy = 0
                            self.last_moved_direction = (0, 0)
                else:  # Se target_x/y é None
                    self.dx = 0
                    self.dy = 0
                    self.last_moved_direction = (0, 0)

        # APLICAR MOVIMENTO OU TELETRANSPORTE SE ESTIVER COMIDO
        if self.is_eaten:
            # Teleporta o fantasma diretamente para o centro da casa
            self.pixel_x = float(self.center_house_target[0] * self.cell_size + self.cell_size // 2)
            self.pixel_y = float(self.center_house_target[1] * self.cell_size + self.cell_size // 2)
            self.dx = 0  # Certifica que ele está parado
            self.dy = 0
            self.last_moved_direction = (0, 0)  # Reseta a direção
            self.grid_x = self.center_house_target[0]  # Atualiza a posição do grid
            self.grid_y = self.center_house_target[1]  # Atualiza a posição do grid

            # Lógica de timer para respawn (já existente e crucial)
            if self.eaten_respawn_timer == 0:
                self.eaten_respawn_timer = pygame.time.get_ticks()

            current_ticks = pygame.time.get_ticks()
            if current_ticks - self.eaten_respawn_timer > GHOST_RESPAWN_DELAY:
                self.is_eaten = False
                self.is_exiting_house = True  # Agora ele quer sair da casa
                self.eaten_respawn_timer = 0
        else:
            # Move normalmente se não estiver comido
            self.pixel_x += self.dx
            self.pixel_y += self.dy
            self.grid_x = int(self.pixel_x // self.cell_size)
            self.grid_y = int(self.pixel_y // self.cell_size)

        # LÓGICA DE TÚNEL: Teletransporte IMEDIATO
        maze_width = len(game_level[0])
        tunnel_row = 15

        if self.grid_y == tunnel_row:
            if self.grid_x < 0:
                self.pixel_x = float((maze_width - 1) * self.cell_size + self.cell_size // 2)
                self.grid_x = maze_width - 1
            elif self.grid_x >= maze_width:
                self.pixel_x = float(0 * self.cell_size + self.cell_size // 2)
                self.grid_x = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.current_color, (int(self.pixel_x), int(self.pixel_y)), self.radius)
        rect_height = int(self.radius * 0.8)
        rect_y = int(self.pixel_y)
        pygame.draw.rect(screen, self.current_color,
                         (int(self.pixel_x - self.radius), rect_y,
                          self.radius * 2, rect_height))

        eye_radius = int(self.radius * 0.2)
        eye_offset = int(self.radius * 0.3)
        pygame.draw.circle(screen, WHITE, (int(self.pixel_x - eye_offset), int(self.pixel_y - eye_offset)), eye_radius)
        pygame.draw.circle(screen, BLACK, (int(self.pixel_x - eye_offset), int(self.pixel_y - eye_offset)),
                           int(eye_radius * 0.5))
        pygame.draw.circle(screen, WHITE, (int(self.pixel_x + eye_offset), int(self.pixel_y - eye_offset)), eye_radius)
        pygame.draw.circle(screen, BLACK, (int(self.pixel_x + eye_offset), int(self.pixel_y - eye_offset)),
                           int(eye_radius * 0.5))

# 5. Inicialização do Pygame
pygame.init()
pygame.font.init()
game_font = pygame.font.Font(None, 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man em Python")
clock = pygame.time.Clock() # Para controlar o FPS

# 6. Criação de Instâncias dos Objetos do Jogo
# Crie seu Pac-Man
pacman = PacMan(14, 22, PACMAN_RADIUS, PACMAN_SPEED, CELL_SIZE)
score = 0
last_score_rendered = -1  # <--- Variável para controlar a renderização do score
game_phase = GHOST_PHASE_SCATTER
last_phase_change_time = pygame.time.get_ticks()

# --- Variáveis de Controle de Lançamento de Fantasmas ---
ghost_release_timer = pygame.time.get_ticks()  # Tempo para controlar o lançamento sequencial
released_ghost_count = 0  # Conta quantos fantasmas já foram lançados (exclui Blinky, que começa lançado)
GHOST_RELEASE_INTERVAL = 3 * 1000  # 3 segundos entre o lançamento de cada fantasma

# --- Variável das Vidas ---
lives = 3  # 3 vidas

#  --- Criação dos Fantasmas ---
ghosts = []
ghosts.append(Ghost("blinky", GHOST_START_POSITIONS["blinky"][0], GHOST_START_POSITIONS["blinky"][1],
                    GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_BLINKY_COLOR, CELL_SIZE))
ghosts.append(Ghost("pinky", GHOST_START_POSITIONS["pinky"][0], GHOST_START_POSITIONS["pinky"][1],
                    GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_PINKY_COLOR, CELL_SIZE))
ghosts.append(Ghost("inky", GHOST_START_POSITIONS["inky"][0], GHOST_START_POSITIONS["inky"][1],
                    GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_INKY_COLOR, CELL_SIZE))
ghosts.append(Ghost("clyde", GHOST_START_POSITIONS["clyde"][0], GHOST_START_POSITIONS["clyde"][1],
                    GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_CLYDE_COLOR, CELL_SIZE))


# --- Lógica de Reinício de Nível ---
def reset_level():
    global level, pills_left, score, pacman, original_level, ghosts, \
        ghost_release_timer, released_ghost_count, game_phase, last_phase_change_time, lives

    # 1. Redefinir o labirinto para o estado original
    level = [row[:] for row in original_level]  # Copia o labirinto original de volta

    # 2. Redefinir a contagem de pílulas
    pills_left = total_pills

    # 3. Redefinir a posição do Pac-Man
    # (Você pode querer uma posição inicial diferente para cada nível ou sempre a mesma)
    pacman.pixel_x = float(14 * CELL_SIZE + CELL_SIZE // 2)  # Posição inicial Pac-Man
    pacman.pixel_y = float(22 * CELL_SIZE + CELL_SIZE // 2)
    pacman.dx = 0
    pacman.dy = 0
    pacman.desired_dx_val = 0
    pacman.desired_dy_val = 0
    pacman.is_powered_up = False
    pacman.power_up_timer = 0
    pacman.mouth_open = True  # Reseta a boca para aberta
    pacman.current_mouth_angle = pacman.open_mouth_angle
    pacman.facing_angle = 0
    pacman.last_moved_direction = (1, 0)

    ghosts.clear()  # Limpa a lista atual de fantasmas
    ghosts.append(Ghost("blinky", GHOST_START_POSITIONS["blinky"][0], GHOST_START_POSITIONS["blinky"][1],
                        GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_BLINKY_COLOR, CELL_SIZE))
    ghosts.append(Ghost("pinky", GHOST_START_POSITIONS["pinky"][0], GHOST_START_POSITIONS["pinky"][1],
                        GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_PINKY_COLOR, CELL_SIZE))
    ghosts.append(Ghost("inky", GHOST_START_POSITIONS["inky"][0], GHOST_START_POSITIONS["inky"][1],
                        GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_INKY_COLOR, CELL_SIZE))
    ghosts.append(Ghost("clyde", GHOST_START_POSITIONS["clyde"][0], GHOST_START_POSITIONS["clyde"][1],
                        GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_CLYDE_COLOR, CELL_SIZE))

    ghost_release_timer = pygame.time.get_ticks()  # Reinicia o timer de lançamento
    released_ghost_count = 0  # Reseta a contagem de fantasmas lançados
    print("Nível Reiniciado! Todas as pílulas consumidas.")


# --- Função para verificar colisão entre Pac-Man e Fantasma ---
def check_collision_pacman_ghost(pacman_instance, ghost_instance):
    # Calcula a distância entre os centros do Pac-Man e do fantasma
    distance_x = pacman_instance.pixel_x - ghost_instance.pixel_x
    distance_y = pacman_instance.pixel_y - ghost_instance.pixel_y
    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    # Colisão ocorre se a distância entre os centros é menor que a soma dos seus raios
    # Subtraia um pouco para uma colisão mais "generosa" ou deixe como soma exata.
    collision_threshold = pacman_instance.radius + ghost_instance.radius - 5  # -5 para ser um pouco mais permissivo

    return distance < collision_threshold

# --- Função para lidar com a morte do Pac-Man ---
def handle_pacman_death():
    global lives, game_over, pacman, ghosts, \
        ghost_release_timer, released_ghost_count, game_phase, last_phase_change_time

    lives -= 1
    print(f"Pac-Man perdeu uma vida! Vidas restantes: {lives}")

    if lives <= 0:
        game_over = True
        print("GAME OVER!")
    else:
        # Reseta Pac-Man para a posição inicial
        pacman.grid_x = 14
        pacman.grid_y = 22
        pacman.pixel_x = float(pacman.grid_x * CELL_SIZE + CELL_SIZE // 2)
        pacman.pixel_y = float(pacman.grid_y * CELL_SIZE + CELL_SIZE // 2)
        pacman.dx = 0
        pacman.dy = 0
        pacman.desired_dx_val = 0
        pacman.desired_dy_val = 0
        pacman.is_powered_up = False  # Perde o power-up ao morrer
        pacman.power_up_timer = 0  # Zera o timer de power-up

        # Recria todos os fantasmas para resetar seus estados
        ghosts.clear()
        ghosts.append(Ghost("blinky", GHOST_START_POSITIONS["blinky"][0], GHOST_START_POSITIONS["blinky"][1],
                            GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_BLINKY_COLOR, CELL_SIZE))
        ghosts.append(Ghost("pinky", GHOST_START_POSITIONS["pinky"][0], GHOST_START_POSITIONS["pinky"][1],
                            GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_PINKY_COLOR, CELL_SIZE))
        ghosts.append(Ghost("inky", GHOST_START_POSITIONS["inky"][0], GHOST_START_POSITIONS["inky"][1],
                            GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_INKY_COLOR, CELL_SIZE))
        ghosts.append(Ghost("clyde", GHOST_START_POSITIONS["clyde"][0], GHOST_START_POSITIONS["clyde"][1],
                            GHOST_RADIUS, GHOST_SPEED_NORMAL, GHOST_CLYDE_COLOR, CELL_SIZE))

        # Reinicia os timers de liberação de fantasmas e a fase do jogo
        ghost_release_timer = pygame.time.get_ticks()
        released_ghost_count = 0
        game_phase = GHOST_PHASE_SCATTER  # Volta para a fase inicial
        last_phase_change_time = pygame.time.get_ticks()


# 7. Loop Principal do Jogo
running = True
game_over = False  # Variável para controlar o estado de Game Over

while running:
    # 7.1. Processamento de Eventos (Entrada do Usuário, Fechar Janela)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Encerra o loop principal

        # Este bloco processa as teclas pressionadas
        if event.type == pygame.KEYDOWN:
            # Lógica para reiniciar o jogo quando é Game Over (prioridade)
            if game_over:
                if event.key == pygame.K_RETURN:  # Verifica se a tecla ENTER foi pressionada
                    game_over = False  # Reseta a flag de Game Over
                    reset_level()  # Chama a função para reiniciar o jogo

            # Lógica para movimento do Pac-Man (só se o jogo NÃO for Game Over)
            else:  # if not game_over
                if event.key == pygame.K_LEFT:
                    pacman.set_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    pacman.set_direction(1, 0)
                elif event.key == pygame.K_UP:
                    pacman.set_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    pacman.set_direction(0, 1)

    # 7.2. Atualização do Estado do Jogo (Lógica do Jogo)
    if not game_over:  # Só atualiza a lógica do jogo se não for Game Over
        points_gained, pill_eaten_this_frame = pacman.update(level)

        if points_gained > 0:
            score += points_gained

        if pill_eaten_this_frame:
            pills_left -= 1

        # Verifica Condição de Reinício do Nível (se todas as pílulas foram comidas)
        if pills_left <= 0:
            print("Nível Concluído!")
            reset_level()

        # --- Lógica de Lançamento Sequencial de Fantasmas ---
        current_time = pygame.time.get_ticks()

        if (current_time - ghost_release_timer) > GHOST_RELEASE_INTERVAL:
            if released_ghost_count == 0:
                for ghost in ghosts:
                    if ghost.name == "pinky" and not ghost.released:
                        ghost.released = True
                        ghost.is_exiting_house = True
                        ghost_release_timer = current_time
                        released_ghost_count += 1
                        print(f"DEBUG: Fantasma {ghost.name} foi liberado e está saindo!")
                        break
            elif released_ghost_count == 1:
                for ghost in ghosts:
                    if ghost.name == "inky" and not ghost.released:
                        ghost.released = True
                        ghost.is_exiting_house = True
                        ghost_release_timer = current_time
                        released_ghost_count += 1
                        print(f"DEBUG: Fantasma {ghost.name} foi liberado e está saindo!")
                        break
            elif released_ghost_count == 2:
                for ghost in ghosts:
                    if ghost.name == "clyde" and not ghost.released:
                        ghost.released = True
                        ghost.is_exiting_house = True
                        ghost_release_timer = current_time
                        released_ghost_count += 1
                        print(f"DEBUG: Fantasma {ghost.name} foi liberado e está saindo!")
                        break

        for ghost in ghosts:
            if ghost.released or ghost.is_eaten:
                ghost.update(level, pacman, game_phase)

        # --- Verificar Colisões Pac-Man vs Fantasmas (Lógica ATUALIZADA para Vidas) ---
        for ghost in ghosts:
            if check_collision_pacman_ghost(pacman, ghost):
                if ghost.is_frightened and not ghost.is_eaten:
                    ghost.is_eaten = True
                    score += GHOST_EATEN_SCORE
                    print(f"Fantasma {ghost.name} comido! Pontuação: {score}")

                elif not ghost.is_frightened and not ghost.is_eaten:
                    # Chamada para a nova função que lida com a morte do Pac-Man
                    handle_pacman_death()
                    break  # Importante para sair do loop de fantasmas após uma colisão fatal

        # --- Gerenciar Status dos Fantasmas (Ciclo Scatter/Chase) ---
        current_time = pygame.time.get_ticks()

        if not pacman.is_powered_up:
            if game_phase == GHOST_PHASE_SCATTER and (current_time - last_phase_change_time > SCATTER_PHASE_DURATION):
                game_phase = GHOST_PHASE_CHASE
                last_phase_change_time = current_time
                print(f"DEBUG: Fase alterada para CHASE! Tempo: {current_time}")
            elif game_phase == GHOST_PHASE_CHASE and (current_time - last_phase_change_time > CHASE_PHASE_DURATION):
                game_phase = GHOST_PHASE_SCATTER
                last_phase_change_time = current_time
                print(f"DEBUG: Fase alterada para SCATTER! Tempo: {current_time}")
        else:
            last_phase_change_time = current_time

        for ghost in ghosts:
            old_frightened_state = ghost.is_frightened

            if pacman.is_powered_up and not ghost.is_eaten:
                if not ghost.is_frightened:
                    ghost.is_frightened = True
                    ghost.current_speed = GHOST_SPEED_FRIGHTENED
                    ghost.dx *= -1
                    ghost.dy *= -1
                    ghost.last_moved_direction = (ghost.dx // ghost.current_speed if ghost.current_speed != 0 else 0,
                                                  ghost.dy // ghost.current_speed if ghost.current_speed != 0 else 0)
                    print(
                        f"DEBUG_FRIGHTEN: Fantasma {ghost.name} ficou assustado e inverteu a direção! (Old is_frightened: {old_frightened_state})")
            elif not pacman.is_powered_up:
                if ghost.is_frightened:
                    ghost.is_frightened = False
                    ghost.current_speed = GHOST_SPEED_NORMAL
                    print(
                        f"DEBUG_FRIGHTEN: Fantasma {ghost.name} deixou de estar assustado! (Old is_frightened: {old_frightened_state})")

    # 7.3. Desenho na Tela (esta parte permanece a mesma)
    screen.fill(BLACK)

    for row_index, row in enumerate(level):
        for col_index, cell in enumerate(row):
            x = col_index * CELL_SIZE
            y = row_index * CELL_SIZE

            center_x = x + CELL_SIZE // 2
            center_y = y + CELL_SIZE // 2

            if cell == 1:
                current_wall_color = BLUE
                if row_index > 0 and level[row_index - 1][col_index] != 1:
                    pygame.draw.line(screen, current_wall_color,
                                     (x, y + WALL_LINE_THICKNESS // 2),
                                     (x + CELL_SIZE, y + WALL_LINE_THICKNESS // 2),
                                     WALL_LINE_THICKNESS)
                if row_index < len(level) - 1 and level[row_index + 1][col_index] != 1:
                    pygame.draw.line(screen, current_wall_color,
                                     (x, y + CELL_SIZE - WALL_LINE_THICKNESS // 2),
                                     (x + CELL_SIZE, y + CELL_SIZE - WALL_LINE_THICKNESS // 2),
                                     WALL_LINE_THICKNESS)
                if col_index < len(row) - 1 and level[row_index][col_index + 1] == 1:
                    pygame.draw.line(screen, current_wall_color,
                                     (center_x, center_y),
                                     (center_x + CELL_SIZE, center_y),
                                     WALL_LINE_THICKNESS)
                if col_index > 0 and level[row_index][col_index - 1] != 1:
                    pygame.draw.line(screen, current_wall_color,
                                     (x + WALL_LINE_THICKNESS // 2, y),
                                     (x + WALL_LINE_THICKNESS // 2, y + CELL_SIZE),
                                     WALL_LINE_THICKNESS)
                if col_index < len(row) - 1 and level[row_index][col_index + 1] != 1:
                    pygame.draw.line(screen, current_wall_color,
                                     (x + CELL_SIZE - WALL_LINE_THICKNESS // 2, y),
                                     (x + CELL_SIZE - WALL_LINE_THICKNESS // 2, y + CELL_SIZE),
                                     WALL_LINE_THICKNESS)
                if row_index < len(level) - 1 and level[row_index + 1][col_index] == 1:
                    pygame.draw.line(screen, current_wall_color,
                                     (center_x, center_y),
                                     (center_x, center_y + CELL_SIZE),
                                     WALL_LINE_THICKNESS)
                pygame.draw.circle(screen, current_wall_color, (center_x, center_y), WALL_LINE_THICKNESS // 2)
            elif cell == 2:
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)
            elif cell == 3:
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2)
            elif cell == 4:
                pygame.draw.rect(screen, (100, 100, 100), (x, y + CELL_SIZE // 2 - 2, CELL_SIZE, 4))

    if not game_over:
        pacman.draw(screen)

    for ghost in ghosts:
        ghost.draw(screen)

    score_text = game_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (5, SCREEN_HEIGHT - 30))

    lives_text = game_font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30))

    if game_over:
        game_over_font = pygame.font.Font(None, 48)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        restart_text = game_over_font.render("Pressione ENTER para jogar novamente", True, WHITE)

        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(game_over_text, text_rect)

        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(60)

# 8. Finalização do Pygame (Após o Loop Principal)
pygame.quit()
