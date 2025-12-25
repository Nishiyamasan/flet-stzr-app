import flet as ft

def main(page: ft.Page):
    # --- Page Settings ---
    page.title = "究極・ストゼロチェッカー v3.0"
    page.theme = ft.Theme(color_scheme_seed="indigo")
    page.dark_theme = ft.Theme(color_scheme_seed="indigo")
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 15
    page.window_width = 450
    page.window_height = 800

    # --- UI Components ---
    result_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.EMOJI_EVENTS),
                    ft.Text("診断結果", size=20, weight=ft.FontWeight.BOLD)
                ]),
                ft.Divider(),
                result_main := ft.Text("数値を入力して計算してください", size=16),
                result_sub := ft.Text("", size=14),
            ]),
            padding=15,
        ),
        visible=False
    )

    water_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.WATER_DROP), ft.Text("推奨水分補給量", weight="bold")]),
                water_text1 := ft.Text("", size=14),
                water_text2 := ft.Text("", size=14),
            ]),
            padding=15,
        ),
        visible=False
    )

    def create_input_group(label_text):
        return {
            "vol": ft.TextField(label="容量", value="350", suffix_text="ml", keyboard_type=ft.KeyboardType.NUMBER, expand=True),
            "price": ft.TextField(label="価格", value="150", suffix_text="円", keyboard_type=ft.KeyboardType.NUMBER, expand=True),
            "alc": ft.TextField(label="度数", value="9", suffix_text="%", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
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
                
                pure_alc_g = v * (a / 100) * 0.8
                cost_per_alc = p / pure_alc_g if pure_alc_g > 0 else 0
                needed_water = (v * (a / 100)) * 15
                
                items_data.append({
                    "cost": cost_per_alc,
                    "alc_g": pure_alc_g,
                    "water": needed_water
                })

            d1, d2 = items_data[0], items_data[1]
            
            if d1["cost"] < d2["cost"]:
                winner = "エントリー【1】"
                result_card.content.bgcolor = page.theme.color_scheme.primary_container
            elif d2["cost"] < d1["cost"]:
                winner = "エントリー【2】"
                result_card.content.bgcolor = page.theme.color_scheme.secondary_container
            else:
                winner = "引き分け"
                result_card.content.bgcolor = None

            result_main.value = f"🎉 {winner} が高コスパ！" if winner != "引き分け" else "⚖️ どちらも同じコスパです"
            result_sub.value = (
                f"1の単価: {d1['cost']:.2f} 円/g (純アルコール {d1['alc_g']:.1f}g)\n"
                f"2の単価: {d2['cost']:.2f} 円/g (純アルコール {d2['alc_g']:.1f}g)"
            )
            
            water_text1.value = f"🥤 1を飲むなら: 水 {d1['water']:.0f}ml が必要"
            water_text2.value = f"🥤 2を飲むなら: 水 {d2['water']:.0f}ml が必要"
            
            result_card.visible = True
            water_card.visible = True
            
        except (ValueError, ZeroDivisionError):
            result_main.value = "⚠️ 正しい半角数字を入力してください"
            result_main.color = page.theme.color_scheme.error
            result_sub.value = ""
            result_card.content.bgcolor = None
            result_card.visible = True
            water_card.visible = False
        
        page.update()

    # --- View ---
    page.add(
        ft.AppBar(
            title=ft.Text("ストゼロ・コスパ・健康くん"),
            center_title=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
        ),
        ft.Column([
            ft.Text("🛒 比較するお酒を入力", size=18, weight="bold"),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("エントリー 1", weight="bold"),
                        ft.Row([item1["vol"], item1["price"], item1["alc"]]),
                    ]),
                    padding=15
                )
            ),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("エントリー 2", weight="bold"),
                        ft.Row([item2["vol"], item2["price"], item2["alc"]]),
                    ]),
                    padding=15
                )
            ),

            ft.FilledButton(
                "コスパと健康をチェック",
                on_click=calculate,
                icon=ft.Icons.CALCULATE,
                height=50
            ),
            
            result_card,
            water_card,
            
            ft.Text("※純アルコール量は比重0.8で計算。水は分解に必要な目安量です。", size=12, italic=True)
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
    )

ft.app(target=main)
