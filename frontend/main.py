import flet as ft
from typing import Dict, List
from api_service import api_service
from ui_elements import (
    MenuCard, OrderSummaryPage, TableSummaryPage, 
    AlertDialog, get_category_icon
)

class RestaurantApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "ระบบสั่งอาหาร"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 10
        
        # ตั้งค่าสำหรับ tablet
        self.page.window_width = 900
        self.page.window_height = 700
        
        # ข้อมูลการสั่งอาหารแยกตามโต๊ะ
        self.orders = {
            "โต๊ะ 1": {},
            "โต๊ะ 2": {},
            "โต๊ะ 3": {},
            "โต๊ะ 4": {}
        }
        
        self.current_table = "โต๊ะ 1"
        self.menu_data = {}
        self.categories = ["เครื่องดื่ม", "อาหารจานเดียว", "ของทานเล่น", "ของหวาน"]
        self.current_page = "menu"  # menu, order_summary, table_summary
        
        # สร้าง UI helper classes
        self.order_summary_page = OrderSummaryPage(self)
        self.table_summary_page = TableSummaryPage(self)
        self.alert_dialog = AlertDialog(page)
        
        self.setup_ui()
        self.load_menu_data()
    
    def load_menu_data(self):
        """โหลดข้อมูลเมนูจาก API"""
        try:
            self.menu_data = api_service.get_menu_data()
            if self.current_page == "menu":
                self.update_menu_view()
        except Exception as e:
            self.alert_dialog.show_error("ข้อผิดพลาด", f"ไม่สามารถโหลดข้อมูลเมนูได้: {str(e)}")
    
    def setup_ui(self):
        """ตั้งค่า UI หลัก"""
        # สร้าง container สำหรับเนื้อหา
        self.content_container = ft.Container(expand=True)
        
        # เพิ่ม container ลงใน page
        self.page.add(self.content_container)
        
        # แสดงหน้าเมนู
        self.show_menu_page()
    
    def show_menu_page(self):
        """แสดงหน้าเมนูสั่งอาหาร"""
        self.current_page = "menu"
        
        # Header สำหรับเลือกโต๊ะ
        self.table_selector = ft.Dropdown(
            label="เลือกโต๊ะ",
            value=self.current_table,
            options=[ft.dropdown.Option(table) for table in self.orders.keys()],
            on_change=self.on_table_changed,
            width=150
        )
        
        # Summary buttons
        self.summary_btn = ft.ElevatedButton(
            "สรุปรายการสั่ง",
            icon=ft.Icons.RECEIPT,
            on_click=self.show_order_summary_page,
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE
        )
        
        self.table_summary_btn = ft.ElevatedButton(
            "สรุปทุกโต๊ะ",
            icon=ft.Icons.TABLE_RESTAURANT,
            on_click=self.show_table_summary_page,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE
        )
        
        header = ft.Row([
            ft.Text("ระบบสั่งอาหาร", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            self.table_selector,
            self.summary_btn,
            self.table_summary_btn
        ])
        
        # Navigation tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            on_change=self.on_tab_changed,
            tabs=[
                ft.Tab(text=category, icon=get_category_icon(category)) 
                for category in self.categories
            ]
        )
        
        # Menu content area
        self.menu_content = ft.Container(
            content=ft.Column([]),
            padding=10,
            height=500,
            expand=True
        )
        
        # สร้างเนื้อหาหน้าเมนู
        menu_page_content = ft.Column([
            header,
            self.tabs,
            self.menu_content
        ], expand=True)
        
        # อัพเดท container
        self.content_container.content = menu_page_content
        self.page.update()
        
        # โหลดเมนู
        if self.menu_data:
            self.update_menu_view()
    
    def show_order_summary_page(self, e=None):
        """แสดงหน้าสรุปรายการสั่ง"""
        self.current_page = "order_summary"
        
        table_orders = self.orders[self.current_table]
        summary_content = self.order_summary_page.create_summary_page(
            table_name=self.current_table,
            orders=table_orders,
            menu_data=self.menu_data
        )
        
        self.content_container.content = summary_content
        self.page.update()
    
    def show_table_summary_page(self, e=None):
        """แสดงหน้าสรุปรายการทุกโต๊ะ"""
        self.current_page = "table_summary"
        
        try:
            # ดึงข้อมูลสรุปจาก API
            summary_data = api_service.get_orders_summary()
            
            summary_content = self.table_summary_page.create_summary_page(summary_data)
            
            self.content_container.content = summary_content
            self.page.update()
            
        except Exception as e:
            self.alert_dialog.show_error("ข้อผิดพลาด", f"ไม่สามารถดึงข้อมูลสรุปได้: {str(e)}")
    
    def go_back_to_menu(self):
        """กลับไปหน้าเมนู"""
        self.show_menu_page()
    
    def on_table_changed(self, e):
        """เมื่อเปลี่ยนโต๊ะ"""
        self.current_table = e.control.value
        self.update_menu_view()
    
    def on_tab_changed(self, e):
        """เมื่อเปลี่ยนแท็บ"""
        self.update_menu_view()
    
    def update_menu_view(self):
        """อัพเดทการแสดงผลเมนู"""
        if not self.menu_data or self.current_page != "menu":
            return
            
        current_category = self.categories[self.tabs.selected_index]
        items = self.menu_data.get(current_category, [])
        
        # สร้าง grid สำหรับแสดงเมนู 4 คอลัมน์
        rows = []
        for i in range(0, len(items), 4):
            row_items = items[i:i+4]
            row = ft.Row(
                controls=[self.create_menu_card(item) for item in row_items],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                spacing=10
            )
            rows.append(row)
        
        self.menu_content.content = ft.Column(
            controls=rows,
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )
        self.page.update()
    
    def create_menu_card(self, item):
        """สร้าง card สำหรับแต่ละรายการอาหาร"""
        item_id = item["id"]
        current_qty = self.orders[self.current_table].get(item_id, 0)
        
        menu_card = MenuCard(
            item=item,
            current_qty=current_qty,
            on_qty_changed=self.on_qty_changed,
            on_increase=self.increase_qty,
            on_decrease=self.decrease_qty
        )
        
        return menu_card.create_card()
    
    def on_qty_changed(self, e, item_id):
        """เมื่อจำนวนถูกเปลี่ยน"""
        try:
            qty = int(e.control.value) if e.control.value.isdigit() else 0
            if qty < 0:
                qty = 0
                e.control.value = "0"
            
            if qty == 0:
                self.orders[self.current_table].pop(item_id, None)
            else:
                self.orders[self.current_table][item_id] = qty
            
            self.page.update()
        except:
            e.control.value = "0"
            self.orders[self.current_table].pop(item_id, None)
            self.page.update()
    
    def increase_qty(self, item_id):
        """เพิ่มจำนวน"""
        current_qty = self.orders[self.current_table].get(item_id, 0)
        self.orders[self.current_table][item_id] = current_qty + 1
        self.update_menu_view()
    
    def decrease_qty(self, item_id):
        """ลดจำนวน"""
        current_qty = self.orders[self.current_table].get(item_id, 0)
        if current_qty > 0:
            if current_qty == 1:
                self.orders[self.current_table].pop(item_id, None)
            else:
                self.orders[self.current_table][item_id] = current_qty - 1
            self.update_menu_view()
    
    def clear_current_order(self):
        """ยกเลิกรายการสั่งอาหารทั้งหมดของโต๊ะปัจจุบัน"""
        def confirm_clear():
            self.orders[self.current_table] = {}
            # กลับไปหน้าเมนูและรีเฟรช
            self.show_menu_page()
        
        self.alert_dialog.show_confirmation(
            "ยืนยันการยกเลิก",
            f"ต้องการยกเลิกรายการสั่งทั้งหมดของ{self.current_table}?",
            confirm_clear
        )
    
    def submit_current_order(self):
        """ส่งรายการสั่งอาหารไปยัง API"""
        table_orders = self.orders[self.current_table]
        
        if not table_orders:
            self.alert_dialog.show_error("แจ้งเตือน", "ไม่มีรายการที่จะส่ง")
            return
        
        try:
            # ส่ง order ไป API
            success = api_service.submit_order(self.current_table, table_orders)
            
            if success:
                # ล้าง order ที่ส่งแล้ว
                self.orders[self.current_table] = {}
                
                # แสดงข้อความสำเร็จและกลับไปหน้าเมนู
                def go_back():
                    self.show_menu_page()
                
                self.alert_dialog.show_success(
                    "สำเร็จ", 
                    f"ส่งรายการสั่งของ{self.current_table}เรียบร้อยแล้ว!"
                )
                
                # กลับหน้าเมนูหลังจาก 2 วินาที
                import threading
                threading.Timer(2.0, go_back).start()
                
            else:
                self.alert_dialog.show_error("ข้อผิดพลาด", "ไม่สามารถส่งรายการสั่งได้")
                
        except Exception as e:
            self.alert_dialog.show_error("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการส่งรายการ: {str(e)}")

    def find_item_by_id(self, item_id: int):
        """ค้นหาข้อมูลเมนูจาก ID"""
        for category_items in self.menu_data.values():
            for item in category_items:
                if item["id"] == item_id:
                    return item
        return None

def main(page: ft.Page):
    app = RestaurantApp(page)

if __name__ == "__main__":
    ft.app(target=main)