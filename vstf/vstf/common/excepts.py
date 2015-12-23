class ChannelDie(Exception):
    """rabbitmq's channel connect failed"""
    pass


class UnsolvableExit(Exception):
    """the soft maybe error , and the code can not solvable, must be exit"""
    pass


class AgentExit(Exception):
    pass
