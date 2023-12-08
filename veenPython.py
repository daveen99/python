import tkinter as tk
from PIL import Image, ImageTk
import pygame
import time
import random

# 이미지 리사이즈 해주는 메서드
def resize_image(image, new_width, new_height):
    resized_image = image.resize((new_width, new_height), Image.BICUBIC)
    return ImageTk.PhotoImage(resized_image)

# 이미지 id를 넣으면 해당 이미지를 없애주는 메서드
def remove_image(image):
    canvas.delete(image)

# 백그라운드 기본 테마곡을 무한반복 실행해주는 메서드
def set_background_music():
    global BGM
    BGM.play(-1)

# 게임스타트 메서드
def mainStart(event):
    global start, ammo_label, ammoText, total, subjectText
    if not start:
        if shootCount == 0:
            # r 키를 눌렀을 때 배경음악 설정과 이미지 제거
            startBGM = pygame.mixer.Sound('start.mp3')
            startBGM.set_volume(0.1)
            startBGM.play()
            time.sleep(2)
            set_background_music()
            remove_image(main_image)
            start = True
            
            ammoText = f"A total of {total} bullets..."
            ammo_label = canvas.create_text(canvas_width / 2 + 250, canvas_height * 4 / 4.2, anchor=tk.CENTER, text=ammoText, font=("Verdana", 36, "italic"))

            subject_label = canvas.create_text(700, 50, anchor=tk.CENTER, text=subjectText, font=("Helvetica", 20))

            # 총알 이미지 보이기 시작
            updateAmmo()

            # 적 생성 시작
            generate_enemy()


def shoot(event):
    global ammo, start, shootCount, ammoText, ammo_label
    if start == True:
        if ammo > 0:
            gunSound = pygame.mixer.Sound('gunSound.mp3')
            gunSound.set_volume(0.1)
            gunSound.play()    
            ammo = ammo -1 
            # 총 쏠때 불꽃이미지 잠깐 나타나게하기
            shot_image = canvas.create_image(canvas_width / 2.6, canvas_height * 4 / 5.6, anchor=tk.CENTER, image=resized_shot)
            canvas.after(100, lambda: remove_image(shot_image))
            updateAmmo()

            shootCount = shootCount + 1
            ammoText = f"A total of {16 - shootCount} bullets..."
            canvas.delete(ammo_label)
            ammo_label = canvas.create_text(canvas_width / 2 + 250, canvas_height * 4 / 4.2, anchor=tk.CENTER, text=ammoText, font=("Verdana", 36, "italic"))
            if shootCount == 16:
                goEnding()
                
            if ammo == 0:
                global R_image
                R_image = canvas.create_image(canvas_width / 2.6, canvas_height * 4 / 4.7, anchor=tk.CENTER, image=resized_R)

            
        
def insertBullet():
    reloadSound = pygame.mixer.Sound('secondBullet.mp3')
    reloadSound.set_volume(0.1)
    reloadSound.play()  
def rollSound():
    reloadSound = pygame.mixer.Sound('rollSound.mp3')
    reloadSound.set_volume(0.1)
    reloadSound.play()  

def reload(event):
    global ammo
    if ammo < 4:
        if ammo == 0:
            insertBullet()
            ammo = min(4, ammo + 1)
            pygame.time.delay(500)
            insertBullet()
            ammo = min(4, ammo + 1)
            pygame.time.delay(500)
            insertBullet()
            ammo = min(4, ammo + 1)
            pygame.time.delay(500)
            insertBullet()
            ammo = min(4, ammo + 1)
            pygame.time.delay(100)
            rollSound()
            remove_image(R_image);
        updateAmmo()

def updateAmmo():
    global ammo, ammo_list, shootCount, ammoText, ammo_label

    # 현재 화면에 그려진 총알 이미지 제거
    # iter문
    for id in ammo_list:
        remove_image(id)

    # 현재 총알 개수에 맞게 이미지 다시 그리기
    ammo_list = []
    for i in range(ammo):
        ammo_image = canvas.create_image(50 + i * 70, 50, anchor=tk.CENTER, image=resized_ammo)
        ammo_list.append(ammo_image)      

 
def on_enemy_click(event, enemy_id):
    global killCount
    remove_image(enemy_id)  # 적 이미지 클릭 시 제거
    killSound = pygame.mixer.Sound('ds.mp3')
    killSound.set_volume(0.1)
    killSound.play()  
    killCount = killCount + 1

def on_citizen_click(event, citizen_id):
    global citizenCount
    remove_image(citizen_id)  # 적 이미지 클릭 시 제거
    killSound = pygame.mixer.Sound('ds.mp3')
    killSound.set_volume(0.1)
    killSound.play()  
    citizenCount = citizenCount + 1

def generate_enemy():
    global start
    if shootCount < 16:
        if start == True:
            rand = random.randrange(1,11)
            if (rand > 3):
                enemy_x = random.randint(50, canvas_width - 50)
                enemy_y = random.randint(50, canvas_height - 50)
                enemy_id = canvas.create_image(enemy_x, enemy_y, anchor=tk.CENTER, image=resized_enemy)

                canvas.tag_bind(enemy_id, '<Button-1>', lambda event, id=enemy_id: on_enemy_click(event, id))
                canvas.after(1000, lambda: remove_image(enemy_id))

                # 다음 적 생성(게임이 끝날때까지!)
                canvas.after(3000, generate_enemy)
            else :
                citizen_x = random.randint(50, canvas_width - 50)
                citizen_y = random.randint(50, canvas_height - 50)
                citizen_id = canvas.create_image(citizen_x, citizen_y, anchor=tk.CENTER, image=resized_citizen)

                canvas.tag_bind(citizen_id, '<Button-1>', lambda event, id=citizen_id: on_citizen_click(event, id))
                canvas.after(1000, lambda: remove_image(citizen_id))

                # 다음 적 생성(게임이 끝날때까지!)
                canvas.after(3000, generate_enemy)    

def goEnding():
    global start, BGM, end_image, ammo, ammo_label
    start = False
    ammo = 4
    BGM.stop()           
    canvas.delete("all") 
    canvas.delete(ammo_label)
    end_image = canvas.create_image(canvas_width / 2, canvas_height / 2, anchor=tk.CENTER, image=resized_end)
    ending_text = f"적 {killCount}명 처치, 시민 {citizenCount}명 살해."
    ending_label = canvas.create_text(canvas_width / 2, canvas_height * 3 / 5.3, anchor=tk.CENTER, text=ending_text, font=("Helvetica", 36))
    game_over_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        
def restart_game():
    global BG_image, gunIMG_image, main_image, end_image,shootCount, killCount, game_over_button, ammoText, citizenCount
    remove_image(end_image)
    game_over_button.destroy()

    shootCount = 0
    killCount = 0
    citizenCount = 0
    ammoText = 20

    BG_image = canvas.create_image(canvas_width / 2, canvas_height / 2, anchor=tk.CENTER, image=resized_BG)
    gunIMG_image = canvas.create_image(canvas_width / 7, canvas_height * 4 / 5, anchor=tk.CENTER, image=resized_gunIMG)
    main_image = canvas.create_image(canvas_width / 2, canvas_height / 2, anchor=tk.CENTER, image=resized_main)
    game_over_button = tk.Button(window, text="과거로 돌아가기", command=restart_game, width=20, height=2, font=("Helvetica", 16))



# 게임내 필요한 변수
start = False    
ammo = 4
ammo_list = []
shootCount = 0
killCount = 0
citizenCount = 0
total = 16 - shootCount
ammoText = f"A total of {total} bullets..."
subjectText = "Subject : Kill the enemy, save the citizens"


# 음악관리 mixer 초기화
pygame.mixer.init()
BGM = pygame.mixer.Sound('bgm.mp3')
BGM.set_volume(0.1) 

# 윈도우 생성
window = tk.Tk()
window.title("서부의 건맨")

# 윈도우 크기 설정
window.geometry("1000x1000")

# Canvas 생성
canvas_width = 1000
canvas_height = 1000
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height)
canvas.pack(fill=tk.BOTH, expand=tk.YES)

game_over_button = tk.Button(window, text="과거로 돌아가기", command=restart_game, width=20, height=2, font=("Helvetica", 16))

# 배경화면 추가
BG = Image.open('pythonBG.png')
resized_BG = resize_image(BG, 1000, 1000)  # 적절한 크기로 조절
BG_image = canvas.create_image(canvas_width / 2, canvas_height / 2, anchor=tk.CENTER, image=resized_BG)

# 총 이미지 추가
gunIMG = Image.open('gun.png')
resized_gunIMG = resize_image(gunIMG, 400, 400)  # 적절한 크기로 조절
gunIMG_image = canvas.create_image(canvas_width / 7, canvas_height * 4 / 5, anchor=tk.CENTER, image=resized_gunIMG)

# 메인화면 추가
main = Image.open('main.png')
resized_main = resize_image(main, 1000, 1000)  # 적절한 크기로 조절
main_image = canvas.create_image(canvas_width / 2, canvas_height / 2, anchor=tk.CENTER, image=resized_main)

# 총알 이미지 추가(사격, 장전시 변화)
ammo_image = Image.open('ammo.png')
resized_ammo = resize_image(ammo_image, 50, 50)

# 총 쏠때 불꽃 이미지 추가(shoot 메서드 작동시 나타남)
shot_image = Image.open('fire.png')
resized_shot = resize_image(shot_image, 100, 100)

# 적 이미지 추가(게임시작하면 생성)
enemy_image = Image.open('Vilian.png')
resized_enemy = resize_image(enemy_image, 200, 200)
# 인질 이미지 추가(게임시작하면 생성)
citizen_image = Image.open('citizen.png')
resized_citizen = resize_image(citizen_image, 200, 200)

# R 키보드 이미지 추가
R_image = Image.open('Rkey.png')
resized_R = resize_image(R_image, 100, 100)

# 엔딩 이미지 추가
end_image = Image.open('endIMG.png')
resized_end = resize_image(end_image, 1000, 1000)

# 총알 텍스트 추가
ammo_label = 1 

window.bind("<Return>", mainStart)
window.bind("<Button-1>", shoot)
window.bind("<KeyPress-r>", reload)

window.mainloop()
