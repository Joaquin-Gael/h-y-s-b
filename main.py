from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

from pathlib import Path

app = FastAPI()

class SPAStaticFiles(StaticFiles):
    def __init__(self):
        super().__init__(directory=Path(__file__).parent / "dist/browser", html=True, check_dir=True)
        self._index_file = "home/index.html"

        self.app = super().__call__

    async def __call__(self, scope, receive, send):
        assert scope["type"] == "http"

        request = Request(scope, receive)

        path = request.url.path.lstrip("/")
        print(path)

        full_path = (Path(self.directory) / path).resolve()
        if full_path.exists():
            await self.app(scope, receive, send)
            return

        index_path = Path(self.directory) /self._index_file
        response = FileResponse(index_path)
        await response(scope, receive, send)

@app.get("/")
async def root():
    return RedirectResponse("/home")

app.mount("/", SPAStaticFiles(), name="static")