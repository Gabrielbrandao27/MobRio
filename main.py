from fastapi import FastAPI

app = FastAPI()


@app.get("/{item_id}")
async def test_func(item_id: str):
    return {"message": {item_id}}