"""
文档解析模块 - 支持 PDF 和 Word 格式
"""

import os
import PyPDF2
import pdfplumber
from docx import Document
from typing import List, Dict


class DocumentParser:
    """文档解析器"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.doc', '.docx']
    
    def parse_file(self, file_path: str) -> Dict:
        """
        解析文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            {
                'filename': 文件名，
                'content': 完整文本内容，
                'pages': 页数，
                'format': 文件格式
            }
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        filename = os.path.basename(file_path)
        
        if file_ext == '.pdf':
            return self._parse_pdf(file_path, filename)
        elif file_ext in ['.doc', '.docx']:
            return self._parse_word(file_path, filename)
        else:
            raise ValueError(f"不支持的文件格式：{file_ext}")
    
    def _parse_pdf(self, file_path: str, filename: str) -> Dict:
        """解析 PDF 文件"""
        content = []
        pages_data = []
        
        # 使用 pdfplumber 获取更精确的文本和位置信息
        with pdfplumber.open(file_path) as pdf:
            total_pages = len(pdf.pages)
            
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ""
                content.append(text)
                
                pages_data.append({
                    'page': page_num,
                    'text': text,
                    'words': len(text.split())
                })
        
        full_content = "\n".join(content)
        
        return {
            'filename': filename,
            'content': full_content,
            'pages': total_pages,
            'format': 'pdf',
            'pages_data': pages_data
        }
    
    def _parse_word(self, file_path: str, filename: str) -> Dict:
        """解析 Word 文件"""
        doc = Document(file_path)
        
        paragraphs = []
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)
        
        full_content = "\n".join(paragraphs)
        
        return {
            'filename': filename,
            'content': full_content,
            'pages': len(paragraphs),  # Word 用段落数代替页数
            'format': 'docx',
            'paragraphs': paragraphs
        }


class DocumentChunker:
    """文档分块器"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        初始化分块器
        
        Args:
            chunk_size: 每块大小（字符数）
            chunk_overlap: 块间重叠大小
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        将文本分块
        
        Args:
            text: 待分块的文本
            metadata: 元数据
            
        Returns:
            [
                {
                    'text': 文本块内容，
                    'metadata': {
                        'chunk_id': 块 ID,
                        'source': 来源文件，
                        'page': 页码（如果有）,
                        'position': 位置
                    }
                }
            ]
        """
        chunks = []
        
        # 按段落分割
        paragraphs = text.split('\n')
        current_chunk = ""
        current_pos = 0
        
        for para in paragraphs:
            if not para.strip():
                continue
            
            # 如果当前块 + 新段落超过大小，保存当前块并开始新块
            if len(current_chunk) + len(para) > self.chunk_size:
                if current_chunk:
                    chunks.append({
                        'text': current_chunk,
                        'metadata': metadata.copy() if metadata else {},
                        'position': current_pos
                    })
                    current_pos += 1
                
                # 保留重叠部分
                current_chunk = para
            else:
                if current_chunk:
                    current_chunk += "\n" + para
                else:
                    current_chunk = para
        
        # 添加最后一个块
        if current_chunk:
            chunks.append({
                'text': current_chunk,
                'metadata': metadata.copy() if metadata else {},
                'position': current_pos
            })
        
        # 为每个块添加 ID 和元数据
        for i, chunk in enumerate(chunks):
            chunk['metadata']['chunk_id'] = f"chunk_{i}"
            chunk['metadata']['chunk_size'] = len(chunk['text'])
        
        return chunks


if __name__ == "__main__":
    # 测试代码
    parser = DocumentParser()
    chunker = DocumentChunker(chunk_size=300, chunk_overlap=30)
    
    # 测试 PDF
    test_pdf = "test.pdf"
    if os.path.exists(test_pdf):
        result = parser.parse_file(test_pdf)
        print(f"PDF 解析成功：{result['filename']}")
        print(f"页数：{result['pages']}")
        print(f"内容长度：{len(result['content'])}")
        
        # 测试分块
        chunks = chunker.chunk_text(result['content'], {'source': result['filename']})
        print(f"分块数量：{len(chunks)}")
        print(f"第一块：{chunks[0]['text'][:100]}...")
