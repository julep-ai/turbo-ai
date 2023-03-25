from typing import Optional, Union

from peak.util.proxies import ObjectWrapper


class TurboGenWrapper(ObjectWrapper):
    g = None

    def __init__(self, g):
        ObjectWrapper.__init__(self, g)
        self.g = g

    def __aiter__(self):
        return self.g.__aiter__()

    async def run(
        self,
        input: Optional[Union[str, dict]] = None,
    ):
        # To avoid circular import
        from ..runner import run as gen_run

        return await gen_run(self, input)


def proxy_turbo_gen_fn(turbo_gen_fn):
    def wrapped_fn(*args, **kwargs):
        gen = turbo_gen_fn(*args, **kwargs)
        proxy = TurboGenWrapper(gen)

        return proxy

    return wrapped_fn
