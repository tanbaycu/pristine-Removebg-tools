## ✂️ pristine-Removebg-tools - tanbaycu Tools🐳

**pristine-Removebg-tools** là một công cụ Python mạnh mẽ sử dụng thư viện `rembg` để loại bỏ nền ảnh một cách thông minh và hiệu quả. Với khả năng `xử lý hàng loạt`, `đa luồng` và `hỗ trợ nhiều phương thức đầu vào`, công cụ này là giải pháp lý tưởng cho cả người dùng cá nhân và doanh nghiệp.

---

## ✨ Tính năng chính

- 🚀 **Xử lý hàng loạt**: Loại bỏ nền của nhiều ảnh cùng lúc
- 📁 **Hỗ trợ thư mục**: Xử lý toàn bộ thư mục, bao gồm cả thư mục con
- 🧵 **Đa luồng**: Tối ưu hiệu suất với xử lý đa luồng
- 🎨 **Alpha matting**: Tùy chọn nâng cao chất lượng với alpha matting
- 🔧 **Tùy chỉnh ngưỡng**: Điều chỉnh ngưỡng alpha matting để có kết quả tối ưu
- 🔍 **Tự động phát hiện**: Bỏ qua các file không phải ảnh
- 📊 **Ghi log chi tiết**: Dễ dàng theo dõi và khắc phục sự cố
- 📈 **Thanh tiến trình**: Theo dõi trực quan quá trình xử lý

---

## 🛠️ Cài đặt

<details>
<summary>Nhấp để xem hướng dẫn cài đặt</summary>

1. Đảm bảo bạn đã cài đặt Python 3.6 trở lên.
2. Clone repository:
   ```bash
   git clone https://github.com/tanbaycu/pristine-Removebg-tools.git

   cd pristine-Removebg-tools
3. Cài đặt các thư viện cần thiết:

    ```shellscript
    pip install -r requirements.txt
    ```




</details>

---

## 🚀 Sử dụng

### Cú pháp cơ bản

```shellscript
python main.py <đường_dẫn_đến_ảnh_hoặc_thư_mục>
```

### Cú pháp nâng cao

```bash
python main.py <đầu_vào> [<đầu_vào>...] [-o ĐẦU_RA] [--alpha-matting] [--alpha-matting-foreground-threshold NGƯỠNG] [--alpha-matting-background-threshold NGƯỠNG]
```

### Tham số

| Tham số | Mô tả | Mặc định
|-----|-----|-----
| `<đầu_vào>` | Đường dẫn đến file ảnh hoặc thư mục | Bắt buộc
| `-o, --output` | Thư mục đầu ra | "output"
| `--alpha-matting` | Kích hoạt alpha matting | False
| `--alpha-matting-foreground-threshold` | Ngưỡng foreground cho alpha matting | 240
| `--alpha-matting-background-threshold` | Ngưỡng background cho alpha matting | 10


### Ví dụ sử dụng

<details>
<summary>Nhấp để xem các ví dụ</summary>   

**1. Xử lý một ảnh đơn:**

```shellscript
python main.py image.jpg
```


**2. Xử lý nhiều ảnh:**

```shellscript
python main.py image1.jpg image2.png image3.jpeg
```


**3. Xử lý một thư mục:**

```shellscript
python main.py /path/to/image/folder
```


**4. Sử dụng alpha matting:**

```shellscript
python main.py image.jpg --alpha-matting
```


**5. Chỉ định thư mục đầu ra:**

```shellscript
python main.py image.jpg -o /path/to/output
```


**6. Điều chỉnh ngưỡng alpha matting:**

```shellscript
python main.py image.jpg --alpha-matting --alpha-matting-foreground-threshold 230 --alpha-matting-background-threshold 20
```




</details>

---

## 🔬 Tính năng nâng cao

### Alpha Matting

Alpha matting là một kỹ thuật nâng cao để cải thiện chất lượng của việc loại bỏ nền, đặc biệt hữu ích cho các ảnh có cạnh phức tạp hoặc trong suốt một phần.

Để sử dụng alpha matting:

```shellscript
python main.py image.jpg --alpha-matting
```

Điều chỉnh ngưỡng để có kết quả tốt nhất:

```shellscript
python main.py image.jpg --alpha-matting --alpha-matting-foreground-threshold 230 --alpha-matting-background-threshold 20
```

### Xử lý đa luồng

Công cụ tự động sử dụng xử lý đa luồng để tối ưu hiệu suất. Bạn có thể điều chỉnh số lượng luồng bằng cách sửa đổi giá trị `max_workers` trong hàm `ThreadPoolExecutor`:

```python
with ThreadPoolExecutor(max_workers=4) as executor:
    # Phần còn lại của mã
```

---

## 📊 Performance Tips

1. **Kích thước ảnh**: Giảm kích thước ảnh trước khi xử lý có thể cải thiện đáng kể tốc độ xử lý.
2. **Bộ nhớ**: Nếu gặp lỗi bộ nhớ, hãy thử xử lý ít ảnh hơn cùng một lúc.
3. **SSD**: Sử dụng ổ SSD để lưu trữ ảnh đầu vào và đầu ra có thể cải thiện tốc độ I/O.
4. **GPU Acceleration**: Nếu có GPU, bạn có thể cân nhắc sử dụng phiên bản GPU của `rembg` để tăng tốc xử lý.


---

## ❓ FAQ

<details>
<summary><b>1. Làm thế nào để xử lý ảnh có kích thước lớn?</b></summary>Đối với ảnh có kích thước lớn, bạn có thể thử các phương pháp sau:

- Giảm kích thước ảnh trước khi xử lý
- Tăng bộ nhớ RAM cho quá trình xử lý
- Sử dụng tùy chọn `--chunk-size` để xử lý ảnh theo từng phần nhỏ (cần thêm tính năng này vào script)


</details><details>
<summary><b>2. Công cụ có hỗ trợ định dạng ảnh nào?</b></summary>Công cụ hỗ trợ các định dạng ảnh phổ biến như JPG, PNG, WEBP. Đối với các định dạng khác, bạn có thể cần chuyển đổi trước khi xử lý.

</details><details>
<summary><b>3. Làm thế nào để cải thiện chất lượng đầu ra?</b></summary>Để cải thiện chất lượng, bạn có thể:

- Sử dụng tùy chọn alpha matting
- Điều chỉnh ngưỡng alpha matting
- Sử dụng ảnh đầu vào có độ phân giải cao


</details>

---

## 🤝 Đóng góp

Chúng tôi rất hoan nghênh mọi đóng góp để cải thiện công cụ này! Dưới đây là các bước để đóng góp:

1. Fork repository
2. Tạo branch cho tính năng của bạn (`git checkout -b feature/AmazingFeature`)
3. Commit các thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request


### Hướng dẫn đóng góp chi tiết

- Đảm bảo mã của bạn tuân thủ PEP 8
- Viết docstring cho các hàm và lớp mới
- Thêm unit test cho các tính năng mới
- Cập nhật README.md nếu cần thiết


---

## 📞 Hỗ trợ

Nếu bạn gặp bất kỳ vấn đề nào hoặc có câu hỏi, vui lòng mở một **issue** trong GitHub repository.

Mọi thắc mắc hay đóng góp hãy liên hệ tôi (24/7):

[→ Email](mailto:tanbaycu@gmail.com)

[→ Facebook](https://facebook.com/tanbaycu.404s)

---

<div align="center">🙏 Cảm ơn bạn đã sử dụng Pristine Removebg Tools của tôi!

[Về đầu trang](#️-advanced-background-removal-tool)

