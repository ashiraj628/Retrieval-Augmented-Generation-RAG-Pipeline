import dramatiq
from dramatiq.brokers.redis import RedisBroker

broker = RedisBroker()

dramatiq.set_broker(broker)