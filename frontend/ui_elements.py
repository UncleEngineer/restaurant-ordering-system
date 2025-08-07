import flet as ft
from typing import Dict, List, Callable, Optional

class MenuCard:
    """Class สำหรับสร้าง Card เมนูอาหาร"""
    
    def __init__(self, item: Dict, current_qty: int, 
                 on_qty_changed: Callable, 
                 on_increase: Callable, 
                 on_decrease: Callable):
        self.item = item
        self.current_qty = current_qty
        self.on_qty_changed = on_qty_changed
        self.on_increase = on_increase
        self.on_decrease = on_decrease
        
    def create_card(self) -> ft.Card:
        """สร้าง card สำหรับแสดงเมนู"""
        item_id = self.item["id"]
        
        # Text field สำหรับจำนวน
        qty_field = ft.TextField(
            value=str(self.current_qty),
            width=80,
            height=40,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=lambda e: self.on_qty_changed(e, item_id)
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    # รูปภาพ
                    ft.Container(
                        content=ft.Image(
                            src=self.item["image"],
                            width=120,
                            height=80,
                            fit=ft.ImageFit.COVER,
                            error_content=ft.Icon(ft.Icons.IMAGE, size=40)
                        ),
                        bgcolor=ft.Colors.GREY_200,
                        border_radius=5
                    ),
                    # ชื่อเมนู
                    ft.Text(
                        self.item["name"],
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=2
                    ),
                    # ราคา
                    ft.Text(
                        f"฿{self.item['price']}",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_700,
                        text_align=ft.TextAlign.CENTER
                    ),
                    # TextField สำหรับจำนวน
                    ft.Container(
                        content=qty_field,
                        alignment=ft.alignment.center
                    ),
                    # ปุ่ม + และ -
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.REMOVE,
                            icon_size=16,
                            on_click=lambda e: self.on_decrease(item_id),
                            bgcolor=ft.Colors.RED_100,
                            icon_color=ft.Colors.RED_700
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            icon_size=16,
                            on_click=lambda e: self.on_increase(item_id),
                            bgcolor=ft.Colors.GREEN_100,
                            icon_color=ft.Colors.GREEN_700
                        )
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5)
                ], 
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=10,
                width=150
            ),
            elevation=2
        )

class OrderSummaryPage:
    """Class สำหรับสร้างหน้าสรุปรายการสั่ง"""
    
    def __init__(self, app):
        self.app = app
    
    def create_summary_page(self, table_name: str, orders: Dict, menu_data: Dict) -> ft.Column:
        """สร้างหน้าสรุปรายการสั่ง"""
        
        # Header พร้อมปุ่ม Back
        header = ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_size=30,
                on_click=lambda e: self.app.go_back_to_menu(),
                tooltip="กลับไปหน้าเมนู"
            ),
            ft.Text(f"สรุปรายการสั่ง - {table_name}", 
                   size=24, 
                   weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
        ])
        
        if not orders:
            # ถ้าไม่มีรายการสั่ง
            empty_content = ft.Column([
                header,
                ft.Container(height=50),
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.RESTAURANT_MENU, size=100, color=ft.Colors.GREY_400),
                        ft.Text("ยังไม่มีรายการสั่งอาหารสำหรับโต๊ะนี้", 
                               size=18, 
                               color=ft.Colors.GREY_600,
                               text_align=ft.TextAlign.CENTER),
                        ft.Container(height=30),
                        ft.ElevatedButton(
                            "กลับไปเลือกเมนู",
                            icon=ft.Icons.RESTAURANT,
                            on_click=lambda e: self.app.go_back_to_menu(),
                            bgcolor=ft.Colors.BLUE,
                            color=ft.Colors.WHITE
                        )
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ], expand=True)
            
            return empty_content
        
        # สร้างรายการสรุป
        summary_items = []
        total_price = 0
        total_items = 0
        
        for item_id, qty in orders.items():
            item_info = self.find_item_by_id(item_id, menu_data)
            if item_info:
                subtotal = item_info["price"] * qty
                total_price += subtotal
                total_items += qty
                
                item_row = ft.Container(
                    content=ft.Row([
                        # รูปภาพเมนู
                        ft.Container(
                            content=ft.Image(
                                src=item_info["image"],
                                width=60,
                                height=45,
                                fit=ft.ImageFit.COVER,
                                error_content=ft.Icon(ft.Icons.IMAGE, size=20)
                            ),
                            border_radius=5
                        ),
                        ft.Container(width=10),
                        # ชื่อเมนู
                        ft.Column([
                            ft.Text(item_info["name"], 
                                   weight=ft.FontWeight.BOLD, 
                                   size=16),
                            ft.Text(f"฿{item_info['price']} x {qty}", 
                                   color=ft.Colors.GREY_600,
                                   size=14)
                        ], expand=True, spacing=2),
                        # ราคารวม
                        ft.Text(f"฿{subtotal}", 
                               size=16, 
                               weight=ft.FontWeight.BOLD,
                               color=ft.Colors.GREEN_700)
                    ], alignment=ft.MainAxisAlignment.START),
                    padding=15,
                    margin=ft.margin.symmetric(vertical=5),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=3,
                        color=ft.Colors.GREY_300,
                        offset=ft.Offset(0, 2)
                    )
                )
                summary_items.append(item_row)
        
        # สรุปยอดรวม
        summary_total = ft.Container(
            content=ft.Column([
                ft.Divider(color=ft.Colors.GREY_400, thickness=2),
                ft.Row([
                    ft.Text("จำนวนรายการ:", size=16),
                    ft.Container(expand=True),
                    ft.Text(f"{len(orders)} เมนู ({total_items} ชิ้น)", 
                           size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Row([
                    ft.Text("รวมทั้งสิ้น:", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.Text(f"฿{total_price}", 
                           size=20, 
                           weight=ft.FontWeight.BOLD, 
                           color=ft.Colors.RED)
                ])
            ], spacing=10),
            padding=20,
            margin=ft.margin.symmetric(vertical=10),
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10
        )
        
        # ปุ่มต่างๆ
        action_buttons = ft.Row([
            ft.ElevatedButton(
                "ยกเลิกรายการ",
                icon=ft.Icons.DELETE,
                on_click=lambda e: self.app.clear_current_order(),
                bgcolor=ft.Colors.RED,
                color=ft.Colors.WHITE,
                expand=True
            ),
            ft.Container(width=10),
            ft.ElevatedButton(
                "ส่งออเดอร์",
                icon=ft.Icons.SEND,
                on_click=lambda e: self.app.submit_current_order(),
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.WHITE,
                expand=True
            )
        ], spacing=10)
        
        # สร้างหน้าสมบูรณ์
        content = ft.Column([
            header,
            ft.Container(height=20),
            ft.Container(
                content=ft.Column([
                    ft.Column(
                        summary_items, 
                        scroll=ft.ScrollMode.AUTO,
                        height=350
                    ),
                    summary_total,
                    action_buttons
                ], spacing=10),
                padding=20
            )
        ], expand=True)
        
        return content
    
    def find_item_by_id(self, item_id: int, menu_data: Dict) -> Optional[Dict]:
        """ค้นหาข้อมูลเมนูจาก ID"""
        for category_items in menu_data.values():
            for item in category_items:
                if item["id"] == item_id:
                    return item
        return None

class TableSummaryPage:
    """Class สำหรับแสดงหน้าสรุปรายการทุกโต๊ะ"""
    
    def __init__(self, app):
        self.app = app
    
    def create_summary_page(self, orders_summary: Dict) -> ft.Column:
        """สร้างหน้าสรุปรายการทุกโต๊ะ"""
        
        # Header พร้อมปุ่ม Back
        header = ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_size=30,
                on_click=lambda e: self.app.go_back_to_menu(),
                tooltip="กลับไปหน้าเมนู"
            ),
            ft.Text("📊 สรุปรายการทุกโต๊ะ", 
                   size=24, 
                   weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            ft.IconButton(
                icon=ft.Icons.REFRESH,
                icon_size=25,
                on_click=lambda e: self.app.show_table_summary_page(),
                tooltip="รีเฟรชข้อมูล",
                bgcolor=ft.Colors.BLUE_100
            )
        ])
        
        if not orders_summary.get("summary"):
            # ถ้าไม่มีรายการสั่ง
            empty_content = ft.Column([
                header,
                ft.Container(height=50),
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.TABLE_RESTAURANT, size=100, color=ft.Colors.GREY_400),
                        ft.Text("ยังไม่มีรายการสั่งอาหาร", 
                               size=18, 
                               color=ft.Colors.GREY_600,
                               text_align=ft.TextAlign.CENTER),
                        ft.Container(height=30),
                        ft.ElevatedButton(
                            "กลับไปหน้าเมนู",
                            icon=ft.Icons.RESTAURANT,
                            on_click=lambda e: self.app.go_back_to_menu(),
                            bgcolor=ft.Colors.BLUE,
                            color=ft.Colors.WHITE
                        )
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ], expand=True)
            
            return empty_content
        
        # สร้างตารางข้อมูล
        table_rows = []
        
        # หัวตาราง
        header_row = ft.Container(
            content=ft.Row([
                ft.Container(ft.Text("โต๊ะ", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), width=80),
                ft.Container(ft.Text("เมนู", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), width=70),
                ft.Container(ft.Text("ชิ้น", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), width=70),
                ft.Container(ft.Text("ราคา", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), width=100),
                ft.Container(ft.Text("เวลา", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), width=120),
                ft.Container(ft.Text("สถานะ", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), width=100),
            ]),
            bgcolor=ft.Colors.BLUE_700,
            padding=15,
            border_radius=ft.border_radius.only(top_left=10, top_right=10)
        )
        table_rows.append(header_row)
        
        # แถวข้อมูล
        for table_name, data in orders_summary["summary"].items():
            status_text = "เสร็จแล้ว" if data["status"] == "completed" else "กำลังทำ"
            status_color = ft.Colors.GREEN if data["status"] == "completed" else ft.Colors.ORANGE_600
            
            # แสดงเฉพาะเวลา (ไม่แสดงวันที่)
            time_display = data["timestamp"].split(" ")[1] if " " in data["timestamp"] else data["timestamp"]
            
            row = ft.Container(
                content=ft.Row([
                    ft.Container(ft.Text(table_name, weight=ft.FontWeight.BOLD), width=80),
                    ft.Container(ft.Text(f"{data['items_count']}"), width=70),
                    ft.Container(ft.Text(f"{data['total_items']}"), width=70),
                    ft.Container(ft.Text(f"฿{data['total_price']}", weight=ft.FontWeight.BOLD), width=100),
                    ft.Container(ft.Text(time_display, size=12), width=120),
                    ft.Container(
                        ft.Text(status_text, color=status_color, weight=ft.FontWeight.BOLD), 
                        width=100
                    ),
                ]),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300))
            )
            table_rows.append(row)
        
        # แถวรวม
        grand_total_row = ft.Container(
            content=ft.Row([
                ft.Container(ft.Text("รวมทั้งสิ้น", weight=ft.FontWeight.BOLD), width=320),
                ft.Container(
                    ft.Text(f"฿{orders_summary['grand_total']}", 
                           weight=ft.FontWeight.BOLD, 
                           color=ft.Colors.RED,
                           size=18), 
                    width=220
                ),
            ]),
            bgcolor=ft.Colors.GREEN_50,
            padding=15,
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
        )
        table_rows.append(grand_total_row)
        
        # สร้างตาราง
        table_container = ft.Container(
            content=ft.Column(table_rows, spacing=0),
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.GREY_400,
                offset=ft.Offset(0, 2)
            )
        )
        
        # สร้างหน้าสมบูรณ์
        content = ft.Column([
            header,
            ft.Container(height=20),
            ft.Container(
                content=ft.Column([
                    table_container,
                    ft.Container(height=20),
                    # ปุ่มกลับ
                    ft.Row([
                        ft.ElevatedButton(
                            "กลับไปหน้าเมนู",
                            icon=ft.Icons.RESTAURANT_MENU,
                            on_click=lambda e: self.app.go_back_to_menu(),
                            bgcolor=ft.Colors.BLUE,
                            color=ft.Colors.WHITE,
                            expand=True
                        )
                    ])
                ], scroll=ft.ScrollMode.AUTO),
                padding=20,
                expand=True
            )
        ], expand=True)
        
        return content

class AlertDialog:
    """Class สำหรับสร้าง Alert Dialog ทั่วไป"""
    
    def __init__(self, page: ft.Page):
        self.page = page
    
    def show_error(self, title: str, message: str):
        """แสดง error dialog"""
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[ft.TextButton("ตกลง", on_click=lambda e: self.close_dialog(dlg))]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def show_success(self, title: str, message: str):
        """แสดง success dialog"""
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[ft.TextButton("ตกลง", on_click=lambda e: self.close_dialog(dlg))]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def show_confirmation(self, title: str, message: str, on_confirm: Callable):
        """แสดง confirmation dialog"""
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("ยกเลิก", on_click=lambda e: self.close_dialog(dlg)),
                ft.TextButton("ตกลง", on_click=lambda e: [on_confirm(), self.close_dialog(dlg)])
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def close_dialog(self, dialog):
        """ปิด dialog"""
        dialog.open = False
        self.page.update()

def get_category_icon(category: str) -> str:
    """กำหนดไอคอนสำหรับแต่ละหมวดหมู่"""
    icons = {
        "เครื่องดื่ม": ft.Icons.LOCAL_DRINK,
        "อาหารจานเดียว": ft.Icons.RESTAURANT,
        "ของทานเล่น": ft.Icons.FASTFOOD,
        "ของหวาน": ft.Icons.CAKE
    }
    return icons.get(category, ft.Icons.RESTAURANT)