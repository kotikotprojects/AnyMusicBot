from aiogram import Bot, F, Router
from aiogram.types import ChosenInlineResult

router = Router()


@router.chosen_inline_result(
    F.result_id.startswith("deezc::") | F.result_id.startswith("scc::")
)
async def on_unneeded_cached_chosen(chosen_result: ChosenInlineResult, bot: Bot):
    await bot.edit_message_reply_markup(
        inline_message_id=chosen_result.inline_message_id, reply_markup=None
    )
