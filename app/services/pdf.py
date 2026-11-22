import pymupdf

class PDFService:
    def get_page_count(self,content:bytes)->int:
        with pymupdf.open(
            stream=content,
            filetype='pdf'
        ) as document:
            return document.page_count
    def extract_text(self,content:bytes)->str:
        with pymupdf.open(stream=content,filetype="pdf") as document:
            texts = []

            for page in document:
                text=(page.get_text())
                text = text.replace("\x00", "")
                texts.append(text)

            return "".join(texts)