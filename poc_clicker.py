"""
Cookie Clicker Simulator
"""
import math

import simpleplot
import codeskulptor
codeskulptor.set_timeout(20)
import poc_clicker_provided as provided

SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    def __init__(self):
        self._cookies = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        self._time = 0.0
        self._total = 0.0

    def __str__(self):
        """
        Return human readable state
        """
        return str({ "cookies": self._cookies, "cps": self._cps,
            "time": self._time, "total": self._total })

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._cookies

    def get_cps(self):
        """
        Get current CPS
        Should return a float
        """
        return self._cps

    def get_time(self):
        """
        Get current time
        Should return a float
        """
        return self._time

    def get_history(self):
        """
        Return history list
        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)
        For example: (0.0, None, 0.0, 0.0)
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)
        Should return a float with no fractional part
        """
        if self._cookies >= cookies:
            return 0.0
        return math.ceil((cookies - self._cookies) / self._cps)

    def wait(self, time):
        """
        Wait for given amount of time and update state
        Should do nothing if time <= 0
        """
        if time <= 0:
            return
        self._cookies += time * self._cps
        self._time += time
        self._total += time * self._cps

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state
        Should do nothing if you cannot afford the item
        """
        if cost > self._cookies:
            return
        self._cookies -= cost
        self._cps += additional_cps
        self._history.append((self._time, item_name, cost, self._total))

def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    info = build_info.clone()
    state = ClickerState()

    while state.get_time() <= duration:
        time_left = duration - state.get_time()
        item = strategy(state.get_cookies(), state.get_cps(),
            state.get_history(), time_left, info)
        time_until = state.time_until(info.get_cost(item)) if item else None

        if not item or time_until > time_left:
            break

        state.wait(time_until)
        state.buy_item(item, info.get_cost(item), info.get_cps(item))
        info.update_item(item)
    state.wait(duration - state.get_time())

    return state

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    items = build_info.build_items()
    items = filter(lambda item: (cookies + cps * time_left) >=
        build_info.get_cost(item), items)
    if not items:
        return None
    cheap = min(items, key = lambda item: build_info.get_cost(item))
    return cheap

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items = build_info.build_items()
    items = filter(lambda item: (cookies + cps * time_left) >=
        build_info.get_cost(item), items)
    if not items:
        return None
    expensive = max(items, key = lambda item: build_info.get_cost(item))
    return expensive

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    def predicate(item):
        return (cookies + cps * time_left) >= build_info.get_cost(item)

    def key(item):
        return build_info.get_cps(item) / build_info.get_cost(item)

    try:
        return max(filter(predicate, build_info.build_items()), key=key)
    except ValueError:
        return None

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies',
        [history], True)

def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

# run()
