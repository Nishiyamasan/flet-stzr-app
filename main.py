import flet as ft

def main(page: ft.Page):
    page.title = "究極・ストゼロチェッカー"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    
    # 結果表示用テキスト（マークダウン対応）
    result_text = ft.Text(size=16, color=ft.Colors.BLACK87)
    water_text = ft.Text(size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)

    # 入力フィールドの作成（度数を追加）
    def create_input(label, default_vol, default_price, default_alc):
        return {
            "vol": ft.TextField(label=f"{label} 容量(ml)", value=default_vol, keyboard_type=ft.KeyboardType.NUMBER, expand=True),
            "price": ft.TextField(label="価格(円)", value=default_price, keyboard_type=ft.KeyboardType.NUMBER, expand=True),
            "alc": ft.TextField(label="度数(%)", value=default_alc, keyboard_type=ft.KeyboardType.NUMBER, expand=True)
        }

    item1 = create_input("エントリー1", "350", "150", "9")
    item2 = create_input("エントリー2", "500", "250", "9")

    def compare_cost(e):
        try:
            # アイテム1の計算
            v1 = float(item1["vol"].value)
            p1 = float(item1["price"].value)
            a1 = float(item1["alc"].value)
            pure_alc1 = v1 * (a1 / 100) # 純アルコール量(ml)
            cost_per_alc1 = p1 / pure_alc1 if pure_alc1 > 0 else 0

            # アイテム2の計算
            v2 = float(item2["vol"].value)
            p2 = float(item2["price"].value)
            a2 = float(item2["alc"].value)
            pure_alc2 = v2 * (a2 / 100)
            cost_per_alc2 = p2 / pure_alc2 if pure_alc2 > 0 else 0

            # コスパ比較（アルコール1mlあたりの安さ）
            if cost_per_alc1 < cost_per_alc2:
                res = "【1】の方がアルコール効率が良いです！"
                color = ft.Colors.GREEN_700
            elif cost_per_alc2 < cost_per_alc1:
                res = "【2】の方がアルコール効率が良いです！"
                color = ft.Colors.ORANGE_700
            else:
                res = "どちらもアルコールコスパは同じです。"
                color = ft.Colors.BLUE_700

            result_text.value = (
                f"{res}\n"
                f"1のアルコール単価: {cost_per_alc1:.2f} 円/ml\n"
                f"2のアルコール単価: {cost_per_alc2:.2f} 円/ml"
            )
            result_text.color = color

            # 水分補給量の計算（アルコール量の約15倍を推奨とする場合）
            # アルコール度数9% 500mlなら 45mlのアルコール → 約675mlの水が必要
            # needed_water = pure_alc1 * 15 # エントリー1を飲んだ場合
            # water_text.value = f"⚠️ エントリー1を飲むなら、水 {needed_water:.0f}ml も一緒に飲みましょう！"

            # 1. アルコール度数(a1)を使って、純アルコール量(ml)を正確に計算
            v1 = float(item1["vol"].value)
            a1 = float(item1["alc"].value)
            pure_alc1 = v1 * (a1 / 100)  # ここで入力された度数を使用

            # 2. 算出した純アルコール量に基づいて、必要な水分量を計算
            # 一般的に、アルコールを分解するのに「アルコール量の約10〜15倍」の水が必要と言われます
            needed_water = pure_alc1 * 15 



            # 1. アルコール度数(a1)を使って、純アルコール量(ml)を正確に計算
            v2 = float(item2["vol"].value)
            a2 = float(item2["alc"].value)
            pure_alc2 = v2 * (a2 / 100)  # ここで入力された度数を使用

            # 2. 算出した純アルコール量に基づいて、必要な水分量を計算
            # 一般的に、アルコールを分解するのに「アルコール量の約10〜15倍」の水が必要と言われます
            needed_water1 = pure_alc1 * 15 
            needed_water2 = pure_alc2 * 15 
            # 表示を更新
            water_text.value = f"⚠️ エントリー1({a1}% {v1}ml)を飲むなら、\n水 {needed_water1:.0f}ml も一緒に飲みましょう！" 
            water_text.value = water_text.value + f"\n⚠️ エントリー2({a2}% {v2}ml)を飲むなら、\n水 {needed_water2:.0f}ml も一緒に飲みましょう！"
            

        except Exception:
            result_text.value = "数値を正しく入力してください"
            result_text.color = ft.Colors.RED_600
        
        page.update()

    # 画面構成
    page.add(
        ft.AppBar(title=ft.Text("ストゼロ・健康チェッカー"), bgcolor=ft.Colors.BLUE_GREY_100),
        ft.Column([
            ft.Text("エントリー1", weight="bold"),
            ft.Row([item1["vol"], item1["price"], item1["alc"]]),
            ft.Divider(),
            ft.Text("エントリー2", weight="bold"),
            ft.Row([item2["vol"], item2["price"], item2["alc"]]),
            ft.ElevatedButton("コスパと健康をチェック", on_click=compare_cost, icon=ft.Icons.CALCULATE, width=300),
            ft.Container(
                content=ft.Column([result_text, water_text]),
                padding=20,
                border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                border_radius=10
            )
        ], scroll=ft.ScrollMode.AUTO)
    )

ft.app(target=main)
