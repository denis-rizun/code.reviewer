from aiogram import Router

from .back import back_router
from .donation import donate_router
from .main import main_router
from .review import review_router
from .support import support_router

router = Router()

router.include_router(back_router)
router.include_router(donate_router)
router.include_router(main_router)
router.include_router(review_router)
router.include_router(support_router)

__all__ = ["router"]
