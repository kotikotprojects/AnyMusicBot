from aiogram import Router
from . import initialize


router = Router()

router.include_routers(
    initialize.router,
)
