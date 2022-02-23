import dataclasses

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
    def from_count(cls, count: int):
        if count >= 9:
            return cls(
                count=0,
                message="You've made it! ICE CREAM TIME, BABY!"
            )
        return cls(
            count=count + 1,
            message=""
        )

@app.get("/")
def get_count():
    return render_template("index.html", count=repo.fetch_count())


@app.post("/")
def update_count():
    ctx = Context.from_count(repo.fetch_count())
    repo.update_count(ctx.count)
    return render_template("index.html", **dataclasses.asdict(ctx))


if __name__ == "__main__":
    app.run(debug=True)
