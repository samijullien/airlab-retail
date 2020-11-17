from rlpyt.samplers.collections import TrajInfo


class RetailTrajInfo(TrajInfo):

    def __init__(self, momentum=.05, **kwargs):
        super().__init__(**kwargs)
        self.AverageReward = 0
        self.Sales = 0
        self.Availability = 0
        self.Waste = 0
        self.Momentum = momentum

    def step(
        self,
        observation,
        action,
        reward,
        done,
        agent_info,
        env_info,
    ):
        super().step(
            observation,
            action,
            reward,
            done,
            agent_info,
            env_info,
        )
        self.AverageReward = self.Momentum * reward + (1
                                                       - self.Momentum) * self.AverageSales
        self.Sales = self.Momentum * getattr(env_info, 'sales', 0) + (1
                                                                      - self.Momentum) * self.AverageSales
        self.Availability = self.Momentum * getattr(env_info,
                                                    'availability', 0) + (1 - self.Momentum) \
            * self.Availability
        self.Waste = self.Momentum * getattr(env_info, 'waste', 0) + (1
                                                                      - self.Momentum) * self.Waste
