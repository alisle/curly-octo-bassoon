from googleapiclient.discovery import build

class Document:
    def __init__(self, credentials = None) -> None:
        if credentials is None:
            credentials = GoogleDriveCredentials()
        
        self.__credentials = credentials
        self.__service = build("docs", "v1", credentials=self.__credentials.get())


    def parse_paragraph(self, element):
        text_run = element.get('textRun')
        if not text_run:
            return ''

        return text_run.get('content')

    def parse_elements(self, elements):
        text = ''
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for element in elements:
                    text += self.parse_paragraph(element)
            elif 'table' in value:
                table = value.get('table')
                for row in table.get('tableRows'):
                    cells = row.get('tableCells')
                    for cell in cells:
                        text += self.parse_elements(cell.get('content'))
            elif 'tableOfContents' in value:
                toc = value.get('tableOfContents')
                text += self.parse_elements(toc.get('content'))
        return text

    def read(self, documentID):
        doc = self.__service.documents().get(documentId=documentID).execute()
        contents = doc.get('body').get('content')
        return self.parse_elements(contents)



    