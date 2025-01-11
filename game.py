from tkinter import *
import random as r
from tkinter import messagebox
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
root = Tk()
root.attributes("-fullscreen", True)


player_data = []
dealer_data = []


def load_card_images():
    card_images = {}
    suits = ['черви', 'пики', 'бубны', 'трефы']

    for suit_index, suit in enumerate(suits):
        for rank in range(1, 14):  # Номера от 1 до 13
            card_name = f"cards/card_{rank + suit_index * 13}.png"  # Формат: card_1.png, card_2.png и т.д.
            card_images[f"{rank} {suit}"] = PhotoImage(file=card_name)

    return card_images

deck = [f"{rank} {suit}" for suit in ['черви', 'пики', 'бубны', 'трефы'] for rank in range(1, 14)]

# Заголовок
lbl_title = Label(root, text="Игра в блэкджек", font=("Helvetica", 24))
lbl_title.pack(pady=10)

# Метка для карт дилера
lbl_dealer = Label(root, text="Карты дилера:", font=("Helvetica", 20))
lbl_dealer.pack(pady=5)

# Фрейм для карт дилера
dealer_frame = Frame(root)
dealer_frame.pack(pady=5)

# Метки для карт дилера
dealer_labels = []  # Изменено на пустой список
for _ in range(10):  # Создайте 10 меток, чтобы было достаточно
    label = Label(dealer_frame)
    label.pack(side=LEFT, padx=5)
    dealer_labels.append(label)

# Метка для карт игрока
lbl_player = Label(root, text="Ваши карты:", font=("Helvetica", 20))
lbl_player.pack(pady=5)

# Фрейм для карт игрока
player_frame = Frame(root)
player_frame.pack(pady=5)

# Метки для карт игрока
player_labels = []  # Изменено на пустой список
for _ in range(10):  # Создайте 10 меток, чтобы было достаточно
    label = Label(player_frame)
    label.pack(side=LEFT, padx=5)
    player_labels.append(label)

# Кнопки
btn_deal = Button(root, text="Раздать карты", font=("Helvetica", 18), command=lambda: deal_cards(), bg="green", fg="white")
btn_deal.pack(pady=10, fill=X)

btn_hit = Button(root, text="Еще", font=("Helvetica", 18), command=lambda: hit(), bg="blue", fg="white")
btn_stand = Button(root, text="Хватит", font=("Helvetica", 18), command=lambda: reveal_dealer(), bg="orange", fg="white")
btn_exit = Button(root, text="Выход из игры", font=("Helvetica", 18), command=root.quit, bg="red", fg="white")

# Изначально кнопки "Еще" и "Хватит" скрыты
btn_hit.pack_forget()
btn_stand.pack_forget()
btn_exit.pack_forget()

def card_value(card):
    """Возвращает числовое значение карты."""
    rank = card.split()[0]
    if rank == '1':  # Туз
        return 11
    elif rank in ['11', '12', '13']:  # Валет, Дама, Король
        return 10
    return int(rank)

def calculate_score(cards):
    """Подсчитывает общий счёт с учетом туза."""
    score = sum(card_value(card) for card in cards)
    aces = sum(1 for card in cards if card.split()[0] == '1')  # Количество тузов
    while score > 21 and aces:
        score -= 10  # Превращаем туз из 11 в 1
        aces -= 1
    return score

def has_blackjack(cards):
    """Проверяет, есть ли у игрока 21 очко."""
    return calculate_score(cards) == 21

def load_deck():
    global gaming_deck, card_images
    card_images = load_card_images()
    gaming_deck = deck.copy()

def deal_cards():
    global gaming_deck, player_cards, dealer_cards

    player_cards = []
    dealer_cards = []

    # Открываем одну карту дилера
    d1 = r.choice(gaming_deck)
    dealer_labels[0].config(image=card_images[d1])
    dealer_labels[0].image = card_images[d1]  # Сохранение ссылки на изображение
    dealer_cards.append(d1)
    gaming_deck.remove(d1)

    # Скрываем вторую карту дилера и сохраняем её для вывода в консоль
    d2 = r.choice(gaming_deck)
    dealer_cards.append(d2)
    gaming_deck.remove(d2)

    # Раздаем карты игроку
    for i in range(2):
        p_card = r.choice(gaming_deck)
        player_cards.append(p_card)
        player_labels[i].config(image=card_images[p_card])
        player_labels[i].image = card_images[p_card]
        gaming_deck.remove(p_card)

    # Проверка на 21 очков для дилера
    if has_blackjack(dealer_cards):
        dealer_wins()
        return  # Завершаем функцию, если дилер выиграл

    # Проверка на 21 очков для игрока
    if has_blackjack(player_cards):
        player_wins()
        return  # Завершаем функцию, если игрок выиграл

    btn_deal.pack_forget()
    btn_hit.pack(pady=10, fill=X)
    btn_stand.pack(pady=10, fill=X)
    btn_exit.pack(pady=20, fill=X)

def hit():
    global player_data

    new_card_player = r.choice(gaming_deck)
    player_cards.append(new_card_player)

    for label in player_labels:
        if label.cget("image") == "":
            label.config(image=card_images[new_card_player])
            label.image = card_images[new_card_player]
            break

    # Проверка на 21 очков для игрока
    if has_blackjack(player_cards):
        player_wins()
    elif calculate_score(player_cards) > 21:
        player_loses()

def reveal_dealer():
    global dealer_data
    # Показываем вторую карту дилера
    dealer_labels[1].config(image=card_images[dealer_cards[1]])
    dealer_labels[1].image = card_images[dealer_cards[1]]

    # Проверка на блэкджек у дилера
    if has_blackjack(dealer_cards):
        dealer_wins()
        return  # Завершаем функцию, если дилер выиграл

    # Дилер берет карты, пока у него меньше 17
    while calculate_score(dealer_cards) < 17:
        new_card_dealer = r.choice(gaming_deck)
        dealer_cards.append(new_card_dealer)
        for label in dealer_labels:
            if label.cget("image") == "":
                label.config(image=card_images[new_card_dealer])
                label.image = card_images[new_card_dealer]
                break
        gaming_deck.remove(new_card_dealer)

    # Проверка на выигрыш дилера
    if calculate_score(dealer_cards) > 21:
        player_wins()
    else:
        compare_scores()  # Сравниваем очки игрока и дилера

def compare_scores():
    player_score = calculate_score(player_cards)
    dealer_score = calculate_score(dealer_cards)

    print(f"Счёт игрока: {player_score}, Счёт дилера: {dealer_score}")  # Для отладки

    if player_score > dealer_score:
        player_wins()  # Игрок выигрывает
    elif player_score < dealer_score:
        dealer_wins()  # Дилер выигрывает
    else:
        tie()  # Ничья


def reset_game():
    global gaming_deck, player_cards, dealer_cards

    # Сброс всех карт
    player_cards = []
    dealer_cards = []
    gaming_deck = [f"{rank} {suit}" for suit in ['черви', 'пики', 'бубны', 'трефы'] for rank in range(1, 14)]

    # Очистка меток для карт игрока
    for label in player_labels:
        label.config(image="")

    # Очистка меток для карт дилера
    for label in dealer_labels:
        label.config(image="")

    # Сброс кнопок
    btn_hit.pack_forget()
    btn_stand.pack_forget()
    btn_exit.pack_forget()
    btn_deal.pack(pady=10, fill=X)

    # Скрыть кнопку "Сыграть еще раз"
    btn_play_again.pack_forget()  # Скрываем кнопку

    # Сброс заголовка или других элементов интерфейса, если необходимо
    lbl_title.config(text="Игра в блэкджек")

# Кнопка "Сыграть еще раз"
btn_play_again = Button(root, text="Сыграть еще раз", font=("Helvetica", 18), command=reset_game, bg="purple", fg="white")
btn_play_again.pack(pady=10, fill=X)
btn_play_again.pack_forget()  # Скрываем кнопку изначально

def player_wins():
    """Функция для обработки выигрыша игрока."""
    btn_hit.pack_forget()  # Отключаем кнопку "Еще"
    btn_stand.pack_forget()  # Отключаем кнопку "Хватит"
    btn_play_again.pack(pady=10, fill=X)  # Показываем кнопку "Сыграть еще раз"
    messagebox.showinfo('', 'Вы выиграли')

def dealer_wins():
    """Функция для обработки выигрыша дилера."""
    btn_hit.pack_forget()  # Отключаем кнопку "Еще"
    btn_stand.pack_forget()  # Отключаем кнопку "Хватит"
    btn_play_again.pack(pady=10, fill=X)  # Показываем кнопку "Сыграть еще раз"
    messagebox.showinfo('', 'Вы проиграли')

def player_loses():
    """Функция для обработки проигрыша игрока."""
    btn_hit.pack_forget()  # Отключаем кнопку "Еще"
    btn_stand.pack_forget()  # Отключаем кнопку "Хватит"
    btn_play_again.pack(pady=10, fill=X)  # Показываем кнопку "Сыграть еще раз"
    messagebox.showinfo('', 'Вы проиграли')

def tie():
    """Функция для обработки ничьей."""
    btn_hit.pack_forget()  # Отключаем кнопку "Еще"
    btn_stand.pack_forget()  # Отключаем кнопку "Хватит"
    btn_play_again.pack(pady=10, fill=X)  # Показываем кнопку "Сыграть еще раз"
    messagebox.showinfo('', 'Ничья!')


# Загрузка колоды карт
load_deck()
root.mainloop()