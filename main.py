import os
import argparse
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed
from rembg import remove, new_session
from PIL import Image, UnidentifiedImageError
import logging
from tqdm import tqdm
import sys
import shutil
import traceback

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except (IOError, SyntaxError, UnidentifiedImageError):
        logger.warning(f"File không phải là ảnh hợp lệ: {file_path}")
        return False
    except Exception as e:
        logger.error(f"Lỗi không xác định khi kiểm tra file: {file_path}. Lỗi: {str(e)}")
        return False

def remove_background(input_path, output_path, alpha_matting=False, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10, session=None):
    try:
        with Image.open(input_path) as img:
            output = remove(
                img,
                alpha_matting=alpha_matting,
                alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
                alpha_matting_background_threshold=alpha_matting_background_threshold,
                session=session
            )
            
            file_extension = os.path.splitext(output_path)[1].lower()
            
            if file_extension in ['.jpg', '.jpeg']:
                rgb_im = output.convert('RGB')
                rgb_im.save(output_path, 'JPEG', quality=95)
            else:
                output.save(output_path)
        
        return True
    except IOError as e:
        logger.error(f"Lỗi I/O khi xử lý {input_path}: {str(e)}")
    except MemoryError:
        logger.error(f"Lỗi bộ nhớ khi xử lý {input_path}. Thử giảm kích thước ảnh hoặc giải phóng bộ nhớ.")
    except Exception as e:
        logger.error(f"Lỗi không xác định khi xử lý {input_path}: {str(e)}")
        logger.debug(traceback.format_exc())
    return False

def process_images(input_paths, output_dir, alpha_matting, alpha_matting_foreground_threshold, alpha_matting_background_threshold):
    try:
        session = new_session()
    except Exception as e:
        logger.error(f"Không thể tạo phiên làm việc mới: {str(e)}")
        return []

    results = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for input_path in input_paths:
            file_name = os.path.basename(input_path)
            file_name_without_ext, _ = os.path.splitext(file_name)
            output_path = os.path.join(output_dir, f"no_bg_{file_name_without_ext}.png")
            
            future = executor.submit(
                remove_background, 
                input_path, 
                output_path, 
                alpha_matting, 
                alpha_matting_foreground_threshold, 
                alpha_matting_background_threshold,
                session
            )
            futures.append(future)
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Xử lý ảnh"):
            try:
                results.append(future.result())
            except Exception as e:
                logger.error(f"Lỗi khi xử lý ảnh: {str(e)}")
    
    return results

def get_valid_image_paths(input_paths):
    valid_paths = []
    for path in input_paths:
        try:
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        if is_valid_image(full_path):
                            valid_paths.append(full_path)
            elif os.path.isfile(path) and is_valid_image(path):
                valid_paths.append(path)
            else:
                logger.warning(f"Đầu vào không hợp lệ hoặc không phải là ảnh: {path}")
        except PermissionError:
            logger.error(f"Không có quyền truy cập: {path}")
        except Exception as e:
            logger.error(f"Lỗi khi xử lý đường dẫn {path}: {str(e)}")
    return valid_paths

def main():
    parser = argparse.ArgumentParser(description="Công cụ xóa nền ảnh nâng cao")
    parser.add_argument("input", nargs="+", help="Đường dẫn đến ảnh đầu vào hoặc thư mục chứa ảnh")
    parser.add_argument("-o", "--output", default="output", help="Thư mục đầu ra")
    parser.add_argument("--alpha-matting", action="store_true", help="Sử dụng alpha matting để cải thiện chất lượng")
    parser.add_argument("--alpha-matting-foreground-threshold", type=int, default=240, help="Ngưỡng foreground cho alpha matting")
    parser.add_argument("--alpha-matting-background-threshold", type=int, default=10, help="Ngưỡng background cho alpha matting")
    
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        logger.error(f"Lỗi đối số: {str(e)}")
        sys.exit(1)

    input_paths = []
    for input_arg in args.input:
        try:
            input_paths.extend(glob.glob(input_arg, recursive=True))
        except glob.GlobError as e:
            logger.error(f"Lỗi khi tìm kiếm file: {str(e)}")

    if not input_paths:
        logger.error("Không tìm thấy file đầu vào. Vui lòng kiểm tra lại đường dẫn.")
        sys.exit(1)

    valid_input_paths = get_valid_image_paths(input_paths)

    if not valid_input_paths:
        logger.error("Không tìm thấy ảnh đầu vào hợp lệ.")
        sys.exit(1)

    output_dir = args.output
    try:
        os.makedirs(output_dir, exist_ok=True)
    except PermissionError:
        logger.error(f"Không có quyền tạo thư mục đầu ra: {output_dir}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Lỗi khi tạo thư mục đầu ra: {str(e)}")
        sys.exit(1)

    logger.info(f"Bắt đầu xử lý {len(valid_input_paths)} ảnh...")
    try:
        results = process_images(
            valid_input_paths, 
            output_dir, 
            args.alpha_matting, 
            args.alpha_matting_foreground_threshold, 
            args.alpha_matting_background_threshold
        )

        successful = sum(results)
        logger.info(f"Đã xử lý thành công {successful}/{len(valid_input_paths)} ảnh.")
        logger.info(f"Ảnh đã được xử lý và lưu trong thư mục: {output_dir}")

        if successful < len(valid_input_paths):
            logger.warning("Một số ảnh không được xử lý thành công. Kiểm tra log để biết thêm chi tiết.")
    except KeyboardInterrupt:
        logger.info("Quá trình xử lý bị ngắt bởi người dùng.")
    except Exception as e:
        logger.error(f"Lỗi không xác định trong quá trình xử lý: {str(e)}")
        logger.debug(traceback.format_exc())
    finally:
        # Dọn dẹp tài nguyên nếu cần
        try:
            shutil.rmtree("temp_dir", ignore_errors=True)
        except Exception as e:
            logger.error(f"Lỗi khi dọn dẹp tài nguyên tạm thời: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Lỗi nghiêm trọng: {str(e)}")
        logger.debug(traceback.format_exc())
        sys.exit(1)

``
# made by tanbaycu
