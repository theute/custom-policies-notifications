import logging

from ..events.models import Notification
from .template import TemplateEngine
from .bop_service import BopSender
from ..db import email as email_store, subscriptions

logger = logging.getLogger(__name__)


class EmailProcessor:
    render_template = 'instant_mail'

    def __init__(self) -> None:
        self.rendering = TemplateEngine()
        self.sender = BopSender()

    async def process(self, notification: Notification):
        account_id: str = notification.tenantId

        await email_store.insert_email(account_id, notification.dict())
        email = await self.rendering.render(self.render_template, notification.dict())

        subscribers = await subscriptions.get_subscribers(account_id, 'instant_mail')
        await self.sender.send_email(email, subscribers)
