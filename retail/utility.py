from rlpyt.utils.quick_args import save__init__args
import torch
import torch.nn.functional as F

class LinearUtility:

    def __init__(
        self,
        alpha,
        beta,
        gamma,
    ):
        save__init__args(locals(), underscore=True)

    def reward(
        self,
        sales,
        waste,
        availability,
    ):
        return sales * self._alpha - waste * self._beta + availability \
            * self._gamma


class CobbDouglasUtility:

    def __init__(
        self,
        alpha,
        beta,
        gamma,
    ):
        save__init__args(locals(), underscore=True)

    def reward(
        self,
        sales,
        waste,
        availability,
    ):
        return F.relu(sales) ** self._alpha * (1 + waste) ** -self._beta \
            * availability ** self._gamma


class LogLinearUtility:

    def __init__(
        self,
        alpha,
        beta,
        gamma,
    ):
        save__init__args(locals(), underscore=True)

    def reward(
        self,
        sales,
        waste,
        availability,
    ):
        return torch.log(1 + F.relu(sales)) * self._alpha - torch.log(1
                                                              + waste) * self._beta + torch.log(1 + availability) \
            * self._gamma


class HomogeneousReward:

    def __init__(
        self,
        alpha,
        beta,
        gamma,
    ):
        save__init__args(locals(), underscore=True)

    def reward(
        self,
        sales,
        waste,
        availability,
    ):
        return (availability ** self._gamma * (sales - waste)).squeeze()


class CustomUtility:

    def __init__(self, utility):
        self.txt = utility

    def reward(self, s, w, a):
        return eval(self.txt)
