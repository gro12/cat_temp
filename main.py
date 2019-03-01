import random


class TheGame:
    class Event:
        def __init__(self):
            self.rand_unc_ev = [self.rats, self.dragon_strike, self.crowns, self.dolgonosik_planded,
                                self.dolgonosik_chaos,
                                self.dolgonosik_people, self.dolgonosik_gold]
            self.rand_c_ev = [self.war, self.declare_war, self.trade_expedition]

        class TradeExpedition:
            def __init__(self, a):
                self.invested = a
                self.stage = random.randint(0, 7)

            ended = False

            def proceed(self, obj):
                self.stage += 1
                if self.stage == 10:
                    obj.gold += self.invested * random.randint(100, 200) // 100
                    self.ended = True

        def rats(self, obj):
            print("Крысы пробрались в амбар и испортили зерно")
            obj.grain = obj.grain * random.randint(10, 90) // 100

        def dragon_strike(self, obj):
            print("На нас напал дракон")
            obj.grain = obj.grain * random.randint(10, 90) // 100
            obj.gold = obj.gold * random.randint(10, 90) // 100
            obj.people = obj.people * random.randint(10, 90) // 100

        def crowns(self, obj):
            print("На нас напал дракон")
            obj.planted = obj.planted * random.randint(10, 90) // 100

        def dolgonosik_planded(self, obj):
            print("Наши посадки пожрал долгоносик, упорожай погиб, милорд")
            obj.planted = 0

        def dolgonosik_gold(self, obj):
            print("В нашу казну проник долгоносик, казна пуста, милорд")
            obj.gold = 0

        def dolgonosik_people(self, obj):
            print("Долгоносик пожрал наш народ, казна пуста, милорд")
            obj.people = obj.people * 9 // 10
            obj.happiness = obj.happiness // 2

        def dolgonosik_chaos(self, obj):
            print("Хаоситов пожрал долгоносик долгоносик, тёмные боги не слышат нас, милорд")
            obj.chaos_rise = 1

        def cultists(self, obj):
            obj.chaos_rise += 2

        def trade_expedition(self, obj):
            z = min(obj.gold,
                    max(0, int(input(
                        "Милорд, собирается торговая экспедиция в далекие земли! Милорд сколько мы инвестируем туда?"))))
            obj.gold -= z
            if z:
                obj.developments.append(self.TradeExpedition(z))

        def war(self, obj):
            print("Война пришла, милорд!")
            r = random.randint(10, max(11, obj.people))
            print("Милорд, на нас движется армия из " + str(r) + " солдат!")
            c = random.randint(100, 300)
            z = min(obj.gold // c,
                    max(0, int(input("Мимопроезжающая компания наемников предлагает нанять солдат по " + str(
                        c) + " золотых за солдата. сколько человек нанять?"))))
            obj.gold -= z * c
            if z + random.randint(0, z) < r + random.randint(0, r):
                print("Мы проиграли, милорд")
                obj.alive = False
            else:
                print("Мы победили, милорд")
                obj.gold += r * random.randint(100, 400)

        def declare_war(self, obj):
            x = int(input("Милорд мы можем объявить войну, мы объявляем войну,милорд?(1/0)"))
            if x:
                self.war(obj)

        def controlled_event(self, obj):
            self.rand_c_ev[random.randint(0, len(self.rand_c_ev))](obj)

        def uncontrolled_event(self, obj):
            self.rand_unc_ev[random.randint(0, len(self.rand_unc_ev))](obj)

    gold = 10000
    grain = 12500
    chaos_rise = 1
    happiness = 70
    people = 100
    year = 0
    planted = 0
    fed = 0
    event = Event()
    alive = True
    developments = []

    def status(self):
        print("year " + str(self.year))
        print("happines " + str(self.happiness))
        print("grain " + str(self.grain))
        print("gold " + str(self.gold))
        print("people " + str(self.people))
        print("chaos " + str(self.chaos_rise))

    def end(self):
        sum_points = 0
        sum_points += self.gold - 10000
        sum_points += (self.grain - 7500) * 30
        sum_points += self.year * 10000
        sum_points += (self.people - 100) * 1000
        sum_points -= self.chaos_rise * 10000
        print("Ваш счет: " + str(sum_points))

    def eventise(self):
        x = random.randint(0, 2000)
        y = random.randint(0, 2000)
        if x < 10:
            self.event.controlled_event(self)
            self.event.controlled_event(self)
        elif x < 400:
            self.event.controlled_event(self)
        if y < 10:
            self.event.uncontrolled_event(self)
            self.event.uncontrolled_event(self)
        elif y < 400:
            self.event.uncontrolled_event(self)

    def trade(self):
        x = random.randint(20, 30)
        print("Приехал торговец, привез зерно по " + str(x) + " золотых за мешок")
        c = max(0, min(int(input("Сколько купить зерна?")), self.gold // x))
        self.gold -= x * c
        self.grain += c
        if c == 0:
            x = random.randint(20, 30)
            print("Приехал торговец, очет купить зерно по " + str(x) + " золотых за мешок")
            c = max(0, min(int(input("Сколько продать зерна?")), self.gold // x))
            self.gold += x * c
            self.grain -= c

    def plant(self):
        x = int(input("Сколько зерна посадить?"))
        self.planted = max(0, min(x, self.grain))
        self.grain -= max(0, min(x, self.grain))

    def feed(self):
        x = int(input("Сколько зерна отдать народу?"))
        self.fed = max(0, min(x, self.grain))
        self.grain -= max(0, min(x, self.grain))

    def grow(self):
        self.grain += round(self.planted * random.randint(5, 100) // 10)
        self.planted = 0

    def grew(self):
        if self.year > 0:
            if self.people * 99 <= self.fed:
                self.happiness += max(2, 1 + self.fed / self.people // 99)
                self.people *= max(1.2, self.fed / self.people // 99)
            else:
                self.happiness -= 100 * (1 - self.fed / self.people // 99)
                self.chaos_rise += 100 * (1 - self.fed / self.people // 99)
                self.people *= self.fed / self.people // 99
            self.people = round(self.people)
        if self.people == 0:
            self.alive = False

    def develop(self):
        if len(self.developments):
            for i in self.developments:
                i.proceed(self)
            for i in range(len(self.developments), 0, -1):
                if self.developments[i].ended:
                    self.developments = self.developments[::i].extend(self.developments[i + 1::])

    def chaos(self):
        if self.chaos_rise > 30:
            if random.randint(0, 101) < self.chaos_rise - 30:
                self.alive = False
                print("Прорыв хаоса")
        if self.happiness < 10:
            if random.randint(0, 10) < self.happiness:
                print("БУНТ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                c = random.randint(100, 300)
                x = min(self.gold // c,
                        max(0, int(input("Мимопроезжающая компания наемников предлагает нанять солдат по " + str(
                            c) + " золотых за солдата. сколько человек нанять?"))))
                self.gold -= x * c
                if random.randint(0, self.people) > x:
                    print("Бунт подавлен")
                    self.people = self.people * random.randint(10, 100) // 100
                    self.happiness *= 0.9
                else:
                    print("Тебя свергли кровавый тиран")

    def process(self):
        self.grow()
        self.grew()
        self.status()
        self.trade()
        self.status()
        self.plant()
        self.status()
        self.feed()
        self.status()
        self.develop()
        self.eventise()
        self.chaos()
        self.year += 1

    def run(self):
        while self.alive:
            self.process()
        self.end()


game = TheGame()
game.run()
