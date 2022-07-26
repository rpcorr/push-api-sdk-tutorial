from coveopush import CoveoPush
from coveopush import Document

def main():
   src_id = "ronancorrbellcadigitalcrowbk0cyffy-wlohpclpmz6fm7x6ozt3klcdba"
   org_id = "ronancorrbellcadigitalcrowbk0cyffy"
   api_key = "xx11ad81c0-3cc1-4afe-a72a-00da393886e0"
   
   push = CoveoPush.Push(src_id, org_id, api_key)
   mydoc = Document("https://employeedbsite.herokuapp.com/employees/Jaroslav-Pu%C5%A1ka/")
   mydoc.SetData("This is the body of the document. It’s a great place to put an employee biography.")
   mydoc.FileExtension = ".html"
   mydoc.AddMetadata("picture", "https://employeedbsite.herokuapp.com/static/images/male/7.jpg")
   mydoc.Title = "Jaroslav Puška - Systems Engineer"
   
   push.AddSingleDocument(mydoc)
   
if __name__ == '__main__':
   main()
