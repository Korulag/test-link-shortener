from urllib.parse import urljoin

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select


from link_shortener.config import settings
from link_shortener.database import engine, Session
from link_shortener.models import Base, ShortLink
from link_shortener.utils import generate_link_id


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/', response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(
        'index.html', {
            'server_host': settings.base_url,
            'link_endpoint': 'get_short_link',
            'request': request
        }
    )


@app.post('/get_short_link/')
async def get_short_link(request: Request, initial_url: str = Form(...)):
    async with Session() as session:
        query = select(ShortLink).where(
            ShortLink.initial_link == initial_url)
        result = await session.execute(query)
        link_item = result.scalars().first()
        if not link_item:
            new_link_id = generate_link_id()
            link_item = ShortLink(
                link_id=new_link_id, initial_link=initial_url
            )
            session.add(link_item)
            await session.commit()
            await session.refresh(link_item)
        return templates.TemplateResponse(
            'short_link.html', {
                'result_short_link': urljoin(
                    settings.base_url, link_item.link_id),
                'follow_count': link_item.follow_count,
                'request': request
            }
        )


@app.get('/{link_id}/')
async def follow_short_link(link_id: str):
    async with Session() as session:
        query = select(ShortLink).where(ShortLink.link_id == link_id)
        result = await session.execute(query)
        link_item = result.scalars().first()
        if not link_item:
            return Response(status_code=404)
        link_item.follow_count += 1
        session.add(link_item)
        await session.commit()
        return RedirectResponse(link_item.initial_link)
