import argparse
import json
import requests

from coveopush import Document
from coveopush.CoveoConstants import Constants
from coveopush.CoveoPermissions import PermissionIdentity
from coveopush.CoveoPermissions import PermissionIdentityExpansion
from coveopush.CoveoPush import Push

class JsonPush:
   def __init__(self, src_id: str, org_id: str, api_key: str, provider: str):
      self.reserved_keys = ["data", "date", "documentId", "permissions"]
      self.provider = provider
      self.push = self.__configure_push(src_id, org_id, api_key)
      
   def push_batch(self, items_file: str, identities_file: str):
      self.__push_items_batch(items_file)
      self.__push_identities_batch(identities_file)
      
   def __push_items_batch(self, items_file: str):
      if not items_file:
            print("No item batch to push")
            return
      
      print(f"Pushing {items_file}...")
      self.push.Start(True, True)
      
      with open(items_file, encoding='utf-8') as file:
            item_batch = json.load(file)
            for item in item_batch["addOrUpdate"]:
               self.push.Add(self.__get_document(item))
            
            for item in item_batch["delete"]:
               self.push.DeleteDocument(item["documentId"])
               
      self.push.End(True, True)
      
      print("Done")
   
   def __get_document(self, item: dict) -> Document:
      document = Document(item["documentId"])
      data = ""
      if "data" in item.keys():
            data = item["data"]
      else:
            data = requests.get(item["documentId"]).text
      document.SetData(data)
      
      for key in item.keys():
            if key not in self.reserved_keys:
               document.AddMetadata(key, item[key])
                
      if "permissions" in item.keys():  # If the item is secured
            permission_set = item["permissions"][0]
            document.SetAllowedAndDeniedPermissions(
               self.__get_permissions(permission_set, "allowedPermissions"),
               self.__get_permissions(permission_set, "deniedPermissions"))
                
      return document

   def __get_permissions(
            self, permission_set: dict, permission_kind: str) -> list:
      permissions = []

      for permission in permission_set[permission_kind]:
            identity_type = \
               Constants.PermissionIdentityType[permission["identityType"]]
            identity = PermissionIdentity(identity_type, self.provider,
                                          permission["identity"])
            permissions.append(identity)

      return permissions

   def __push_identities_batch(self, identities_file: str):
      if not identities_file:
            print("No identity batch to push")
            return

      print(f"Pushing {identities_file}...")

      self.push.StartExpansion(self.provider, True)

      with open(identities_file) as file:
            identity_batch = json.load(file)
            self.__add_identities(identity_batch, "members")
            self.__add_identities(identity_batch, "mappings")

      self.push.EndExpansion(self.provider, True)

      print("Done")

   def __add_identities(self, identity_batch: dict, identity_kind: str):
      for identity_data in identity_batch[identity_kind]:
            identity = self.__get_identity(identity_data["identity"])
            members = self.__get_members(identity_data, "members")
            mappings = self.__get_members(identity_data, "mappings")
            if identity_kind == "members":
               self.push.AddExpansionMember(identity, members, mappings, [])
            elif identity_kind == "mappings":
               self.push.AddExpansionMapping(identity, members, mappings, [])

   def __get_identity(self, member: dict) -> PermissionIdentityExpansion:
      identity_type = Constants.PermissionIdentityType.Unknown
      for enum in Constants.PermissionIdentityType:
            if str(enum.value) == member["type"]:
               identity_type = enum
               break

      return PermissionIdentityExpansion(
            identity_type, self.provider, member["name"])

   def __get_members(self, identity_data: dict, identity_kind: str) -> list:
      members = []

      if identity_kind in identity_data.keys():
            for member in identity_data[identity_kind]:
               members.append(self.__get_identity(member))

      return members

   def __configure_push(self, src_id: str, org_id: str, api_key: str) -> Push:
      push = Push(src_id, org_id, api_key)

      if self.provider:  # In other words, if the source is secured
            push.AddSecurityProvider(self.provider, "EXPANDED", {
               "Email Security Provider": {
                  "name": "Email Security Provider",
                  "type": "EMAIL"
               }
            })

      return push

def main():
   parser = argparse.ArgumentParser()

   parser.add_argument("--config", nargs="?", type=str,
                        default="./config.json", help="The path to the JSON \
                        configuration file to use (default: './config.json')")
   parser.add_argument("--items", nargs="?", type=str, help="The path to the \
      items JSON batch file to push")
   parser.add_argument("--identities", nargs="?", type=str, help="The path \
      to the security identities batch file to push")

   args = parser.parse_args()

   with open(args.config) as config_file:
      config = json.load(config_file)
      JsonPush(config["src_id"], config["org_id"], config["api_key"],
               config["provider"]).push_batch(args.items, args.identities)

if __name__ == '__main__':
   main()
