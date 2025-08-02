from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import uvicorn
import os
from concurrent.futures import ThreadPoolExecutor

from bangumi.enum import CollectionType
from bangumi_data.data import get_data_by_year_month
from bangumi.collection import mark_subject

app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

@app.get("/")
def index():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    return FileResponse(index_path)

@app.get("/api/data")
def get_data(year: int, month: int):
    data = get_data_by_year_month(year, month)
    # dataclass对象转为dict
    serializable_data = [bd.__dict__ | {"sites": [site.__dict__ for site in bd.sites]} for bd in data]
    return JSONResponse(content={"data": serializable_data})

@app.post("/api/batch")
async def batch_process(request: Request):
    body = await request.json()
    ids: List[int] = body.get("ids", [])
    type_str = body.get("type", str(CollectionType.DONE.value))
    def process_one(id):
        response = mark_subject(id, int(type_str))
        print(f"process id = {id}, type = {type_str}, response = {response}")
        return response
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_one, ids))
    result = {"processed": ids, "count": len(ids)}
    return JSONResponse(content=result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
