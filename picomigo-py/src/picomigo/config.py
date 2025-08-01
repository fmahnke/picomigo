# pyright: reportUnnecessaryTypeIgnoreComment=false
# from enum import StrEnum, auto
from typing import Annotated, Any, override

from mktech.config2 import BaseConfig, Field
from mktech.path import Path
from mktech.xdg import xdg_config_home
from pydantic import AfterValidator, BaseModel
from pydantic_settings.sources import PathType

__all__ = ['BuildConfig', 'build_config_create']

default_config_path = f'{xdg_config_home()}/picomigo/build.toml'


def _validate_arch(arch: str) -> str:
    return arch


class BuildConfig(BaseConfig):
    class Ninja(BaseModel):
        verbose: bool = False

    log_level: str = 'WARNING'

    arch: Annotated[str, AfterValidator(_validate_arch)] = 'unknown'

    top_build_dir: Path = Path()
    top_source_dir: Path = Path()

    micropython_source_dir: Path | None = None

    build_toml_path: Path | None = None

    verbosity: Annotated[int, Field(ge=0)] = 0

    def __init__(
        self,
        toml_path: PathType = default_config_path,
        *args: Any,  # pyright: ignore[reportAny]
        **kwargs: Any,  # pyright: ignore[reportAny]
    ) -> None:
        super().__init__(
            toml_path,
            *args,  # pyright: ignore[reportAny]
            **kwargs,
        )

    @override
    def model_post_init(self, context: Any, /) -> None:
        self.top_build_dir = Path(f'{self.top_build_dir}/{self.arch}'
                                  ).absolute()

        if self.build_toml_path is None:
            self.build_toml_path = Path(
                f'{self.top_source_dir}/build/build.toml'
            )

        if self.micropython_source_dir is None:
            self.micropython_source_dir = Path(
                f'{self.top_source_dir}/picomigo-native/lib/micropython'
            )


def build_config_create(
    toml_path: PathType | None = None,
    arch: str = '',
    *args: Any,  # pyright: ignore[reportAny]
    **kwargs: Any,  # pyright: ignore[reportAny]
) -> BuildConfig:
    if toml_path is None:
        toml_path = ''

    arch = _validate_arch(arch)

    if 'top_build_dir' in kwargs and kwargs['top_build_dir'] is None:
        del kwargs['top_build_dir']

    if 'top_source_dir' in kwargs and kwargs['top_source_dir'] is None:
        del kwargs['top_source_dir']

    return BuildConfig(toml_path, arch=arch, *args, **kwargs)
