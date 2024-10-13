from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title("Hệ thống quản lý sinh viên")
root.geometry("600x800")

# # Kết nối tới db
# conn = sqlite3.connect('student_book.db')
# c = conn.cursor()
#
# # Tao bang de luu tru
# c.execute('''
#     CREATE TABLE students(
#         student_id integer PRIMARY KEY AUTOINCREMENT,
#         first_name text,
#         last_name text,
#         class_code text,
#         year_enrolled integer,
#         avg_score real
#     )
# ''')
#
# # Ngat ket noi
# conn.close()

def them():
     # Kết nối và lấy dữ liệu
     conn = sqlite3.connect('student_book.db')
     c = conn.cursor()
     # Lấy dữ liệu đã nhập
     studentID_value = student_id.get()
     firstName_value = f_name.get()
     lastName_value = l_name.get()
     classCode_value = class_code.get()
     yearEnrolled_value = year_enrolled.get()
     avgScore_value = avg_score.get()
     # Thực hiện câu lệnh để thêm
     if not studentID_value:
         c.execute('''
             INSERT INTO students (student_id, first_name, last_name, class_code, year_enrolled, avg_score) 
             VALUES (:student_id, :first_name, :last_name, :class_code, :year_enrolled, :avg_score)
             ''', {
             'student_id': studentID_value,
             'first_name': firstName_value,
             'last_name': lastName_value,
             'class_code': classCode_value,
             'year_enrolled': yearEnrolled_value,
             'avg_score': avgScore_value
         })
     else:
         c.execute('''
              INSERT INTO students (first_name, last_name, class_code, year_enrolled, avg_score) 
              VALUES (:first_name, :last_name, :class_code, :year_enrolled, :avg_score)
              ''', {
             'first_name': firstName_value,
             'last_name': lastName_value,
             'class_code': classCode_value,
             'year_enrolled': yearEnrolled_value,
             'avg_score': avgScore_value
         })
     conn.commit()
     conn.close()

     # Reset form
     student_id.delete(0, END)
     f_name.delete(0, END)
     l_name.delete(0, END)
     class_code.delete(0, END)
     year_enrolled.delete(0, END)
     avg_score.delete(0, END)

     # Hien thi lai du lieu
     truy_van()


def xoa():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    # Thực hiện câu lệnh để xóa
    c.execute('DELETE FROM students WHERE student_id = :student_id', {'student_id': selected_id.get()})
    conn.commit()
    conn.close()

    selected_id.delete(0, END)

    # Hien thi thong bao
    messagebox.showinfo("Thông báo", "Đã xóa!")

    # Hien thi lai du lieu
    truy_van()


def truy_van():
    # Xóa đi các dữ liệu trong TreeView
    for row in tree.get_children():
        tree.delete(row)

    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    records = c.fetchall()

    # Hiển thị dữ liệu
    for r in records:
        tree.insert("", END, values=(r[0], r[2], r[1], r[3], r[4], r[5]))

    # Ngắt kết nối
    conn.close()


def chinh_sua():
    global editor
    editor = Tk()
    editor.title('Cập nhật bản ghi')
    editor.geometry("400x300")

    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    record_id = selected_id.get()
    c.execute("SELECT * FROM students WHERE student_id=:student_id", {'student_id':record_id})
    records = c.fetchall()

    global student_id_editor, f_name_editor, l_name_editor, class_code_editor, year_enrolled_editor, avg_score_editor

    student_id_editor = Entry(editor, width=30)
    student_id_editor.grid(row=0, column=1)
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1)
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=2, column=1)
    class_code_editor = Entry(editor, width=30)
    class_code_editor.grid(row=3, column=1)
    year_enrolled_editor = Entry(editor, width=30)
    year_enrolled_editor.grid(row=4, column=1)
    avg_score_editor = Entry(editor, width=30)
    avg_score_editor.grid(row=5, column=1)

    student_id_label = Label(editor, text="Mã sinh viên")
    student_id_label.grid(row=0, column=0)
    l_name_label = Label(editor, text="Họ")
    l_name_label.grid(row=1, column=0)
    f_name_label = Label(editor, text="Tên")
    f_name_label.grid(row=2, column=0)
    class_code_label = Label(editor, text="Mã lớp")
    class_code_label.grid(row=3, column=0)
    year_enrolled_label = Label(editor, text="Năm nhập học")
    year_enrolled_label.grid(row=4, column=0)
    avg_score_label = Label(editor, text="Điểm trung bình")
    avg_score_label.grid(row=5, column=0)

    for record in records:
        student_id_editor.insert(0, record[0])
        f_name_editor.insert(0, record[1])
        l_name_editor.insert(0, record[2])
        class_code_editor.insert(0, record[3])
        year_enrolled_editor.insert(0, record[4])
        avg_score_editor.insert(0, record[5])

    edit_btn = Button(editor, text="Lưu bản ghi", command=cap_nhat)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

def cap_nhat():
    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    record_id = student_id_editor.get()

    c.execute('''UPDATE students SET
           first_name = :first,
           last_name = :last,
           class_code = :class,
           year_enrolled = :year,
           avg_score = :score
           WHERE student_id = :id''',
              {
                  'first': f_name_editor.get(),
                  'last': l_name_editor.get(),
                  'class': class_code_editor.get(),
                  'year': year_enrolled_editor.get(),
                  'score': avg_score_editor.get(),
                  'id': record_id
              })

    conn.commit()
    conn.close()
    editor.destroy()

    # Cập nhật lại danh sách bản ghi sau khi chỉnh sửa
    truy_van()


# Khung cho các ô nhập liệu
input_frame = Frame(root)
input_frame.pack(pady=10)

# Các ô nhập liệu cho cửa sổ chính
student_id = Entry(input_frame, width=30)
student_id.grid(row=0, column=1)
l_name = Entry(input_frame, width=30)
l_name.grid(row=1, column=1)
f_name = Entry(input_frame, width=30)
f_name.grid(row=2, column=1)
class_code = Entry(input_frame, width=30)
class_code.grid(row=3, column=1)
year_enrolled = Entry(input_frame, width=30)
year_enrolled.grid(row=4, column=1)
avg_score = Entry(input_frame, width=30)
avg_score.grid(row=5, column=1)

# Các nhãn
student_id_label = Label(input_frame, text="Mã sinh viên")
student_id_label.grid(row=0, column=0)
l_name_label = Label(input_frame, text="Họ")
l_name_label.grid(row=1, column=0)
f_name_label = Label(input_frame, text="Tên")
f_name_label.grid(row=2, column=0)
class_code_label = Label(input_frame, text="Mã lớp")
class_code_label.grid(row=3, column=0)
year_enrolled_label = Label(input_frame, text="Năm nhập học")
year_enrolled_label.grid(row=4, column=0)
avg_score_label = Label(input_frame, text="Điểm trung bình")
avg_score_label.grid(row=5, column=0)

# Khung cho các nút chức năng
button_frame = Frame(root)
button_frame.pack(pady=10)

# Các nút chức năng
submit_btn = Button(button_frame, text="Thêm bản ghi", command=them)
submit_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
query_btn = Button(button_frame, text="Hiển thị bản ghi", command=truy_van)
query_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
selected_id_label = Label(button_frame, text="Chọn ID")
selected_id_label.grid(row=2, column=0, pady=5)
selected_id = Entry(button_frame, width=30)
selected_id.grid(row=2, column=1, pady=5)
delete_btn = Button(button_frame, text="Xóa bản ghi", command=xoa)
delete_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=136)
edit_btn = Button(button_frame, text="Chỉnh sửa bản ghi", command=chinh_sua)
edit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

# Khung cho Treeview
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Treeview để hiển thị bản ghi
columns = ("Mã sinh viên", "Họ", "Tên", "Mã lớp", "Năm nhập học", "Điểm trung bình")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
for column in columns:
    tree.column(column, anchor=CENTER)
    tree.heading(column, text=column)
tree.pack()

# Định nghĩa tiêu đề cho các cột
for col in columns:
    tree.heading(col, text=col)

# Gọi hàm truy vấn để hiển thị bản ghi khi khởi động
truy_van()

root.mainloop()
