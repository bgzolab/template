from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import uvicorn
import os
from bangumi_data.data import get_data_by_year_month

app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

@app.get("/")
def index():
    return FileResponse("web/static/index.html")

@app.get("/api/data")
def get_data(year: int, month: int):
    # 获取 bangumi-data 数据，假设有 get_data_by_year_month 方法
    data = get_data_by_year_month(year, month)
    return JSONResponse(content={"data": data})

@app.post("/api/batch")
async def batch_process(request: Request):
    body = await request.json()
    ids: List[int] = body.get("ids", [])
    # 这里可以做统一处理，比如返回处理结果
    result = {"processed": ids, "count": len(ids)}
    return JSONResponse(content=result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
