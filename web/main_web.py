from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import uvicorn
import os

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
    # 这里可以做统一处理，比如返回处理结果

    for id in ids:
        response = mark_subject(id, CollectionType.DONE.value)
        print("process id = {}, response = {}", id, response)

    result = {"processed": ids, "count": len(ids)}
    return JSONResponse(content=result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
