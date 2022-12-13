import blackjack_env as bj1
from blackjack_env import draw_card, is_bust, sum_hand, score, cmp

# Fuente: https://zoo.cs.yale.edu/classes/cs470/materials/hws/aima/gym/gym/envs/toy_text/blackjack.py
def is_natural(hand):
    """
    Devuelve si tiene un natural de mano 
    """
    return sorted(hand) == [1, 10]

class BlackjackEnv(bj1.BlackjackEnv):
    def __init__(self, natural=False):
        self.natural = natural # Apartado 1.2: añadir el caso de tener un natural y cambiar su recompensa por 1.5
        super().__init__()

    def _step(self, action):
        """
        Evalúa los pasos y asigna una recompensa
        """
        assert self.action_space.contains(action), f"Fallo, Action = {action}"
        if action:  # Action es 1 pide una carta más
            self.player.append(draw_card(self.np_random))
            if is_bust(self.player):
                done = True
                reward = -1
            else:
                done = False
                reward = 0
        else:  # Si por el contrario action es 0, es que se para
            done = True
            while sum_hand(self.dealer) < 17:
                self.dealer.append(draw_card(self.np_random))
            reward = cmp(score(self.player), score(self.dealer))
            if is_natural(self.player) and not is_natural(self.dealer) and reward == 1.0:
                reward = 1.5
        return self._get_obs(), reward, done, {}