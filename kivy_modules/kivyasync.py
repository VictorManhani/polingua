# https://github.com/gottadiveintopython/asynckivy

# -*- coding: utf-8 -*-

__all__ = ('start', 'sleep', 'event', 'thread', 'process', 
           'rest_of_touch_moves', 'sleep', 'sleep_free', 
           'sleep_forever', 'create_sleep')

from functools import partial
from collections import namedtuple
from kivy.clock import Clock
import types
import typing
from inspect import getcoroutinestate, CORO_CLOSED

CallbackParameter = namedtuple('CallbackParameter', ('args', 'kwargs', ))

async def create_sleep(duration):
    '''(experimental) Improves the performance by re-using a ClockEvent. 

        sleep_for_1sec = await create_sleep(1)
        while True:
            dt = await sleep_for_1sec()
            # do whatever you want

    WARNING:

        In the example above, "sleep_for_1sec" must be awaited in the same
        async-thread that created it. That means the following code is not
        allowed:

            sleep_for_1sec = await create_sleep(1)

            asynckivy.start(sleep_for_1sec())  # No
            asynckivy.and_(sleep_for_1sec(), ...)  # No
            asynckivy.or_(sleep_for_1sec(), ...)  # No

            async def some_fn():
                await sleep_for_1sec()
            asynckivy.start(some_fn())  # No

        But the following code is allowed:

            sleep_for_1sec = await create_sleep(1)

            async def some_fn():
                await sleep_for_1sec()
            await some_fn()  # OK
    '''
    # from asynckivy._core import _get_step_coro
    clock_event = Clock.create_trigger(await _get_step_coro(), duration)

    @types.coroutine
    def sleep():
        return (yield clock_event)[0][0]
    return sleep

def start(coro):
    def step_coro(*args, **kwargs):
        try:
            if getcoroutinestate(coro) != CORO_CLOSED:
                coro.send((args, kwargs, ))(step_coro)
        except StopIteration:
            pass
    try:
        coro.send(None)(step_coro)
    except StopIteration:
        pass
    return coro

@types.coroutine
def sleep(duration):
    args, kwargs = yield \
        lambda step_coro: schedule_once(step_coro, duration)
    return args[0]

class Task:
    '''(internal)'''
    __slots__ = ('coro', 'done', 'result', 'done_callback')
    def __init__(self):
        self.coro = None
        self.done = False
        self.result = None
        self.done_callback = None

    def run(self, coro, *, done_callback=None):
        if self.coro is not None:
            raise Exception("'run()' can be called only once.")
        self.done_callback = done_callback
        self.coro = start(self._wrapper(coro))

    async def _wrapper(self, inner_coro):
        self.result = await inner_coro
        self.done = True
        if self.done_callback is not None:
            self.done_callback()

    def cancel(self):
        self.coro.close()

@types.coroutine
def gather(coros:typing.Iterable[typing.Coroutine], *, n:int=None) -> typing.Sequence[Task]:
    '''(internal)'''
    coros = tuple(coros)
    n_coros_left = n if n is not None else len(coros)

    def step_coro(*args, **kwargs):
        nonlocal n_coros_left; n_coros_left -= 1
    def done_callback():
        nonlocal n_coros_left
        n_coros_left -= 1
        if n_coros_left == 0:
            step_coro()
    tasks = tuple(Task() for coro in coros)
    for task, coro in zip(tasks, coros):
        task.run(coro, done_callback=done_callback)

    if n_coros_left <= 0:
        return tasks

    def callback(step_coro_):
        nonlocal step_coro
        step_coro = step_coro_
    yield callback

    return tasks

async def or_(*coros):
    return await gather(coros, n=1)

async def and_(*coros):
    return await gather(coros)

class Event:
    '''Similar to 'trio.Event'. The difference is this one allows the user to
    pass data:

        import asynckivy as ak

        e = ak.Event()
        async def task(e):
            assert await e.wait() == 'A'
        ak.start(task(e))
        e.set('A')
    '''
    __slots__ = ('_value', '_flag', '_step_coro_list', )

    def __init__(self):
        self._value = None
        self._flag = False
        self._step_coro_list = []

    def is_set(self):
        return self._flag

    def set(self, value=None):
        if self._flag:
            return
        self._flag = True
        self._value = value
        step_coro_list = self._step_coro_list
        self._step_coro_list = []
        for step_coro in step_coro_list:
            step_coro(value)

    def clear(self):
        self._flag = False

    @types.coroutine
    def wait(self):
        if self._flag:
            yield lambda step_coro: step_coro()
            return self._value
        else:
            return (yield self._step_coro_list.append)[0][0]

@types.coroutine
def _get_step_coro():
    '''(internal)'''
    return (yield lambda step_coro: step_coro(step_coro))[0][0]

async def thread(func, *, daemon=False, polling_interval=3):
    # from ._sleep import create_sleep
    from threading import Thread

    return_value = None
    is_finished = False
    def wrapper():
        nonlocal return_value, is_finished
        return_value = func()
        is_finished = True
    Thread(target=wrapper, daemon=daemon).start()
    sleep = await create_sleep(polling_interval)
    while not is_finished:
        await sleep()
    return return_value

async def process(p, *, polling_interval=3):
    '''wait for the completion of subprocess'''
    # from ._sleep import create_sleep

    sleep = await create_sleep(polling_interval)
    poll = p.poll
    while poll() is None:
        await sleep()
    return p.returncode

class event:

    def __init__(self, ed, name):
        self.bind_id = None
        self.ed = ed
        self.name = name

    def bind(self, step_coro):
        self.bind_id = bind_id = self.ed.fbind(self.name, self.callback)
        assert bind_id > 0  # check if binding succeeded
        self.step_coro = step_coro

    def callback(self, *args, **kwargs):
        self.parameter = CallbackParameter(args, kwargs)
        ed = self.ed
        ed.unbind_uid(self.name, self.bind_id)
        self.step_coro()

    def __await__(self):
        yield self.bind
        return self.parameter

@types.coroutine
def event(ed, name, *, filter=None, return_value=None):
    bind_id = None
    step_coro = None

    def bind(step_coro_):
        nonlocal bind_id, step_coro
        bind_id = ed.fbind(name, callback)
        assert bind_id  # check if binding succeeded
        step_coro = step_coro_

    def callback(*args, **kwargs):
        if (filter is not None) and (not filter(*args, **kwargs)):
            return
        ed.unbind_uid(name, bind_id)
        step_coro(*args, **kwargs)
        return return_value

    return (yield bind)[0]

async def rest_of_touch_moves(widget, touch, *, eat_touch=False):
    '''Returns an async-generator, which yields the touch when `on_touch_move`
    is fired, and ends when `on_touch_up` is fired. Grabs and ungrabs the
    touch automatically. If `eat_touch` is True, the touch will never be
    dispatched further.
    '''
    # from asynckivy._core import _get_step_coro
    step_coro = await _get_step_coro()

    if eat_touch:
        def _on_touch_up(w, t):
            if t is touch:
                if t.grab_current is w:
                    t.ungrab(w)
                    step_coro(False)
                return True
        def _on_touch_move(w, t):
            if t is touch:
                if t.grab_current is w:
                    step_coro(True)
                return True
    else:
        def _on_touch_up(w, t):
            if t.grab_current is w and t is touch:
                t.ungrab(w)
                step_coro(False)
                return True
        def _on_touch_move(w, t):
            if t.grab_current is w and t is touch:
                step_coro(True)
                return True

    touch.grab(widget)
    uid_up = widget.fbind('on_touch_up', _on_touch_up)
    uid_move = widget.fbind('on_touch_move', _on_touch_move)
    assert uid_up
    assert uid_move

    # assigning to a local variable might improve performance
    true_if_touch_move_false_if_touch_up = \
        _true_if_touch_move_false_if_touch_up

    try:
        while await true_if_touch_move_false_if_touch_up():
            yield touch
    finally:
        touch.ungrab(widget)
        widget.unbind_uid('on_touch_up', uid_up)
        widget.unbind_uid('on_touch_move', uid_move)

@types.coroutine
def _true_if_touch_move_false_if_touch_up() -> bool:
    return (yield lambda step_coro: None)[0][0]

all_touch_moves = rest_of_touch_moves  # will be removed in the future

schedule_once = Clock.schedule_once
def _raise_exception_for_free_type_clock_not_being_available(*args, **kwargs):
    raise Exception(
        "'Clock.schedule_once_free()' is not available."
        " Use a non-default clock."
    )
schedule_once_free = getattr(
    Clock, 'schedule_once_free',
    _raise_exception_for_free_type_clock_not_being_available
)

@types.coroutine
def sleep_free(duration):
    '''(experimental)'''
    args, kwargs = yield \
        lambda step_coro: schedule_once_free(step_coro, duration)
    return args[0]

@types.coroutine
def sleep_forever():
    yield lambda step_coro: None
