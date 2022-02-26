import dataclasses
import os
from datetime import datetime
from distutils.util import strtobool

from flask import Flask, render_template
import sqlite3

import repository

app = Flask("reward_counter")
repo = repository.CountRepository(lambda: sqlite3.connect("rewardCount.db"))


@dataclasses.dataclass
class Context:
    message: str
    count: int

    @classmethod
    def from_count(cls, count: repository.Count):
        if count.updated_date >= datetime.utcnow().date():
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


@app.get("/dad-jokes")
def get_dad_jokes():
    return render_template("dadjokes.html")

@app.get("/insults")
def get_insults():
    return render_template("insults.html")

@app.get("/")
def index():
    return get_count()


@app.get("/car-ride-rewards")
def get_count():
    return render_template("index.html", count=repo.fetch_count().count)


@app.post("/car-ride-rewards")
def update_count():
    ctx = Context.from_count(repo.fetch_count())
    repo.update_count(ctx.count)
    return render_template("index.html", **dataclasses.asdict(ctx))

@app.get("/games/pigs")
def et_pigs():
    return render_template("pigs.html")


if __name__ == "__main__":
    app.run(debug=strtobool(os.environ.get("DEBUG", "False")))
