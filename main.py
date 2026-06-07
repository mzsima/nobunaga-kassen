import random
import math

class Castle:
    def __init__(self, name, x, y, owner, troops):
        self.name = name
        self.x = x
        self.y = y
        self.owner = owner
        self.troops = troops

    def __str__(self):
        return f"[{self.name}] (Owner: {self.owner}, Troops: {self.troops})"

class Game:
    def __init__(self):
        # 初期状態の定義（名前, X, Y, 所有者, 兵数）
        initial_castles = [
            Castle("Kyoto", 0, 0, "Oda", 100),
            Castle("Osaka", 1, 0, "Oda", 80),
            Castle("Nagoya", 2, 0, "Takeda", 90),
            Castle("Inuyama", 3, 0, "Oda", 60),
            Castle("Gifu", 1, 1, "Hideyoshi", 70),
            Castle("Mino", 2, 1, "Tokugawa", 80),
        ]
        self.castles = initial_castles
        self.turn = 1

    def display_status(self):
        print(f"\n--- Turn {self.turn} ---")
        # 地図の視覚化
        print("【現在の領土状況】")
        max_x = max(c.x for c in self.castles) + 1
        max_y = max(c.y for c in self.castles) + 1
        
        for y in range(max_y):
            row = []
            for x in range(max_x):
                castle = next((c for c in self.castles if c.x == x and c.y == y), None)
                if castle:
                    # 領主の頭文字を添えて表示（例：Odaなら[Kyoto(O)]）
                    owner_init = castle.owner[0]
                    row.append(f"[{castle.name}({owner_init})]")
                else:
                    row.append("...")
            print(f"y={y} | {' '.join(row)}")
        print("-" * 30)

        for c in self.castles:
            print(c)
        print("-" * 30)

    def get_distance(self, c1, c2):
        return abs(c1.x - c2.x) + abs(c1.y - c2.y)

    def play(self):
        print("「信長の野望・ミニマム」へようこそ。")
        print("あなたの勢力は『Oda』です。領土を奪い、天下統一を目指しましょう。")
        print("操作方法: 自分の領土から隣接する座標 (x, y) を入力してください（例: move 1 0）")
        print("何もせず次のターンへ進む場合は 'pass' と入力してください。")
        input("\n準備ができたらEnterを押して開始してください...")

        while True:
            self.display_status()
            
            # 勝敗判定
            owners = set(c.owner for c in self.castles)
            if len(owners) == 1:
                print(f"【勝利】 あなたの野望が成就し、天下統一を成し遂げました！")
                break

            action = input("進軍コマンドを入力してください (例: move x y または pass): ").lower()

            if action.startswith("move"):
                try:
                    parts = action.split()
                    tx, ty = int(parts[1]), int(parts[2])
                    
                    target_castle = next((c for c in self.castles if c.x == tx and c.y == ty), None)
                    if not target_castle:
                        print("！！エラー：その座標に城は見当たりません。")
                        continue

                    source_castle = None
                    for c in self.castles:
                        if c.owner == "Oda" and self.get_distance(c, target_castle) <= 1:
                            source_castle = c
                            break
                    
                    if not source_castle:
                        print("！！警告：隣接するあなたの領地（O）から進軍してください。")
                        continue

                    # 戦闘・移動ロジック
                    if target_castle == source_castle:
                        pass
                    elif target_castle.owner == "Oda":
                        target_castle.troops += source_castle.troops
                        source_castle.troops = 0
                        print(f"【成功】 {target_castle.name} に部隊を統合しました。")
                    else:
                        # 敵への攻城
                        if source_castle.troops > target_castle.troops:
                            loss = int(target_castle.troops * 0.5)
                            target_castle.owner = "Oda"
                            target_castle.troops = source_castle.troops - loss
                            source_castle.troops = 0
                            print(f"【勝利】 {target_castle.name} を奪い取りました。")
                        else:
                            damage = source_castle.troops
                            target_castle.troops -= damage
                            source_castle.troops = 0
                            print(f"【敗北】 強敵の前に、{target_castle.name} は奪えませんでした。しかし敵に大きな打撃を与えました。")

                except (ValueError, IndexError):
                    print("！！エラー：入力形式が正しくありません。「move x y」（例: move 1 0）または「pass」と入力してください。")
            else:
                print("パスしました。次のターンへ進みます。")

            # --- 自動補給システム ---
            for c in self.castles:
                if c.owner == "Oda":
                    # 自領の拠点は毎ターン一定量（最大10%）の兵を補充する
                    supply = int(c.troops * 0.1)
                    if supply < 2: supply = 2
                    c.troops += supply

            self.turn += 1

if __name__ == "__main__":
    game = Game()
    game.play()
