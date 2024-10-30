# event (상태 이벤트 종류, 실제 이벤트 값)
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def start_event(e):
    return e[0] == 'START'


def a_key_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


# 상태머신을 처리해주는 클래스
class StateMachine:
    def __init__(self, o):
        self.o = o # 현재 담당할 객체에 대한 정보를 전달함 (캐릭터 객체)
        self.event_que = [] # 발생하는 일을 저장하는 리스트

    def update(self):
        self.cur_state.do(self.o) # Idle.do()

    def start(self, start_state):
        self.cur_state = start_state # 현재 상태 = Idle
        # Idle 상태로 시작할 때, enter로 들어가 get_time() 함수를 잴 수 있게 해야함
        self.cur_state.enter(self.o, ('START', 0)) # 이벤트를 함꼐 전달, start할때에는 더미값을 저장함.
        print(f'ENTER into {self.cur_state}')

    def draw(self):
        self.cur_state.draw(self.o)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def add_event(self, e):
        self.event_que.append(e) # 상태 머신용 이벤트 추가
        print(f'    DEBUG: new event {e} is added.')
        # 이벤트 발생 여부 및 상태 확인
        if self.event_que:  #리스트에 값이 있으면 true
            e = self.event_que.pop(0) # 리스트의 첫번쨰 요소를 꺼냄

            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e): #e가 지금 check 이벤트이면 space_down이라는 것으로 해석이 됨.
                    print(f'Exit from {self.cur_state}')
                    self.cur_state.exit(self.o, e)
                    self.cur_state = next_state
                    print(f'Enter into {self.cur_state}')
                    self.cur_state.enter(self.o, e)
                    return