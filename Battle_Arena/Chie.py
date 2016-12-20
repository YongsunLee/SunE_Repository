from pico2d import *

class Chie:
    # 이동 상태
    STAND_L, WALK_L, RUN_L, JUMP_L, DOWN_L, BACKWALK_L, BACKSTEP_L = 1, 2,  3,  4,  5,  6,  7
    STAND_R, WALK_R, RUN_R, JUMP_R, DOWN_R, BACKWALK_R, BACKSTEP_R = 8, 9, 10, 11, 12, 13, 14
    FALL = 15
    # 공격 상태
    SREG_L, SFIST_L, RKICK_L = 16, 17, 18
    SREG_R, SFIST_R, RKICK_R = 19, 20, 21

    # 물리적 속도 지정
    PIXEL_PER_METER = (250.0 / 1.6)  # 250 pixel 160cm // 1 pixel 0.64cm
    GRAVITY = 9.8
    # 걷기
    WALK_SPEED_KMPH = 10.0  # Km / Hour
    WALK_SPEED_PPS = (((WALK_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER)
    BACKWALK_SPEED_KMPH = 5.0  # Km / Hour
    BACKWALK_SPEED_PPS = (((BACKWALK_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER)
    # 뛰기
    RUN_SPEED_KMPH = 20.0  # Km / Hour
    RUN_SPEED_PPS = (((RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER)
    BACKSTEP_SPEED_KMPH = 15.0  # Km / Hour
    BACKSTEP_SPEED_PPS = (((BACKSTEP_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER)
    # 점프
    JUMP_SPEED_KMPH = 1.0
    JUMP_SPEED_PPS = (((JUMP_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER)

    # 액션 프레임 조절
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 12

    # 속도 계산 핸들
    def handle_speed(self, frame_time):
        global walk_speed, backwalk_speed, run_speed, backstep_speed, jump_speed
        walk_speed     = self.WALK_SPEED_PPS       * frame_time
        backwalk_speed = self.BACKWALK_SPEED_PPS   * frame_time
        run_speed      = self.RUN_SPEED_PPS        * frame_time
        backstep_speed = self.BACKSTEP_SPEED_PPS   * frame_time
        jump_speed     = self.JUMP_SPEED_PPS       * frame_time * self.GRAVITY

        self.key_timer += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.total_frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time

    # 프레임 출력함수
    def handle_frame_stand(self):
        self.stand_frame = int(self.total_frame) % 10
    def handle_frame_walk(self):
        if self.key_timer < 3.0:
            self.walk_frame = int(self.total_frame) % 6 + 2
        else:
            self.walk_frame = int(self.total_frame) % 8
        self.x += (self.dir * walk_speed)
        self.key_timer = int(self.key_timer) % 3
    def handle_frame_backwalk(self):
        if self.key_timer > 3.0:
            self.backwalk_frame = int(self.total_frame) % 6 + 2
        else:
            self.backwalk_frame = int(self.total_frame) % 8
        self.x -= (self.dir * backwalk_speed)
        self.key_timer = int(self.key_timer) % 3
    def handle_frame_run(self):
        if self.key_timer > 3.0:
            self.run_frame = 3
            self.run_frame = int(self.total_frame) % 8
        else:
            self.run_frame = int(self.total_frame) % 11
        self.x += (self.dir * run_speed)
    def handle_frame_down(self):
        if self.key_timer > 3.0:
            self.down_frame = int(self.total_frame) % 6 + 3
        else:
            self.down_frame = int(self.total_frame) % 10
    def handle_frame_jump(self):
        self.jump_frame = int(self.total_frame) % 8
        self.y += int(jump_speed)
        if self.y >= 360:
            self.state = self.FALL
    def handle_frame_fall(self):
        self.jump_frame = int(self.total_frame) % 16 + 8
        self.y -= int(jump_speed)
        if self.y <= 180:
            if self.dir == 1:
                self.state = self.STAND_L
            elif self.dir == -1:
                self.state = self.STAND_R
    def handle_frame_backstep(self):
        self.backstep_frame = int(self.total_frame) % 5
        self.x -= (self.dir * backstep_speed)
        if self.backstep_frame == 4:
            if self.dir == 1:
                self.state = self.STAND_L
            elif self.dir == -1:
                self.state = self.STAND_R
            self.backstep_frame = 0
    def handle_frame_sfist(self):
        self.s_fist_frame = int(self.total_frame) % 5
        if self.s_fist_frame == 4:
            if   self.dir == 1: self.state = self.STAND_L
            else              : self.state = self.STAND_R
    def handle_frame_sreg(self):
        self.s_reg_frame = int(self.total_frame) % 11
        if self.s_reg_frame == 10:
            if   self.dir == 1:
                self.state = self.STAND_L
            else              :
                self.state = self.STAND_R
            self.s_reg_frame = 0
        self.round_kick_frame = 0
        self.key_timer = int(self.key_timer) % 3
    def handle_frame_rkick(self):
        self.round_kick_frame = int(self.total_frame) % 9
        if self.round_kick_frame == 8:
            if   self.dir == 1:
                self.state = self.STAND_L
            else              :
                self.state = self.STAND_R
            self.round_kick_frame = 0
        self.s_reg_frame = 0

    # 이미지 출력 함수
    def handle_image_stand(self):
        if self.dir    == 1:
            self.image_stand_L.clip_draw(self.stand_frame * 148, 0, 148, 250, self.x, self.y)
        elif self.dir == -1:
            self.image_stand_R.clip_draw(self.stand_frame * 148, 0, 148, 250, self.x, self.y)
    def handle_image_walk(self):
        if self.dir   ==  1:
            self.image_walk_L.clip_draw(self.walk_frame * 150, 0, 150, 250, self.x, self.y)
        elif self.dir == -1:
            self.image_walk_R.clip_draw(self.walk_frame * 150, 0, 150, 250, self.x, self.y)
    def handle_image_backwalk(self):
        if self.dir   ==  1:
            self.image_backwalk_L.clip_draw(self.backwalk_frame * 157, 0, 157, 250, self.x, self.y)
        elif self.dir == -1:
            self.image_backwalk_R.clip_draw(self.backwalk_frame * 157, 0, 157, 250, self.x, self.y)
    def handle_image_run(self):
        if self.dir == 1:
            self.image_run_L.clip_draw(self.run_frame * 250, 0, 250, 250, self.x, self.y)
        elif self.dir == -1:
            self.image_run_R.clip_draw(self.run_frame * 250, 0, 250, 250,self.x, self.y)
    def handle_image_down(self):
        if self.dir == 1:
            self.image_down_L.clip_draw(self.down_frame * 125, 0, 125, 250, self.x, self.y)
        elif self.dir == -1:
            self.image_down_R.clip_draw(self.down_frame * 125, 0, 125, 250, self.x, self.y)
    def handle_image_jump(self):
        if self.dir == 1:
            self.image_jump_L.clip_draw(self.jump_frame * 121, 0, 121, 280, self.x, self.y)
        elif self.dir == -1:
            self.image_jump_R.clip_draw(self.jump_frame * 121, 0, 121, 280, self.x, self.y)
    def handle_image_fall(self):
        if self.dir == 1:
            self.image_jump_L.clip_draw((16 - self.jump_frame) * 121, 0, 121, 280, self.x, self.y )
        elif self.dir == -1:
            self.image_jump_R.clip_draw((16 - self.jump_frame) * 121, 0, 121, 280, self.x, self.y)
    def handle_image_backstep(self):
        if self.dir == 1:
            self.image_backstep_L.clip_draw(self.backstep_frame * 160, 0, 160, 250, self.x, self.y)
        elif self.dir == -1:
            self.image_backstep_R.clip_draw(self.backstep_frame * 160, 0, 160, 250, self.x, self.y)
    def handle_image_sfist(self):
        if self.dir == 1:
            self.image_s_fist_L.clip_draw(self.s_fist_frame * 180, 0, 180, 250, self.x, self.y)
        elif self.dir == -1:
            self.image_s_fist_R.clip_draw(self.s_fist_frame * 180, 0, 180, 250, self.x, self.y)
    def handle_image_sreg(self):
        if self.dir == 1:
            self.image_s_reg_L.clip_draw(self.s_reg_frame * 390, 0, 390, 250, self.x, self.y)
        elif self.dir == -1:
            self.image_s_reg_R.clip_draw(self.s_reg_frame * 390, 0, 390, 250, self.x, self.y)
    def handle_image_rkick(self):
        self.s_reg_frame = 0
        if self.dir == 1:
            self.image_round_kick_L.clip_draw(self.round_kick_frame * 350, 0, 350, 250, self.x, self.y)
        elif self.dir == -1:
            self.image_round_kick_R.clip_draw(self.round_kick_frame * 350, 0, 350, 250, self.x, self.y)


    # 프레임 갱신 핸들
    frame_handle = {
        STAND_L    : handle_frame_stand,
        STAND_R    : handle_frame_stand,
        WALK_L     : handle_frame_walk,
        WALK_R     : handle_frame_walk,
        BACKWALK_L : handle_frame_backwalk,
        BACKWALK_R : handle_frame_backwalk,
        RUN_L      : handle_frame_run,
        RUN_R      : handle_frame_run,
        DOWN_L     : handle_frame_down,
        DOWN_R     : handle_frame_down,
        JUMP_L     : handle_frame_jump,
        JUMP_R     : handle_frame_jump,
        BACKSTEP_L : handle_frame_backstep,
        BACKSTEP_R : handle_frame_backstep,
        FALL       : handle_frame_fall,
        SFIST_L    : handle_frame_sfist,
        SFIST_R    : handle_frame_sfist,
        SREG_L     : handle_frame_sreg,
        SREG_R     : handle_frame_sreg,
        RKICK_L    : handle_frame_rkick,
        RKICK_R    : handle_frame_rkick
    }

    # 이미지 출력 핸들
    image_handle = {
        STAND_L    : handle_image_stand,
        STAND_R    : handle_image_stand,
        WALK_L     : handle_image_walk,
        WALK_R     : handle_image_walk,
        BACKWALK_L : handle_image_backwalk,
        BACKWALK_R : handle_image_backwalk,
        RUN_L      : handle_image_run,
        RUN_R      : handle_image_run,
        DOWN_L     : handle_image_down,
        DOWN_R     : handle_image_down,
        JUMP_L     : handle_image_jump,
        JUMP_R     : handle_image_jump,
        BACKSTEP_L : handle_image_backstep,
        BACKSTEP_R : handle_image_backstep,
        FALL       : handle_image_fall,
        SFIST_L    : handle_image_sfist,
        SFIST_R    : handle_image_sfist,
        SREG_L     : handle_image_sreg,
        SREG_R     : handle_image_sreg,
        RKICK_L    : handle_image_rkick,
        RKICK_R    : handle_image_rkick
    }

    def handle_event(self, event):
        # KeyDown
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            if   self.dir ==  1:    self.dir = -1
            elif self.dir == -1:    self.dir = 1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if   self.dir ==  1:
                if self.key_timer < 3.0:
                    self.state = self.BACKSTEP_L
                else:
                    self.state = self.BACKWALK_L
            elif self.dir == -1:
                if self.key_timer < 3.0:
                    self.state = self.RUN_R
                else:
                    self.state = self.WALK_R
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if   self.dir ==  1:
                if self.key_timer < 3.0:
                    self.state = self.RUN_L
                else:
                    self.state = self.WALK_L
            elif self.dir == -1:
                if self.key_timer < 3.0:
                    self.state = self.BACKSTEP_R
                else:
                    self.state = self.BACKWALK_R
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.dir == 1:
                self.state = self.DOWN_L
            elif self.dir == -1:
                self.state = self.DOWN_R
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.dir == 1:
                self.state = self.JUMP_L
            elif self.dir == -1:
                self.state = self.JUMP_R

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            if self.dir == 1:
                self.state = self.SFIST_L
            elif self.dir == -1:
                self.state = self.SFIST_R
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            if self.dir == 1:
                if self.key_timer < 3.0:
                    self.state = self.RKICK_L
                else:
                    self.state = self.SREG_L
            elif self.dir == -1:
                if self.key_timer < 3.0:
                    self.state = self.RKICK_R
                else:
                    self.state = self.SREG_R
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
            if self.dir == 1:
                self.state = self.SFIST_L
            elif self.dir == -1:
                self.state = self.SFIST_R

        # Key UP
        if (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.dir == 1:
                self.state = self.STAND_L
            elif self.dir == -1:
                self.state = self.STAND_R
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.dir == 1:
                self.state = self.STAND_L
            elif self.dir == -1:
                self.state = self.STAND_R
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.dir == 1:
                self.state = self.STAND_L
            elif self.dir == -1:
                self.state = self.STAND_R
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            pass

    #_________________________________________________
    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x,maximum))

        self.handle_speed(frame_time)
        self.frame_handle[self.state](self)

        self.x = clamp(80, self.x, 1200)
        self.y = clamp(180, self.y, 595)
    #_________________________________________________

    def __init__(self):
        # 캐릭터 피봇 좌표
        self.x = 820
        self.y = 180
        self.dir = 1

        # 프레임 변수
        self.total_frame        = 0
        self.stand_frame        = 0
        self.walk_frame         = 0
        self.backwalk_frame     = 0
        self.run_frame          = 0
        self.down_frame         = 0
        self.jump_frame         = 0
        self.backstep_frame     = 0
        self.s_fist_frame       = 0
        self.s_reg_frame        = 0
        self.round_kick_frame   = 0

        # 상태 체크
        self.state = self.STAND_L
        self.key_timer = 0

        # 이미지 파일______________________________________________
            # 왼쪽 파일
        self.image_stand_L      = load_image('Asset\\Chie\\Chie_Stand_L.png')
        self.image_walk_L       = load_image('Asset\\Chie\\Chie_Walk_L.png')
        self.image_backwalk_L   = load_image('Asset\\Chie\\Chie_Backwalk_L.png')
        self.image_run_L        = load_image('Asset\\Chie\\Chie_Run_L.png')
        self.image_down_L       = load_image('Asset\\Chie\\Chie_Down_L.png')
        self.image_jump_L       = load_image('Asset\\Chie\\Chie_Jump_L.png')
        self.image_backstep_L   = load_image('Asset\\Chie\\Chie_Backstep_L.png')
        self.image_s_fist_L     = load_image('Asset\\Chie\\Chie_Simple_Fist_L.png')
        self.image_s_reg_L      = load_image('Asset\\Chie\\Chie_Simple_Reg_L.png')
        self.image_round_kick_L = load_image('Asset\\Chie\\Chie_Round_kick_L.png')

            # 오른쪽 파일
        self.image_stand_R      = load_image('Asset\\Chie\\Chie_Stand_R.png')
        self.image_walk_R       = load_image('Asset\\Chie\\Chie_Walk_R.png')
        self.image_backwalk_R   = load_image('Asset\\Chie\\Chie_Backwalk_R.png')
        self.image_run_R        = load_image('Asset\\Chie\\Chie_Run_R.png')
        self.image_down_R       = load_image('Asset\\Chie\\Chie_Down_R.png')
        self.image_jump_R       = load_image('Asset\\Chie\\Chie_Jump_R.png')
        self.image_backstep_R   = load_image('Asset\\Chie\\Chie_Backstep_R.png')
        self.image_s_fist_R     = load_image('Asset\\Chie\\Chie_Simple_Fist_R.png')
        self.image_s_reg_R      = load_image('Asset\\Chie\\Chie_Simple_Reg_R.png')
        self.image_round_kick_R = load_image('Asset\\Chie\\Chie_Round_kick_R.png')






    #____________________________________________
    def draw(self):
            self.image_handle[self.state](self)
    #____________________________________________
