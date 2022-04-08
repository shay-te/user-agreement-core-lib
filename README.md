# UserAgreementCoreLib
`UserAgreementCoreLib` is built using [Core-Lib](https://github.com/shay-te/core-lib) and offers us with services that we can utilise to build an agreement platform for users where they 
may agree or disagree with documents or list items that we can create using the service. 

- Add document to the database
- Add list 
- Add items to the list
- User can agree to a document
- User can agree to individual list items
- User can disagree to individual list items


# Example

```python
import hydra
from user_agreement_core_lib.user_agreement_core_lib import UserAgreementCoreLib

hydra.core.global_hydra.GlobalHydra.instance().clear()
hydra.initialize(config_path='../../user_agreement_core_lib/config')

# Create a new UserAgreementCoreLib using hydra (https://hydra.cc/docs/next/advanced/compose_api/) config
ua_core_lib = UserAgreementCoreLib(hydra.compose('user_agreement_core_lib.yaml'))

# Seeding document
version = 'v1'
md_content = '**some***basic - markdown'
file_name = 'privacy_policy'
document_data = ua_core_lib.seed_service.seed_document(file_name, 'path/to/file', md_content, version)

# Agreement for documents
ua_core_lib.agreement_service.agree_document(user_id, document_data['id'])
ua_core_lib.agreement_service.is_agreed_document(user_id,
                                                 document_data['id'])  # Returns True is user has agreed the document

# Seed List and List Items
list_name = 'terms_service'
list_items = ['term1', 'term2', 'term3'...]
list_data = ua_core_lib.seed_service.seed_agreement_list(list_name, list_items)
# list_data will have the details of created list and the ids of created items

# Agreement for List items
for items in list_data['list_items']:
    list_item_data = ua_core_lib.agreement_service.agree_item(user_id, items['id'])

ua_core_lib.agreement_service.is_agreed_list(user_id,
                                             list_id)  # Returns true if the user has agreed to all the list items
ua_core_lib.agreement_service.disagree_item(user_id, list_item_id)
ua_core_lib.agreement_service.is_agreed_list(user_id, list_id)  # Returns false after disagreeing to one item

```



# AgreementService

Responsible for agreeing to document and list items

## Functions

```python
def agree_document(self, user_id: int, document_id: int):
```

When a user agrees to a document, this method can be invoked, and it stores the document id and user id in the db entity. 

**Parameters**

`user_id` (*int*): The user who has agreed to the terms of the document.

`document_id` (*int*): The document that the user agrees to.

**Returns**

Created row in the entity **UserAgreementDocument** 


<br/>

```python
def agree_item(self, user_id: int, item_id: int):
```

When the user agrees to an item in the list, this method can be invoked to store the item id and user id in the database entity.

**Parameters**

`user_id` (*int*): The user who has agreed to the terms of the list item.

`item_id` (*int*): List item that the user agrees to.

**Returns**

Created row in the entity **UserAgreementListItem** 

<br/>

```python
def disagree_item(self, user_id: int, item_id: int):
```

When the user disagrees an item in the list this method can be invoked to SoftDelete the agreed item row.

**Parameters**

`user_id` (*int*): The user who has disagreed to the terms of the list item.

`item_id` (*int*): Item ID that the user has disagreed from the list.

<br/>

```python
def is_agreed_document(self, user_id: int, document_id: int):
```

To check if the user has agreed to a specific document.

**Parameters**

`user_id` (*int*): The user.

`document_id` (*int*): Document ID of the document to check.

**Returns**

`True` if agreed else `False`

<br/>

```python
def is_agreed_list(self, user_id, list_id: int):
```

To check if the user has agreed all items inside a list.

**Parameters**

`user_id` (*int*): The user.

`list` (*int*): List ID to check.

**Returns**

`True` if agreed else `False`

<br/>

# SeedService
 
Responsible for inserting data in database

## Functions 

```python
def seed_document(self, name: str, file_path: str, file_path_text_content: str, version: str):
```
Is responsible to add document data into the database entity.

**Parameters**

`name` (*str*): Name of the document.

`file_path` (*str*): Path of the file from which content id to be added to database.

`file_path_text_content` (*str*): Markdown content of the file.

`version` (*str*): Version of the document.

**Returns**

Created row in the entity **AgreementDocument** (*dict*).

>Note: There cannot be 2 documents with same name and same version, there can be multiple files with same name and different versions

<br/>

```python
def seed_agreement_list(self, agreement_list_name: str, agreement_list_items: list = []):
```
**Parameters**

`agreement_list_name` (*str*): Name of the agreement list.

`agreement_list_items` (*list*): Items to be included inside the agreement list.

**Returns**

Created list row in the entity **AgreementList** (*dict*) with a *list* of created items id (entity: **AgreementListItems** ) under `list_items` key.


## License
Core-Lib in licenced under [MIT](https://github.com/shacoshe/core-lib/blob/master/LICENSE)
