"""
OCR 工具模块 - 处理扫描件等非结构化文档
支持 PDF 扫描件和图片的文本识别
"""

import os
import io
from typing import List, Dict, Optional
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tempfile


class OCRProcessor:
    """OCR 处理器"""
    
    def __init__(self, lang: str = 'chi_sim+eng'):
        """
        初始化 OCR 处理器
        
        Args:
            lang: 识别语言，chi_sim 为简体中文，eng 为英文
                  可以使用 'chi_sim+eng' 组合
        """
        self.lang = lang
        self.config = '--oem 3 --psm 6'
    
    def extract_text_from_image(self, image_path: str) -> Dict:
        """
        从图片提取文本
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            {
                'filename': 文件名，
                'text': 识别的文本，
                'confidence': 置信度（如果有）
            }
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"文件不存在：{image_path}")
        
        try:
            # 打开图片
            image = Image.open(image_path)
            
            # OCR 识别
            text = pytesseract.image_to_string(image, lang=self.lang, config=self.config)
            
            # 获取详细数据（包含置信度）
            data = pytesseract.image_to_data(image, lang=self.lang, output_type=pytesseract.Output.DICT)
            
            # 计算平均置信度
            confidences = [c for c in data['conf'] if c > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'filename': os.path.basename(image_path),
                'text': text.strip(),
                'confidence': avg_confidence,
                'format': 'image'
            }
        
        except Exception as e:
            raise Exception(f"OCR 识别失败：{str(e)}")
    
    def extract_text_from_pdf(self, pdf_path: str, dpi: int = 300) -> Dict:
        """
        从 PDF 扫描件提取文本
        
        Args:
            pdf_path: PDF 文件路径
            dpi: 转换 DPI，越高识别越准确但速度越慢
            
        Returns:
            {
                'filename': 文件名，
                'pages': 页数，
                'text': 完整文本，
                'pages_data': 每页数据 [
                    {
                        'page': 页码，
                        'text': 文本内容，
                        'confidence': 置信度
                    }
                ]
            }
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"文件不存在：{pdf_path}")
        
        try:
            # 将 PDF 转换为图片
            images = convert_from_path(pdf_path, dpi=dpi)
            
            pages_data = []
            full_text = []
            
            for i, image in enumerate(images, 1):
                # 临时保存页面图片
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    image.save(tmp.name, 'PNG')
                    tmp_path = tmp.name
                
                try:
                    # OCR 识别
                    result = self.extract_text_from_image(tmp_path)
                    
                    pages_data.append({
                        'page': i,
                        'text': result['text'],
                        'confidence': result['confidence']
                    })
                    
                    full_text.append(result['text'])
                
                finally:
                    # 清理临时文件
                    os.unlink(tmp_path)
            
            return {
                'filename': os.path.basename(pdf_path),
                'pages': len(images),
                'text': '\n'.join(full_text),
                'pages_data': pages_data,
                'format': 'pdf_scan'
            }
        
        except Exception as e:
            raise Exception(f"PDF OCR 识别失败：{str(e)}")
    
    def process_document(self, file_path: str, is_scan: bool = False) -> Dict:
        """
        处理文档（自动判断是否需要 OCR）
        
        Args:
            file_path: 文件路径
            is_scan: 是否强制使用 OCR（扫描件）
            
        Returns:
            文档解析结果
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # 图片格式
        if file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            return self.extract_text_from_image(file_path)
        
        # PDF 扫描件
        elif file_ext == '.pdf' and is_scan:
            return self.extract_text_from_pdf(file_path)
        
        else:
            raise ValueError(f"不支持的文件格式或不需要 OCR: {file_ext}")
    
    def batch_process(self, file_paths: List[str], is_scan: bool = False) -> List[Dict]:
        """
        批量处理文件
        
        Args:
            file_paths: 文件路径列表
            is_scan: 是否强制使用 OCR
            
        Returns:
            处理结果列表
        """
        results = []
        for file_path in file_paths:
            try:
                result = self.process_document(file_path, is_scan)
                results.append(result)
            except Exception as e:
                results.append({
                    'filename': os.path.basename(file_path),
                    'error': str(e)
                })
        return results


# 测试代码
if __name__ == "__main__":
    processor = OCRProcessor(lang='chi_sim+eng')
    
    # 测试图片 OCR
    test_image = "test_scan.jpg"
    if os.path.exists(test_image):
        result = processor.extract_text_from_image(test_image)
        print(f"图片 OCR 结果：{result['filename']}")
        print(f"置信度：{result['confidence']:.2f}%")
        print(f"识别文本：{result['text'][:200]}...")
    
    # 测试 PDF OCR
    test_pdf = "test_scan.pdf"
    if os.path.exists(test_pdf):
        result = processor.extract_text_from_pdf(test_pdf)
        print(f"\nPDF OCR 结果：{result['filename']}")
        print(f"页数：{result['pages']}")
        print(f"识别文本：{result['text'][:200]}...")
