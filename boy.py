from pico2d import load_image, get_time

from statemachine import right_down, left_down, right_up, left_up, start_event, a_key_down
from statemachine import StateMachine, time_out, space_down
import math

class Idle:
    @staticmethod
    def enter(boy, e):
        # 현재 시작 시간을 기록함
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1
        boy.frame = 0
        boy.dir = 0
        boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 1: # 테스트 리드 타임 줄이는 용도
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class Sleep:
    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100, math.pi / 2, '', boy.x-25, boy.y-25, 100, 100)
            # '' 는 좌우상하 반전을 하지 않겠다는 의미
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100, math.pi / 2, '', boy.x+25, boy.y-25, 100, 100)


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.action = 1
            boy.dir = 1
        elif left_down(e) or right_up(e):
            boy.action = 0
            boy.dir = -1
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * boy.speed

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame*100, boy.action*100, 100, 100, boy.x, boy.y)


class Auto_Run:
    @staticmethod
    def enter(boy, e):
        boy.speed = 6
        boy.scale = 2.0
        boy.frame = 0
        boy.y = 120
        boy.start_time = get_time()
        if boy.action == 3:
            boy.dir = 1
            boy.action = 1
        elif boy.action == 2:
            boy.dir = -1
            boy.action = 0

    @staticmethod
    def exit(boy, e):
        boy.speed = 3
        boy.scale = 1
        boy.y = 90

        if boy.dir == 1:
            boy.action = 3
        elif boy.dir == -1:
            boy.action = 2

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * boy.speed

        if boy.x < 50 or boy.x > 750:
            boy.dir *= -1
            boy.action = 1 if boy.dir == 1 else 0

        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, 0, '', boy.x, boy.y, int(100 * boy.scale), int(100 * boy.scale))


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.scale = 1
        self.speed = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 어떤 객체를 위한 상태 머신인지 알려줄 필요가 있음
        self.state_machine.start(Idle) # 객체를 사용한 것이 아닌 직접적으로 클래스를 사용함
        self.state_machine.set_transitions(
            {
                Sleep: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Idle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, a_key_down: Auto_Run},
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, a_key_down: Auto_Run},
                Auto_Run: {time_out: Idle, right_down: Run, left_down: Run}
            }
        )

    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, event):
        # event : input event
        # state machine event = (이벤트 종류, 값)

        self.state_machine.add_event(
            ('INPUT', event)
        )
        pass

    def draw(self):
        self.state_machine.draw()
