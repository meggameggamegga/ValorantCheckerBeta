from aiogram.dispatcher.filters.state import StatesGroup, State


class StartState(StatesGroup):
    log_pass = State()

class AdminState(StatesGroup):
    message = State()
    photo = State()
    accept = State()
class TestState(StatesGroup):
    start = State()

class BuyerState(StatesGroup):
    send_price = State()

class AddSeller(StatesGroup):
    get_id = State()
    delete_sell = State()

class LKSeller(StatesGroup):
    set_status_lk = State()

class Check(StatesGroup):
    checks = State()

class PayCheck(StatesGroup):
    get_photo = State()

class AddPayCheck(StatesGroup):
    get_user_id = State()
    get_photo_pay = State()

class AddTestCheck(StatesGroup):
    get_user_test_id = State()
    get_photo_test = State()

