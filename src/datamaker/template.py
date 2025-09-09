from typing import Optional, Dict, List, Union


class WordsField:
    def __init__(self, name: str, options: Optional[Dict[str, int]] = None):
        self.name = name
        self.type = "Words"
        self.options = options


class UUIDField:
    def __init__(self, name: str, options: Optional[Dict[str, bool]] = None):
        self.name = name
        self.type = "UUID"
        self.options = options


class NumberField:
    def __init__(
        self, name: str, options: Optional[Dict[str, Union[int, bool]]] = None
    ):
        self.name = name
        self.type = "Number"
        self.options = options


class FloatField:
    def __init__(
        self, name: str, options: Optional[Dict[str, Union[int, float]]] = None
    ):
        self.name = name
        self.type = "Float"
        self.options = options


class BooleanField:
    def __init__(self, name: str, options: Optional[Dict[str, bool]] = None):
        self.name = name
        self.type = "Boolean"
        self.options = options


class AIField:
    def __init__(self, name: str, prompt: str):
        self.name = name
        self.type = "AI"
        self.options = {"prompt": prompt}


class CustomField:
    def __init__(self, name: str, values: List[str]):
        self.name = name
        self.type = "Custom"
        self.options = {"values": values}


# Similar classes would follow for each field type defined in the TypeScript code

DataMakerField = Union[
    WordsField,
    UUIDField,
    NumberField,
    FloatField,
    BooleanField,
    AIField,
    CustomField,  # Add other field classes here
]


class Template:
    def __init__(
        self,
        fields: List[DataMakerField],
        name: Optional[str] = None,
        quantity: Optional[int] = None,
    ):
        self.name = name
        self.fields = fields
        self.quantity = quantity

    def to_dict(self):
        return {
            "name": self.name,
            "fields": [field.__dict__ if hasattr(field, '__dict__') else field for field in self.fields],
            "quantity": self.quantity,
        }


class AccountTemplate:
    def __init__(
        self,
        id: str,
        name: str,
        fields: List[DataMakerField],
        created_at: str,
        created_by: str,
        template_folder_id: Optional[None] = None,
        team_id: str = "",
        seed: Optional[None] = None,
    ):
        self.id = id
        self.name = name
        self.fields = fields
        self.created_at = created_at
        self.created_by = created_by
        self.template_folder_id = template_folder_id
        self.team_id = team_id
        self.seed = seed


class Endpoint:
    def __init__(
        self,
        id: str,
        name: str,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        query_params: Optional[Dict] = None,
        created_at: str = "",
        created_by: str = "",
        team_id: Optional[str] = None,
        endpoint_folder_id: Optional[Union[str, None]] = None,
    ):
        self.id = id
        self.name = name
        self.method = method
        self.url = url
        self.headers = headers
        self.query_params = query_params
        self.created_at = created_at
        self.created_by = created_by
        self.team_id = team_id
        self.endpoint_folder_id = endpoint_folder_id


class Headers:
    def __init__(
        self, authorization: Optional[str], content_type: str, credentials: str
    ):
        self.Authorization = authorization
        self.Content_type = content_type
        self.Credentials = credentials


Data = Dict[str, Union[str, int]]


class CustomEndpoint:
    def __init__(self, url: str, method: str, headers: Optional[Dict] = None):
        self.url = url
        self.method = method
        self.headers = headers


class DBQuery:
    def __init__(self, connection_id: str, query: str):
        self.connection_id = connection_id
        self.query = query
