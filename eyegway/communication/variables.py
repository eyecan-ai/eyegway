from redis import Redis
import typing as t
import pickle


class SharedVariable:
    def __init__(
        self,
        redis: Redis,
        name: str,
    ):
        self.redis = redis
        self.variable_name = name

    def set(self, value: t.Any):
        self.redis.set(self.variable_name, pickle.dumps(value))

    def get(self) -> t.Optional[t.Any]:
        output = self.redis.get(self.variable_name)
        if output is None:
            return None
        return pickle.loads(output)

    def delete(self):
        print("DELETEING", self.variable_name)
        self.redis.delete(self.variable_name)
