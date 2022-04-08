[![PyPI](https://img.shields.io/pypi/v/core-lib)](https://pypi.org/project/core-lib/)
![PyPI - License](https://img.shields.io/pypi/l/core-lib)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/core-lib)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/core-lib.svg)](https://pypistats.org/packages/core-lib)

# UserAgreementCoreLib
`UserAgreementCoreLib` is built using `Core-Lib` and offers us with services that we can utilise to build an agreement platform for users where they 
may agree or disagree with documents or list items that we can create using the service. 

- Add document to the database
- Add list 
- Add items to the list
- User can agree to a document
- User can agree to individual list items
- User can disagree to individual list items

## Services

### SeedService
 
Responsible for inserting data in database

Functions 

-`seed_document(self, name: str, file_path: str, file_path_text_content: str, version: str)`

`name` (*str*): Name of the document.

`file_path` (*str*): Path of the file from which content id to be added to database.

`file_path_text_content` (*str*): Markdown content of the file.

`version` (*str*): Version of the document.

>Note: There cannot be 2 documents with same name and same version, there can be multiple files with same name and different versions

-`seed_agreement_list(self, agreement_list_name: str, agreement_list_items: list = [])`

`agreement_list_name` (*str*): Name of the list group.

`agreement_list_items` (*list*): Items to be included inside the list group.


### AgreementService

Responsible for agreeing to document and list items

Functions

- `agree_document(self, user_id: int, document_id: int)`

`user_id` (*int*): User ID of the person who has agreed to the terms of the document.

`document_id` (*int*): Document ID that the user has agreed.


- `agree_items(self, user_id: int, item_id: int)`

`user_id` (*int*): User ID of the person who has agreed to the terms of the list item.

`item_id` (*int*): Item ID that the user has agreed from the list.


- `disagree_items(self, user_id: int, item_id: int)`

`user_id` (*int*): User ID of the person who has disagreed to the terms of the list item.

`item_id` (*int*): Item ID that the user has disagreed from the list.


- `is_agreed_document(self, user_id: int, document_id: int)`

To check if the user has agreed to a specific document. Returns `bool`

`user_id` (*int*): User ID of the person.

`document_id` (*int*): Document ID of the document to check.


- `is_agreed_list(self, user_id, list_id: int)`

To check if the user has agreed to a specific list and all items inside it. Returns `bool`

`user_id` (*int*): User ID of the person.

`list` (*int*): List ID to check.



#### Example

```python
import hydra
from user_agreement_core_lib.user_agreement_core_lib import UserAgreementCoreLib

config_file = 'user_agreement_core_lib.yaml'
hydra.core.global_hydra.GlobalHydra.instance().clear()
hydra.initialize(config_path='../../user_agreement_core_lib/config')
config = hydra.compose(config_file)
ua_core_lib = UserAgreementCoreLib(config)

# Seeding document
version = 'v1'
md_content = '**some***basic - markdown'
file_name = 'privacy_policy'
document_data = ua_core_lib.seed_service.seed_document(file_name, 'path/to/file', md_content, version)

# Agreement for documents
ua_core_lib.agreement_service.agree_document(user_id, document_data['id'])
ua_core_lib.agreement_service.is_agreed_document(user_id, document_data['id'])# Returns True is user has agreed the document

# Seed List and List Items
list_name = 'terms_service'
list_items = ['term1', 'term2', 'term3' ...]
list_data  = ua_core_lib.seed_service.seed_agreement_list(list_name, list_items)
# list_data will have the details of created list and the ids of created items

# Agreement for List items
for items in list_data['list_items']:
    list_item_data = ua_core_lib.agreement_service.agree_items(user_id, items['id'])

ua_core_lib.agreement_service.is_agreed_list(user_id, list_id) #  Returns true if the user has agreed to all the list items
ua_core_lib.agreement_service.is_agreed_list(user_id, list_item_id)
ua_core_lib.agreement_service.is_agreed_list(user_id, list_id) # Returns false after disagreeing to one item

```




## License
Core-Lib in licenced under [MIT](https://github.com/shacoshe/core-lib/blob/master/LICENSE)

## About




## Services

  - SeedService
    - 

#### SeedService

We can use this service to add documents or