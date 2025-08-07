import requests
import json
from typing import Dict, List, Optional

class APIService:
    """Class สำหรับจัดการการเรียก API ทั้งหมด"""
    
    def __init__(self, base_url: str = "http://localhost:5000/api"):
        self.base_url = base_url
    
    def get_menu_data(self) -> Dict:
        """ดึงข้อมูลเมนูทั้งหมดจาก API"""
        try:
            response = requests.get(f"{self.base_url}/menu/all")
            if response.status_code == 200:
                data = response.json()
                return data.get("data", {})
            else:
                raise Exception(f"API Error: {response.status_code}")
        except requests.RequestException as e:
            raise Exception(f"Network Error: {str(e)}")
    
    def get_menu_by_category(self, category: str) -> List[Dict]:
        """ดึงข้อมูลเมนูตามหมวดหมู่"""
        try:
            response = requests.get(f"{self.base_url}/menu/{category}")
            if response.status_code == 200:
                data = response.json()
                return data.get("items", [])
            else:
                raise Exception(f"API Error: {response.status_code}")
        except requests.RequestException as e:
            raise Exception(f"Network Error: {str(e)}")
    
    def submit_order(self, table_name: str, items: Dict[int, int]) -> bool:
        """ส่ง order ไปยัง API"""
        try:
            order_data = {
                "table_name": table_name,
                "items": items
            }
            
            response = requests.post(
                f"{self.base_url}/orders", 
                json=order_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("success", False)
            else:
                raise Exception(f"API Error: {response.status_code}")
                
        except requests.RequestException as e:
            raise Exception(f"Network Error: {str(e)}")
    
    def get_orders_summary(self) -> Dict:
        """ดึงสรุปรายการสั่งของทุกโต๊ะ"""
        try:
            response = requests.get(f"{self.base_url}/orders/summary")
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"API Error: {response.status_code}")
        except requests.RequestException as e:
            raise Exception(f"Network Error: {str(e)}")
    
    def get_order_by_table(self, table_name: str) -> Optional[Dict]:
        """ดึงข้อมูล order ของโต๊ะที่ระบุ"""
        try:
            response = requests.get(f"{self.base_url}/orders/{table_name}")
            if response.status_code == 200:
                data = response.json()
                return data.get("order")
            elif response.status_code == 404:
                return None
            else:
                raise Exception(f"API Error: {response.status_code}")
        except requests.RequestException as e:
            raise Exception(f"Network Error: {str(e)}")
    
    def get_all_orders(self) -> List[Dict]:
        """ดึงรายการ order ทั้งหมด"""
        try:
            response = requests.get(f"{self.base_url}/orders")
            if response.status_code == 200:
                data = response.json()
                return data.get("orders", [])
            else:
                raise Exception(f"API Error: {response.status_code}")
        except requests.RequestException as e:
            raise Exception(f"Network Error: {str(e)}")

# Singleton instance
api_service = APIService()