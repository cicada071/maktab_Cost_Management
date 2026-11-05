from fastapi import FastAPI, HTTPException, status, Body
import uvicorn

app = FastAPI(title="Cont Managment App")

db = dict()

#Create cost
@app.post("/costs/create/",
          status_code=status.HTTP_201_CREATED)
def create_cost(description: str|None=Body(default=None),
                amount: float=Body()):
    key = next(reversed(db))+1 if db else 1
    db[key] = {"description":description, "amount":amount}
    return {"message":"The list of costs has been received.",
            "data":db}

#Read cost
@app.get("/costs/")
def read_costs(cost_id: int|None=None):
    if cost_id:
        cost = db.get(cost_id)
        if not cost:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="cost not found!")
        return {"message":"Cost found.",
                "data":cost}
    return {"message":"The list of costs has been received.",
            "data":db}

#Update cost
@app.put("/costs/{cost_id}/update/")
def update_cost(cost_id: int,
                description: str|None=Body(default=None),
                amount: float=Body()):
    if not db.get(cost_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cost not found!")

    db[cost_id] =  {"description":description, "amount":amount}
    return {"message":"Successfully updated.",
            "data":db[cost_id]}

#Delete cost
@app.delete("/costs/{cost_id}/delete/")
def delete_cost(cost_id: int):
    if not db.get(cost_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cost not found!")

    db.pop(cost_id)
    return {"message":"Successfully deleted."}














if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True )