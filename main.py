import dataclasses
import os
from datetime import datetime
from distutils.util import strtobool

from flask import Flask, render_template
import sqlite3

import repository

app = Flask("reward_counter")


@dataclasses.dataclass
class Context:
    message: str
    count: int

    @classmethod
    def from_count(cls, count: repository.Count):
        if count.updated_ts == datetime.utcnow().strftime("%Y-%m-%d"):
            return cls(
                count=count.count,
                message="You can only increment this once a day, silly."
            )
        if count.count >= 9:
            return cls(
                count=0,
                message="You've made it! ICE CREAM TIME, BABY!"
            )
        return cls(
            count=count.count + 1,
            message="Keep Going!"
        )


@app.get("/")
def get_count():
    return render_template("index.html", count=repo.fetch_count().count)


@app.post("/")
def update_count():
    ctx = Context.from_count(repo.fetch_count())
    repo.update_count(ctx.count)
    return render_template("index.html", **dataclasses.asdict(ctx))


if __name__ == "__main__":
    repo = repository.CountRepository(lambda: sqlite3.connect("rewardCount.db"))
    app.run(debug=strtobool(os.environ.get("DEBUG", "False")))
