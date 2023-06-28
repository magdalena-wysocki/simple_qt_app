import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMessageBox, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as ET
import psycopg2

class XmlViewer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("XML Viewer")
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.openFile()
        self.loadDatabaseData()

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml)")
        if filePath:
            try:
                tree = ET.parse(filePath)
                root = tree.getroot()
                xmlTags = self.parseXmlTags(root)
                self.textEdit.setText(xmlTags)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open the file: {str(e)}")

    def parseXmlTags(self, root):
        xmlTags = ""
        for child in root.iter():
            xmlTags += f"<{child.tag}>\n"
        return xmlTags

    def loadDatabaseData(self):
        try:
            connection = psycopg2.connect(
                host="your_host_name",
                port="5432",
                database="your_database_name",
                user="your_username",
                password="your_password"
            )

            cursor = connection.cursor()
            cursor.execute("SELECT xml_data FROM my_table LIMIT 1")
            result = cursor.fetchone()
            if result:
                xmlData = result[0]
                self.textEdit.append("\n\nXML Data from Database:\n")
                self.textEdit.append(xmlData)

            cursor.close()
            connection.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to the database: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    viewer = XmlViewer()
    viewer.show()

    sys.exit(app.exec_())
