import flet as ft

def main(page: ft.Page):
    page.title = "ストゼロ・コスパチェッカー"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # フォントサイズなどの設定
    result_text = ft.Text(size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600)

    # 入力フィールドの作成
    vol1 = ft.TextField(label="1. 容量 (ml)", value="350", keyboard_type=ft.KeyboardType.NUMBER)
    price1 = ft.TextField(label="1. 価格 (円)", value="150", keyboard_type=ft.KeyboardType.NUMBER)
    
    vol2 = ft.TextField(label="2. 容量 (ml)", value="500", keyboard_type=ft.KeyboardType.NUMBER)
    price2 = ft.TextField(label="2. 価格 (円)", value="330", keyboard_type=ft.KeyboardType.NUMBER)

    def compare_cost(e):
        try:
            # 単価（1mlあたりの価格）を計算
            unit_price1 = float(price1.value) / float(vol1.value)
            unit_price2 = float(price2.value) / float(vol2.value)

            if unit_price1 < unit_price2:
                diff = (unit_price2 - unit_price1) * float(vol1.value)
                result_text.value = f"結果：【1】の方がお得です！\n(2より1mlあたり {unit_price2 - unit_price1:.2f}円安い)"
                result_text.color = ft.Colors.GREEN_600
            elif unit_price2 < unit_price1:
                result_text.value = f"結果：【2】の方がお得です！\n(1より1mlあたり {unit_price1 - unit_price2:.2f}円安い)"
                result_text.color = ft.Colors.ORANGE_600
            else:
                result_text.value = "結果：どちらも同じコスパです！"
                result_text.color = ft.Colors.BLUE_600
        except Exception:
            result_text.value = "数値を正しく入力してください"
            result_text.color = ft.Colors.RED_600
        
        page.update()

    # 画面への配置
    page.add(
        ft.AppBar(title=ft.Text("ストゼロ計算機"), bgcolor="bluegrey100"),
        ft.Column([
            ft.Text("エントリー1", weight="bold"),
            ft.Row([vol1, price1]),
            ft.Divider(),
            ft.Text("エントリー2", weight="bold"),
            ft.Row([vol2, price2]),
            ft.ElevatedButton("コスパを比較する", on_click=compare_cost, icon=ft.Icons.CALCULATE),
            ft.Container(content=result_text, padding=20)
        ], scroll=ft.ScrollMode.AUTO)
    )

# デスクトップで開く場合はこちら
ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550, host="localhost")
#ft.app(target=main, view=ft.AppView.WEB_BROWSER, share=True)
