import gym
from gym import spaces
from gym.utils import seeding

def cmp(a, b):
    """
    Devuelve quién tiene más puntaje al finalizar la partida:
    ->  1: gana jugador
    ->  0: empate
    -> -1: gana crupier
    """
    return int((a > b)) - int((a < b))

# 1 = Ace, 2-10 = Number cards, Jack/Queen/King = 10
deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def draw_card(np_random):
    """
    Asigna una carta disponible
    """
    return np_random.choice(deck)


def draw_hand(np_random):
    """
    Reparte una carta
    """
    return [draw_card(np_random), draw_card(np_random)]


def usable_ace(hand):
    """
    Devuelve si tiene un as utilizable o no.
    Si el total de cartas supera los 21, entonces el as deberá valer 1
    """   
    return 1 in hand and sum(hand) + 10 <= 21


def sum_hand(hand):
    """
    Devuelve el valor total de la mano actual
    """
    if usable_ace(hand):
        return sum(hand) + 10
    return sum(hand)


def is_bust(hand):
    """
    Devuelve si la mano actual está perdida por pasarse de 21
    """
    return sum_hand(hand) > 21


def score(hand): 
    """
    Devuelve el puntaje final de la mano actual, o 0 en caso de estar perdida
    """
    return 0 if is_bust(hand) else sum_hand(hand)


class BlackjackEnv(gym.Env):
    """
    Clase que define el entorno del juego Bakckjack
    """

    def __init__(self):
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Tuple((
            spaces.Discrete(32),
            spaces.Discrete(11),
            spaces.Discrete(2)))
        self._seed()
        self._reset()

    def reset(self):
        return self._reset()

    def step(self, action):
        return self._step(action)

    def _seed(self, seed=None):
        """
        Devuelve un número aleatorio
        """
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        """
        Evalúa los pasos y asigna una recompensa
        """
        assert self.action_space.contains(action), "Fallo, Action = {}".format(action)
        if action:  # Action es 0 si pide carta o 1 si se para, y en este último caso evalúa el resultado y asigna la recompensa
            self.player.append(draw_card(self.np_random))
            if is_bust(self.player):
                done = True
                reward = -1
            else:
                done = False
                reward = 0
        else:  # Si por el contrario action es 0, es que pide una carta más
            done = True
            while sum_hand(self.dealer) < 17:
                self.dealer.append(draw_card(self.np_random))
            reward = cmp(score(self.player), score(self.dealer))
        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        """
        Devuelve una tupla de 3 elementos: 
        - la suma actual del jugador, 
        - la carta que muestra el crupier con valores 1-10, donde 1 es un as, y 
        - si el jugador tiene o no un as utilizable
        """
        return (sum_hand(self.player), self.dealer[0], usable_ace(self.player))

    def _reset(self):
        """
        Reinicia la partida
        """
        self.dealer = draw_hand(self.np_random)
        self.player = draw_hand(self.np_random)
        
        while sum_hand(self.player) < 12:
            self.player.append(draw_card(self.np_random))

        return self._get_obs()