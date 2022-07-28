import json
import requests

from coveopush import CoveoPush
from coveopush import Document

def main():
   src_id = "your source id"
   org_id = "your org id"
   api_key = "your api key"
  
   push = CoveoPush.Push(src_id, org_id, api_key)
   employee_file_name = "./employee_items.json"
   push.Start()
   with open(employee_file_name, encoding='utf-8') as f:
      meta_keys = ["picture", "firstname", "lastname", "transliteratedname",
      "worktitle", "workdepartment", "workteam", "workhiredate", "workterminationdate",
      "office", "latitude", "longitude", "timezone", "telephone",
      "email", "workhierarchy", "foldingcollection", "foldingparent", "foldingchild",
      "workstatus"]
      my_batch = []
      employee_object = json.load(f)
      for employee in employee_object["addOrUpdate"]:
          mydoc = Document(employee["documentId"])
          mydoc.SetData(requests.get(employee["documentId"]).text)
          for key in meta_keys:
              mydoc.AddMetadata(key, employee[key])
          push.Add(mydoc)
   push.End()

if __name__ == '__main__':
    main()
