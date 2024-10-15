__package__ = 'plugins_extractor.ytdlp'

from typing import List

from pydantic import Field, model_validator, AliasChoices

from abx.archivebox.base_configset import BaseConfigSet

from archivebox.config.common import ARCHIVING_CONFIG
from archivebox.misc.logging import STDERR


class YtdlpConfig(BaseConfigSet):
    USE_YTDLP: bool                = Field(default=True, validation_alias=AliasChoices('USE_YOUTUBEDL', 'SAVE_MEDIA'))

    YTDLP_BINARY: str              = Field(default='yt-dlp', alias='YOUTUBEDL_BINARY')
    YTDLP_EXTRA_ARGS: List[str]    = Field(default=[], alias='YOUTUBEDL_EXTRA_ARGS')
    
    YTDLP_CHECK_SSL_VALIDITY: bool = Field(default=lambda: ARCHIVING_CONFIG.CHECK_SSL_VALIDITY)
    YTDLP_TIMEOUT: int             = Field(default=lambda: ARCHIVING_CONFIG.MEDIA_TIMEOUT)
    
    @model_validator(mode='after')
    def validate_use_ytdlp(self):
        if self.USE_YTDLP and self.YTDLP_TIMEOUT < 20:
            STDERR.print(f'[red][!] Warning: MEDIA_TIMEOUT is set too low! (currently set to MEDIA_TIMEOUT={self.YTDLP_TIMEOUT} seconds)[/red]')
            STDERR.print('    youtube-dl/yt-dlp will fail to archive any media if set to less than ~20 seconds.')
            STDERR.print('    (Setting it somewhere over 60 seconds is recommended)')
            STDERR.print()
            STDERR.print('    If you want to disable media archiving entirely, set SAVE_MEDIA=False instead:')
            STDERR.print('        https://github.com/ArchiveBox/ArchiveBox/wiki/Configuration#save_media')
            STDERR.print()
        return self


YTDLP_CONFIG = YtdlpConfig()
