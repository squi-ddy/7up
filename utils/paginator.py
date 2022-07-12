import datetime
from enum import IntEnum, auto, unique
from typing import Any, Sequence, Union

import nextcord
from nextcord.ext import commands


# noinspection PyArgumentList
@unique
class FooterType(IntEnum):
    TIMESTAMP = auto()
    PAGE_NUMBER = auto()
    NONE = auto()


class Paginator(nextcord.ui.View):
    footer_type: FooterType
    footer_bot_icon: bool
    message: nextcord.PartialInteractionMessage
    embeds: Sequence[nextcord.Embed]
    bot: commands.Bot
    page: int

    def __init__(
        self,
        *,
        message: nextcord.PartialInteractionMessage,
        embeds: Sequence[nextcord.Embed],
        author: Union[nextcord.User, nextcord.Member],
        bot: commands.Bot,
        timeout: float = 180.0,
        footer_type: FooterType = FooterType.NONE,
        footer_bot_icon: bool = False,
    ) -> None:
        super().__init__(timeout=timeout)
        self.footer_type = footer_type
        self.footer_bot_icon = footer_bot_icon
        self.message = message
        self.embeds = embeds
        self.author = author
        self.bot = bot
        self.page = 0

        if self.bot.user is None or self.bot.user.display_avatar is None:
            raise ValueError("Invalid bot avatar")

        if self.footer_type != FooterType.NONE:
            for i, embed in enumerate(self.embeds):
                if self.footer_type == FooterType.TIMESTAMP:
                    embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(
                    text=f"Page {i + 1} of {len(self.embeds)}"
                    if self.footer_type == FooterType.PAGE_NUMBER
                    else "\u200b",
                    icon_url=self.bot.user.display_avatar.url if self.footer_bot_icon else nextcord.Embed.Empty,
                )

    async def start(self) -> None:
        await self.message.edit(
            embed=self.embeds[0],
            view=Paginator(message=self.message, embeds=self.embeds, author=self.author, bot=self.bot),
        )

    async def on_timeout(self) -> None:
        for button in self.children:
            if not isinstance(button, nextcord.ui.Button):
                continue

            button.disabled = True
        await self.message.edit(embed=self.embeds[0], view=self)
        await super().on_timeout()

    @nextcord.ui.button(emoji="⬅️", style=nextcord.ButtonStyle.grey, disabled=True)
    async def previous(self, button: nextcord.ui.Button[Any], interaction: nextcord.Interaction) -> None:
        if interaction.user is None:
            return

        if self.author.id == interaction.user.id:
            self.page -= 1
            embed = self.embeds[self.page]
            if self.page == 0:
                button.disabled = True
            if self.page < len(self.embeds):
                self.next.disabled = False  # type: ignore
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("This is not for you!️", ephemeral=True)

    @nextcord.ui.button(emoji="➡️", style=nextcord.ButtonStyle.grey, disabled=False)
    async def next(self, button: nextcord.ui.Button[Any], interaction: nextcord.Interaction) -> None:
        if interaction.user is None:
            return

        if self.author.id == interaction.user.id:
            self.page += 1
            embed = self.embeds[self.page]
            if self.page > 0:
                self.previous.disabled = False  # type: ignore
            if self.page == len(self.embeds) - 1:
                button.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("This is not for you!️", ephemeral=True)

    @nextcord.ui.button(emoji="🗑️", style=nextcord.ButtonStyle.red)
    async def delete(self, _button: nextcord.ui.Button[Any], interaction: nextcord.Interaction) -> None:
        if interaction.user is None:
            return

        if self.author.id == interaction.user.id:
            await interaction.response.edit_message(view=None)
        else:
            await interaction.response.send_message("This is not for you!️", ephemeral=True)
