from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# ข้อมูลเมนูแต่ละหมวดหมู่
menu_data = {
    "เครื่องดื่ม": [
        {"id": 1, "name": "ชาเขียวเย็น", "price": 35, "image": "https://via.placeholder.com/200x150/4CAF50/white?text=ชาเขียวเย็น"},
        {"id": 2, "name": "กาแฟเย็น", "price": 40, "image": "https://via.placeholder.com/200x150/8D6E63/white?text=กาแฟเย็น"},
        {"id": 3, "name": "น้ำส้มคั้นสด", "price": 45, "image": "https://via.placeholder.com/200x150/FF9800/white?text=น้ำส้มคั้น"},
        {"id": 4, "name": "โค้กเย็น", "price": 25, "image": "https://via.placeholder.com/200x150/F44336/white?text=โค้ก"},
        {"id": 5, "name": "น้ำแข็งใส", "price": 15, "image": "https://via.placeholder.com/200x150/2196F3/white?text=น้ำแข็งใส"},
        {"id": 6, "name": "ชาดำเย็น", "price": 30, "image": "https://via.placeholder.com/200x150/795548/white?text=ชาดำเย็น"},
        {"id": 7, "name": "น้ำมะนาวโซดา", "price": 35, "image": "https://via.placeholder.com/200x150/CDDC39/white?text=มะนาวโซดา"},
        {"id": 8, "name": "กาแฟร้อน", "price": 35, "image": "https://via.placeholder.com/200x150/6D4C41/white?text=กาแฟร้อน"},
        {"id": 9, "name": "ชาไทยเย็น", "price": 40, "image": "https://via.placeholder.com/200x150/FF5722/white?text=ชาไทย"},
        {"id": 10, "name": "น้ำเปล่า", "price": 10, "image": "https://via.placeholder.com/200x150/E3F2FD/black?text=น้ำเปล่า"}
    ],
    "อาหารจานเดียว": [
        {"id": 11, "name": "ข้าวผัดกุ้ง", "price": 120, "image": "https://via.placeholder.com/200x150/FF9800/white?text=ข้าวผัดกุ้ง"},
        {"id": 12, "name": "ผัดไทยกุ้ง", "price": 100, "image": "https://via.placeholder.com/200x150/FFC107/white?text=ผัดไทย"},
        {"id": 13, "name": "ข้าวกะเพราหมูกรอบ", "price": 80, "image": "https://via.placeholder.com/200x150/4CAF50/white?text=กะเพราหมู"},
        {"id": 14, "name": "ก๋วยเตี๋ยวน้ำใส", "price": 60, "image": "https://via.placeholder.com/200x150/2196F3/white?text=ก๋วยเตี๋ยว"},
        {"id": 15, "name": "ข้าวผัดปู", "price": 150, "image": "https://via.placeholder.com/200x150/E91E63/white?text=ข้าวผัดปู"},
        {"id": 16, "name": "ผัดซีอิ๊วหมู", "price": 85, "image": "https://via.placeholder.com/200x150/795548/white?text=ผัดซีอิ๊ว"},
        {"id": 17, "name": "ข้าวหน้าเป็ด", "price": 90, "image": "https://via.placeholder.com/200x150/FF5722/white?text=ข้าวหน้าเป็ด"},
        {"id": 18, "name": "ลาบหมู", "price": 70, "image": "https://via.placeholder.com/200x150/8BC34A/white?text=ลาบหมู"},
        {"id": 19, "name": "ส้มตำไทย", "price": 65, "image": "https://via.placeholder.com/200x150/CDDC39/white?text=ส้มตำ"},
        {"id": 20, "name": "ข้าวซอยไก่", "price": 75, "image": "https://via.placeholder.com/200x150/FFA726/white?text=ข้าวซอย"}
    ],
    "ของทานเล่น": [
        {"id": 21, "name": "ไก่ทอด 6 ชิ้น", "price": 90, "image": "https://via.placeholder.com/200x150/FF9800/white?text=ไก่ทอด"},
        {"id": 22, "name": "หมูปิ้ง 5 ไม้", "price": 80, "image": "https://via.placeholder.com/200x150/E91E63/white?text=หมูปิ้ง"},
        {"id": 23, "name": "ปอเปี๊ยะทอด", "price": 45, "image": "https://via.placeholder.com/200x150/4CAF50/white?text=ปอเปี๊ยะ"},
        {"id": 24, "name": "ไส้กรอกอีสาน", "price": 60, "image": "https://via.placeholder.com/200x150/F44336/white?text=ไส้กรอก"},
        {"id": 25, "name": "ข้าวเกรียบปากหม้อ", "price": 35, "image": "https://via.placeholder.com/200x150/795548/white?text=ข้าวเกรียบ"},
        {"id": 26, "name": "กุ้งชุบแป้งทอด", "price": 120, "image": "https://via.placeholder.com/200x150/FF5722/white?text=กุ้งทอด"},
        {"id": 27, "name": "ปลาหมึกย่าง", "price": 95, "image": "https://via.placeholder.com/200x150/9C27B0/white?text=ปลาหมึก"},
        {"id": 28, "name": "ไข่เจียวกรอบ", "price": 40, "image": "https://via.placeholder.com/200x150/FFEB3B/black?text=ไข่เจียว"},
        {"id": 29, "name": "มันทอด", "price": 30, "image": "https://via.placeholder.com/200x150/FFC107/white?text=มันทอด"},
        {"id": 30, "name": "ปีกไก่ย่าง 4 ชิ้น", "price": 70, "image": "https://via.placeholder.com/200x150/FF9800/white?text=ปีกย่าง"}
    ],
    "ของหวาน": [
        {"id": 31, "name": "มะม่วงข้าวเหนียว", "price": 60, "image": "https://via.placeholder.com/200x150/FFEB3B/black?text=มะม่วงเหนียว"},
        {"id": 32, "name": "บัวลอยน้ำกะทิ", "price": 40, "image": "https://via.placeholder.com/200x150/E1BEE7/black?text=บัวลอย"},
        {"id": 33, "name": "ทับทิมกรอบ", "price": 45, "image": "https://via.placeholder.com/200x150/E91E63/white?text=ทับทิมกรอบ"},
        {"id": 34, "name": "ไอติมกะทิ", "price": 35, "image": "https://via.placeholder.com/200x150/F8BBD9/black?text=ไอติม"},
        {"id": 35, "name": "ลอดช่องสิงคโปร์", "price": 50, "image": "https://via.placeholder.com/200x150/4CAF50/white?text=ลอดช่อง"},
        {"id": 36, "name": "ข้าวเหนียวมะม่วง", "price": 55, "image": "https://via.placeholder.com/200x150/FF9800/white?text=เหนียวมะม่วง"},
        {"id": 37, "name": "ฟักทองแกงบวด", "price": 40, "image": "https://via.placeholder.com/200x150/FF5722/white?text=ฟักทอง"},
        {"id": 38, "name": "กล้วยบวชชี", "price": 35, "image": "https://via.placeholder.com/200x150/795548/white?text=กล้วยบวชชี"},
        {"id": 39, "name": "ขนมครก", "price": 25, "image": "https://via.placeholder.com/200x150/9E9E9E/white?text=ขนมครก"},
        {"id": 40, "name": "วุ้นกะทิ", "price": 30, "image": "https://via.placeholder.com/200x150/2196F3/white?text=วุ้นกะทิ"}
    ]
}

# เก็บข้อมูล orders จากแต่ละโต๊ะ
orders_data = {}
order_history = []

def find_menu_item(item_id):
    """ค้นหาเมนูจาก ID"""
    for category_items in menu_data.values():
        for item in category_items:
            if item["id"] == item_id:
                return item
    return None

@app.route('/')
def kitchen_view():
    """หน้าแสดงรายการสั่งสำหรับเชฟในครัว"""
    return render_template('home.html')

@app.route('/table/<int:table_number>')
def customer_view(table_number):
    """หน้าสำหรับลูกค้าดูรายการอาหารของโต๊ะตัวเอง"""
    table_name = f"โต๊ะ {table_number}"
    return render_template('customer.html', table_name=table_name, table_number=table_number)

@app.route('/api/menu/<category>', methods=['GET'])
def get_menu_by_category(category):
    """ดึงข้อมูลเมนูตามหมวดหมู่"""
    if category in menu_data:
        return jsonify({
            "success": True,
            "category": category,
            "items": menu_data[category]
        })
    else:
        return jsonify({
            "success": False,
            "message": "Category not found"
        }), 404

@app.route('/api/menu/all', methods=['GET'])
def get_all_menu():
    """ดึงข้อมูลเมนูทั้งหมด"""
    return jsonify({
        "success": True,
        "data": menu_data
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """ดึงรายชื่อหมวดหมู่ทั้งหมด"""
    return jsonify({
        "success": True,
        "categories": list(menu_data.keys())
    })

@app.route('/api/orders', methods=['POST'])
def submit_order():
    """รับ order จากแอพและเก็บไว้"""
    try:
        data = request.json
        table_name = data.get('table_name')
        items = data.get('items', {})
        
        if not table_name or not items:
            return jsonify({
                "success": False,
                "message": "Missing table_name or items"
            }), 400
        
        # แปลง items เป็นรูปแบบที่มีข้อมูลเมนูครบ
        order_items = []
        total_price = 0
        
        for item_id_str, quantity in items.items():
            item_id = int(item_id_str)
            menu_item = find_menu_item(item_id)
            if menu_item and quantity > 0:
                subtotal = menu_item["price"] * quantity
                order_items.append({
                    "id": item_id,
                    "name": menu_item["name"],
                    "price": menu_item["price"],
                    "quantity": quantity,
                    "subtotal": subtotal
                })
                total_price += subtotal
        
        if not order_items:
            return jsonify({
                "success": False,
                "message": "No valid items in order"
            }), 400
        
        # สร้าง order object
        order = {
            "id": len(order_history) + 1,
            "table_name": table_name,
            "items": order_items,
            "total_price": total_price,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending"
        }
        
        # เก็บ order
        orders_data[table_name] = order
        order_history.append(order)
        
        return jsonify({
            "success": True,
            "message": "Order submitted successfully",
            "order_id": order["id"]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/orders', methods=['GET'])
def get_all_orders():
    """ดึงรายการ order ทั้งหมดสำหรับแสดงในครัว"""
    return jsonify({
        "success": True,
        "orders": list(orders_data.values())
    })

@app.route('/api/orders/<table_name>', methods=['GET'])
def get_order_by_table(table_name):
    """ดึง order ของโต๊ะที่ระบุ"""
    if table_name in orders_data:
        return jsonify({
            "success": True,
            "order": orders_data[table_name]
        })
    else:
        return jsonify({
            "success": False,
            "message": "No order found for this table"
        }), 404

@app.route('/api/orders/customer', methods=['POST'])
def submit_customer_order():
    """รับ order จากลูกค้าผ่านเว็บ"""
    try:
        data = request.json
        table_name = data.get('table_name')
        items = data.get('items', {})
        
        if not table_name or not items:
            return jsonify({
                "success": False,
                "message": "Missing table_name or items"
            }), 400
        
        # ตรวจสอบว่ามี order เดิมอยู่แล้วหรือไม่
        existing_order = orders_data.get(table_name)
        
        # แปลง items เป็นรูปแบบที่มีข้อมูลเมนูครบ
        new_order_items = []
        total_price = 0
        
        for item_id_str, quantity in items.items():
            item_id = int(item_id_str)
            menu_item = find_menu_item(item_id)
            if menu_item and quantity > 0:
                subtotal = menu_item["price"] * quantity
                new_order_items.append({
                    "id": item_id,
                    "name": menu_item["name"],
                    "price": menu_item["price"],
                    "quantity": quantity,
                    "subtotal": subtotal
                })
                total_price += subtotal
        
        if not new_order_items:
            return jsonify({
                "success": False,
                "message": "No valid items in order"
            }), 400
        
        if existing_order:
            # รวมรายการใหม่เข้ากับของเดิม
            existing_items = {item["id"]: item for item in existing_order["items"]}
            
            for new_item in new_order_items:
                item_id = new_item["id"]
                if item_id in existing_items:
                    # รวมจำนวนถ้าเมนูเดิมมีอยู่แล้ว
                    existing_items[item_id]["quantity"] += new_item["quantity"]
                    existing_items[item_id]["subtotal"] = existing_items[item_id]["price"] * existing_items[item_id]["quantity"]
                else:
                    # เพิ่มเมนูใหม่
                    existing_items[item_id] = new_item
            
            # คำนวณราคารวมใหม่
            combined_items = list(existing_items.values())
            combined_total = sum(item["subtotal"] for item in combined_items)
            
            # อัพเดท order
            existing_order["items"] = combined_items
            existing_order["total_price"] = combined_total
            existing_order["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            existing_order["status"] = "pending"
            
            return jsonify({
                "success": True,
                "message": "Order updated successfully",
                "order_id": existing_order["id"]
            })
        else:
            # สร้าง order ใหม่
            order = {
                "id": len(order_history) + 1,
                "table_name": table_name,
                "items": new_order_items,
                "total_price": total_price,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "pending"
            }
            
            # เก็บ order
            orders_data[table_name] = order
            order_history.append(order)
            
            return jsonify({
                "success": True,
                "message": "Order submitted successfully",
                "order_id": order["id"]
            })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/orders/<table_name>/complete', methods=['POST'])
def complete_order(table_name):
    """ทำเครื่องหมายว่า order เสร็จแล้ว"""
    if table_name in orders_data:
        orders_data[table_name]["status"] = "completed"
        return jsonify({
            "success": True,
            "message": "Order marked as completed"
        })
    else:
        return jsonify({
            "success": False,
            "message": "Order not found"
        }), 404

@app.route('/api/orders/summary', methods=['GET'])
def get_orders_summary():
    """สรุปรายการสั่งของทุกโต๊ะ"""
    summary = {}
    total_all = 0
    
    for table_name, order in orders_data.items():
        summary[table_name] = {
            "items_count": len(order["items"]),
            "total_items": sum(item["quantity"] for item in order["items"]),
            "total_price": order["total_price"],
            "timestamp": order["timestamp"],
            "status": order["status"]
        }
        total_all += order["total_price"]
    
    return jsonify({
        "success": True,
        "summary": summary,
        "grand_total": total_all
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)