# flake8: noqa
from textwrap import dedent
from ward import test

from turbo_chat import *


@test("contains returns True when summarize_bot works")
async def test_summarize_bot():
    text = dedent(
        """
    Monty Python (also collectively known as the Pythons)
     were a British comedy troupe formed in 1969 and consisting of
     Graham Chapman, John Cleese, Terry Gilliam, Eric Idle, Terry Jones,
     and Michael Palin. The group came to prominence for creating and
     performing the sketch comedy series Monty Python's Flying Circus (1969–1974).
     Their work then evolved from the series into a larger and more influential
     collection that included live shows, films, albums, books, and musicals;
     their influence on comedy has been compared to the Beatles' influence on music.
     Regarded as an enduring icon of 1970s pop culture, their sketch show has been
     referred to as being "an important moment in the evolution of television comedy".
    """.strip()
    )

    summary = await run(summarize_bot(text=text))

    assert 0 < len(summary.content) < len(text)
