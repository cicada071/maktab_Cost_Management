from fastapi import FastAPI, HTTPException, status
import uvicorn

from app.schemas import request_models, response_models

app = FastAPI(title="Cont Managment App")

db = dict()

#Create cost
@app.post("/costs",
          status_code=status.HTTP_201_CREATED,
          response_model=response_models.ContResponse)
def create_cost(cont:request_models.ContCreate):
    key = next(reversed(db))+1 if db else 1
    db[key] = {"description":cont.description, "amount":cont.amount}
    return {"message":"The list of costs has been received.",
            "data":db}

#Read cost
@app.get("/costs",
         response_model=response_models.ContResponse)
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

#Search cost
@app.get("/costs/search",
         response_model=response_models.ContResponse)
def search_costs(
    cost_id: int|None=None,
    description: str|None=None,
    amount: float|None=None
):
    results = {}

    for key, value in db.items():

        if cost_id is not None and str(cost_id) not in str(key):
            continue

        if description is not None:
            if description.lower() not in (value["description"] or "").lower():
                continue

        if amount is not None and abs(value["amount"] - amount) > 200000:
            continue

        results[key] = value

    return {
        "message": "Search completed successfully.",
        "data": results
    }

#Update cost
@app.patch("/costs/{cost_id}")
def update_cost(cost_id: int,
                cont: request_models.ContUpdate):

    if not db.get(cost_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cost not found!")

    values = cont.model_dump(exclude_unset=True)
    if not values:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="cost not found!")

    db[cost_id].update(values)
    return {"message":"Successfully updated.",
            "data":db[cost_id]}

#Delete cost
@app.delete("/costs/{cost_id}",
            response_model=response_models.BaseResponse)
def delete_cost(cost_id: int):
    if not db.get(cost_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cost not found!")

    db.pop(cost_id)
    return {"message":"Successfully deleted."}














if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True )