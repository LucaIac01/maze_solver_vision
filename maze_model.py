import gym
from gym import spaces
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
import matplotlib.pyplot as plt
import os
from PIL import Image


# Funzione per caricare le immagini dei labirinti da una cartella
def load_mazes_from_folder(folder_path):
    maze_images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            # Carica l'immagine
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path).convert('RGB')
            img_array = np.array(img)
            maze_images.append(img_array)
    return maze_images


# Classe per l'ambiente del labirinto
class MazeEnv(gym.Env):
    def __init__(self, maze_images):
        super(MazeEnv, self).__init__()
        self.maze_images = maze_images  # Lista di immagini di labirinti
        self.current_maze = None
        self.start_position = None
        self.exit_position = None
        self.agent_position = None

        # Spazio delle azioni: 4 direzioni (su, giù, sinistra, destra)
        self.action_space = spaces.Discrete(4)

        # Spazio degli stati: posizione dell'agente (x, y)
        max_height = max(img.shape[0] for img in maze_images)
        max_width = max(img.shape[1] for img in maze_images)
        self.observation_space = spaces.Box(low=0, high=np.array([max_height, max_width]), dtype=np.int32)

        # Inizializza il seed
        self.seed()

    def seed(self, seed=None):
        """
        Imposta il seed per la generazione di numeri casuali.
        """
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def reset(self):
        # Seleziona un labirinto casuale
        self.current_maze = self.maze_images[np.random.randint(len(self.maze_images))]
        self.start_position, self.exit_position = self._find_start_and_exit()
        self.agent_position = self.start_position
        return np.array(self.agent_position)

    def step(self, action):
        # Aggiorna la posizione dell'agente in base all'azione
        x, y = self.agent_position
        if action == 0:  # Su
            x -= 1
        elif action == 1:  # Giù
            x += 1
        elif action == 2:  # Sinistra
            y -= 1
        elif action == 3:  # Destra
            y += 1

        # Controlla se la nuova posizione è valida
        if self._is_valid_position(x, y):
            self.agent_position = (x, y)

        # Calcola la ricompensa
        reward = -0.01  # Penalità per ogni mossa
        done = False
        if self.agent_position == self.exit_position:
            reward = 1  # Ricompensa per aver raggiunto l'uscita
            done = True
        elif not self._is_valid_position(x, y):
            reward = -1  # Penalità per aver colpito un muro

        return np.array(self.agent_position), reward, done, {}

    def _find_start_and_exit(self):
        # Trova il punto di partenza (quadrato rosso) e l'uscita (linea rossa)
        red = np.array([255, 0, 0])
        start_position = None
        exit_position = None
        for i in range(self.current_maze.shape[0]):
            for j in range(self.current_maze.shape[1]):
                if np.array_equal(self.current_maze[i, j], red):
                    if start_position is None:
                        start_position = (i, j)
                    else:
                        exit_position = (i, j)
        return start_position, exit_position

    def _is_valid_position(self, x, y):
        # Controlla se la posizione è all'interno del labirinto e non è un muro
        if 0 <= x < self.current_maze.shape[0] and 0 <= y < self.current_maze.shape[1]:
            return not np.array_equal(self.current_maze[x, y], [0, 0, 0])  # Muro nero
        return False

    def render(self, mode='human'):
        # Visualizza il labirinto e la posizione corrente dell'agente
        img = self.current_maze.copy()
        x, y = self.agent_position
        img[x, y] = [0, 255, 0]  # Agente rappresentato in verde
        plt.imshow(img)
        plt.axis('off')
        #plt.show()


# Caricamento delle immagini dei labirinti
maze_folder = "./maze_set"  # Assicurati che questa cartella contenga le tue immagini
maze_images = load_mazes_from_folder(maze_folder)
print(f"Trovate {len(maze_images)} immagini di labirinti.")

# Creazione dell'ambiente
env = MazeEnv(maze_images)

# Crea un ambiente vettoriale per accelerare l'addestramento
vec_env = make_vec_env(lambda: env, n_envs=1)

# Crea il modello DQN
model = DQN("MlpPolicy", vec_env, verbose=1)

# Addestra il modello
print("Inizio dell'addestramento...")
model.learn(total_timesteps=50000)
print("Addestramento completato!")

# Salva il modello
model.save("maze_solver")

# Test del modello su un nuovo labirinto
print("Test del modello...")
obs = env.reset()
done = False
while not done:
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()  # Visualizza l'ambiente