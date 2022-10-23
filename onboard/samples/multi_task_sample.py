from pybricks.tools import wait, StopWatch


def try_wait(time):
    timer = StopWatch()
    while timer.time() < time:
        yield


def repeating_wait_task():
    while True:
        yield from try_wait(2000)
        print('repeating time is up!')


def wait_once_task():
    yield from try_wait(5000)
    print('one time is up!')

    # don't crash the main loop
    while True:
        yield


def main_loop():
    # each "task" will run until the first yield statement here
    tasks = [repeating_wait_task(), wait_once_task()]

    while True:
        # Warning! This assumes that all tasks in the list run forever.
        # If they don't, we will eventually get an unhandled StopIteration exception.
        for t in tasks:
            next(t)

        # Give the CPU some time to relax (this is especially important on EV3)
        wait(1)


main_loop()
