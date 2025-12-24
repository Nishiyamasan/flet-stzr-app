import flet as ft

def main(page: ft.Page):
    page.title = "究極・ストゼロチェッカー v2.1"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    # ウィンドウサイズ設定（デスクトップ実行時用）
    page.window_width = 450
    page.window_height = 800
    
    # --- UI Components ---
    
    # 結果表示用カード（修正ポイント：Containerからelevationを削除）
    result_container = ft.Container(
        content=ft.Column([
            ft.Text("診断結果", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            result_main := ft.Text("数値を入力して計算してください", size=16),
            result_sub := ft.Text("", size=14, color=ft.Colors.GREY_700),
        ]),
        padding=15,
        border_radius=12,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.BLUE_GREY_100), # elevationの代わりに枠線で表現
        visible=False
    )

    water_container = ft.Container(
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.WATER_DROP, color=ft.Colors.BLUE), ft.Text("推奨水分補給量", weight="bold")]),
            water_text1 := ft.Text("", size=14),
            water_text2 := ft.Text("", size=14),
        ]),
        padding=15,
        border_radius=12,
        bgcolor=ft.Colors.BLUE_50,
        visible=False
    )

    def create_input_group(label_text):
        return {
            "vol": ft.TextField(label="容量(ml)", value="350", suffix_text="ml", keyboard_type=ft.KeyboardType.NUMBER, expand=True),
            "price": ft.TextField(label="価格(円)", value="150", suffix_text="円", keyboard_type=ft.KeyboardType.NUMBER, expand=True),
            "alc": ft.TextField(label="度数(%)", value="9", suffix_text="%", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
        }

    item1 = create_input_group("エントリー1")
    item2 = create_input_group("エントリー2")

    # --- Logic ---
    def calculate(e):
        try:
            items_data = []
            for item in [item1, item2]:
                v = float(item["vol"].value)
                p = float(item["price"].value)
                a = float(item["alc"].value)
                
                # 純アルコール量(g) = 容量(ml) × (度数/100) × 0.8
                pure_alc_g = v * (a / 100) * 0.8
                # アルコール1gあたりの単価
                cost_per_alc = p / pure_alc_g if pure_alc_g > 0 else 0
                # 必要水分量（純アルコールmlの約15倍）
                needed_water = (v * (a / 100)) * 15
                
                items_data.append({
                    "cost": cost_per_alc,
                    "alc_g": pure_alc_g,
                    "water": needed_water
                })

            d1, d2 = items_data[0], items_data[1]
            
            # 比較判定
            if d1["cost"] < d2["cost"]:
                winner = "エントリー【1】"
                result_container.bgcolor = ft.Colors.GREEN_50
            elif d2["cost"] < d1["cost"]:
                winner = "エントリー【2】"
                result_container.bgcolor = ft.Colors.ORANGE_50
            else:
                winner = "引き分け"
                result_container.bgcolor = ft.Colors.WHITE

            result_main.value = f"🎉 {winner} が高コスパ！" if winner != "引き分け" else "⚖️ どちらも同じコスパです"
            result_sub.value = (
                f"1の単価: {d1['cost']:.2f} 円/g (純アルコール {d1['alc_g']:.1f}g)\n"
                f"2の単価: {d2['cost']:.2f} 円/g (純アルコール {d2['alc_g']:.1f}g)"
            )
            
            water_text1.value = f"🥤 1を飲むなら: 水 {d1['water']:.0f}ml が必要"
            water_text2.value = f"🥤 2を飲むなら: 水 {d2['water']:.0f}ml が必要"
            
            result_container.visible = True
            water_container.visible = True
            
        except ValueError:
            result_main.value = "⚠️ 半角数字で入力してください"
            result_main.color = ft.Colors.RED
            result_container.visible = True
            water_container.visible = False
        
        page.update()

    # --- View ---
    page.add(
        ft.AppBar(
            title=ft.Text("ストゼロ・コスパ・健康くん", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.INDIGO_700,
            center_title=True
        ),
        ft.Column([
            ft.Text("🛒 比較するお酒を入力", size=18, weight="bold"),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("エントリー 1", weight="bold", color=ft.Colors.INDIGO),
                    ft.Row([item1["vol"], item1["price"], item1["alc"]]),
                ]),
                padding=10, border=ft.border.all(1, ft.Colors.BLUE_GREY_100), border_radius=8
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("エントリー 2", weight="bold", color=ft.Colors.INDIGO),
                    ft.Row([item2["vol"], item2["price"], item2["alc"]]),
                ]),
                padding=10, border=ft.border.all(1, ft.Colors.BLUE_GREY_100), border_radius=8
            ),

            ft.ElevatedButton(
                "コスパと健康をチェック",
                on_click=calculate,
                icon=ft.Icons.CALCULATE,
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.INDIGO_600,
                ),
                width=400,
                height=50
            ),
            
            result_container,
            water_container,
            
            ft.Text("※純アルコール量は比重0.8で計算。水は分解に必要な目安量です。", size=12, color=ft.Colors.GREY_600)
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
    )

ft.app(target=main)