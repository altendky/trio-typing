import attr
import trio
from typing import (
    Any,
    AsyncContextManager,
    Awaitable,
    Callable,
    ContextManager,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

F = TypeVar("F", bound=Callable[..., Any])

async def wait_all_tasks_blocked(
    cushion: float = ..., tiebreaker: int = ...
) -> None: ...
def trio_test(fn: F) -> F: ...

class MockClock(trio.abc.Clock):
    rate: float
    autojump_threshold: float
    def __init__(self, rate: float = ..., autojump_threshold: float = ...): ...
    def start_clock(self) -> None: ...
    def current_time(self) -> float: ...
    def deadline_to_sleep_time(self, deadline: float) -> float: ...
    def jump(self, seconds: float) -> None: ...

def assert_checkpoints() -> ContextManager[None]: ...
def assert_no_checkpoints() -> ContextManager[None]: ...

class Sequencer:
    def __call__(self, position: int) -> AsyncContextManager[None]: ...

_StreamMaker = Callable[
    [], Awaitable[Tuple[trio.abc.SendStream, trio.abc.ReceiveStream]]
]

async def check_one_way_stream(
    stream_maker: _StreamMaker, clogged_stream_maker: Optional[_StreamMaker]
) -> None: ...
async def check_two_way_stream(
    stream_maker: _StreamMaker, clogged_stream_maker: Optional[_StreamMaker]
) -> None: ...
async def check_half_closeable_stream(
    stream_maker: _StreamMaker, clogged_stream_maker: Optional[_StreamMaker]
) -> None: ...

MemoryStreamHook = Optional[Callable[[], Awaitable[Any]]]
MemoryStreamSyncHook = Optional[Callable[[], Any]]
@attr.s(auto_attribs=True)
class MemorySendStream(trio.abc.SendStream):
    send_all_hook: MemoryStreamHook = ...
    wait_send_all_might_not_block_hook: MemoryStreamHook = ...
    close_hook: MemoryStreamSyncHook = ...
    async def send_all(self, data: Union[bytes, bytearray, memoryview]) -> None: ...
    async def wait_send_all_might_not_block(self) -> None: ...
    async def aclose(self) -> None: ...
    def close(self) -> None: ...
    async def get_data(self, max_bytes: Optional[int] = ...) -> bytes: ...
    def get_data_nowait(self, max_bytes: Optional[int] = ...) -> bytes: ...

@attr.s(auto_attribs=True)
class MemoryReceiveStream(trio.abc.ReceiveStream):
    receive_some_hook: MemoryStreamHook = ...
    close_hook: MemoryStreamSyncHook = ...
    async def receive_some(self, max_bytes: Optional[int] = ...) -> bytes: ...
    async def aclose(self) -> None: ...
    def close(self) -> None: ...
    def put_data(self, data: bytes) -> None: ...
    def put_eof(self) -> None: ...

def memory_stream_pump(
    memory_send_stream: MemorySendStream,
    memory_receive_stream: MemoryReceiveStream,
    *,
    max_bytes: Optional[int] = ...,
) -> bool: ...
def memory_stream_one_way_pair() -> Tuple[MemorySendStream, MemoryReceiveStream]: ...
def memory_stream_pair() -> Tuple[trio.StapledStream, trio.StapledStream]: ...
def lockstep_stream_one_way_pair() -> Tuple[MemorySendStream, MemoryReceiveStream]: ...
def lockstep_stream_pair() -> Tuple[trio.StapledStream, trio.StapledStream]: ...
async def open_stream_to_socket_listener(
    socket_listener: trio.SocketListener
) -> trio.SocketStream: ...
