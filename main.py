from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# ------------------ DATABASE ------------------

users = []
movies = []
tickets = []

user_id_counter = 1
movie_id_counter = 1
ticket_id_counter = 1


# ------------------ MODELS ------------------

class User(BaseModel):
    name: str = Field(min_length=2)
    email: str


class Movie(BaseModel):
    title: str
    price: int
    total_seats: int


class Ticket(BaseModel):
    user_id: int
    movie_id: int
    seats: int


# ------------------ USERS ------------------

@app.post("/users/register")
def register_user(user: User):
    global user_id_counter

    new_user = user.dict()
    new_user["id"] = user_id_counter

    users.append(new_user)
    user_id_counter += 1

    return {"message": "User registered", "user": new_user}


@app.get("/users")
def get_users():
    return users


@app.get("/users/{id}")
def get_user(id: int):
    for u in users:
        if u["id"] == id:
            return u
    return {"error": "User not found"}


@app.delete("/users/{id}")
def delete_user(id: int):
    for u in users:
        if u["id"] == id:
            users.remove(u)
            return {"message": "User deleted"}
    return {"error": "User not found"}


# ------------------ MOVIES ------------------

@app.post("/movies/add")
def add_movie(movie: Movie):
    global movie_id_counter

    new_movie = movie.dict()
    new_movie["id"] = movie_id_counter
    new_movie["available_seats"] = movie.total_seats

    movies.append(new_movie)
    movie_id_counter += 1

    return {"message": "Movie added", "movie": new_movie}


@app.get("/movies")
def get_movies():
    return movies


# ------------------ SEARCH ------------------

@app.get("/movies/search")
def search_movie(keyword: str):
    result = [m for m in movies if keyword.lower() in m["title"].lower()]

    if not result:
        return {"message": "No movies found"}

    return result


# ------------------ SORT ------------------

@app.get("/movies/sort")
def sort_movies(order: str = "asc"):
    sorted_movies = sorted(
        movies,
        key=lambda x: x["price"],
        reverse=(order == "desc")
    )
    return sorted_movies


# ------------------ PAGINATION ------------------

@app.get("/movies/page")
def paginate_movies(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "movies": movies[start:end]
    }


# ------------------ AVAILABILITY ------------------

@app.get("/movies/{id}/availability")
def check_availability(id: int):
    for m in movies:
        if m["id"] == id:
            return {"available_seats": m["available_seats"]}
    return {"error": "Movie not found"}


# ------------------ UPDATE MOVIE ------------------

@app.put("/movies/update/{id}")
def update_movie(id: int, movie: Movie):
    for m in movies:
        if m["id"] == id:
            m.update(movie.dict())
            return {"message": "Movie updated", "movie": m}
    return {"error": "Movie not found"}


# ------------------ DELETE MOVIE ------------------

@app.delete("/movies/delete/{id}")
def delete_movie(id: int):
    for m in movies:
        if m["id"] == id:
            movies.remove(m)
            return {"message": "Movie deleted"}
    return {"error": "Movie not found"}


# ------------------ GET MOVIE BY ID (IMPORTANT: LAST) ------------------

@app.get("/movies/{id}")
def get_movie(id: int):
    for m in movies:
        if m["id"] == id:
            return m
    return {"error": "Movie not found"}


# ------------------ BOOK TICKET ------------------


@app.post("/tickets/book")
def book_ticket(ticket: Ticket):
    global ticket_id_counter

    for m in movies:
        if m["id"] == ticket.movie_id:

            if m["available_seats"] < ticket.seats:
                return {"error": "Not enough seats available"}

            m["available_seats"] -= ticket.seats

            new_ticket = ticket.dict()
            new_ticket["id"] = ticket_id_counter
            new_ticket["status"] = "pending"

            tickets.append(new_ticket)
            ticket_id_counter += 1

            return {"message": "Ticket booked", "ticket": new_ticket}

    return {"error": "Movie not found"}


@app.get("/tickets")
def get_tickets():
    return tickets

@app.get("/tickets/page")
def paginate_tickets(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit
    return tickets[start:end]


@app.get("/tickets/{id}")
def get_ticket(id: int):
    for t in tickets:
        if t["id"] == id:
            return t
    return {"error": "Ticket not found"}


@app.patch("/tickets/confirm/{id}")
def confirm_ticket(id: int):
    for t in tickets:
        if t["id"] == id:
            t["status"] = "confirmed"
            return {"message": "Ticket confirmed", "ticket": t}
    return {"error": "Ticket not found"}


@app.delete("/tickets/cancel/{id}")
def cancel_ticket(id: int):
    for t in tickets:
        if t["id"] == id:
            tickets.remove(t)
            return {"message": "Ticket cancelled"}
    return {"error": "Ticket not found"}


# ------------------ DASHBOARD ------------------

@app.get("/dashboard")
def dashboard():
    return {
        "total_users": len(users),
        "total_movies": len(movies),
        "total_tickets": len(tickets)
    }


# ------------------ BONUS PAGINATION ------------------

@app.get("/tickets/page")
def paginate_tickets(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit

    return tickets[start:end]