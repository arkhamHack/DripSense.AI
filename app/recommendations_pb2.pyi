from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RecommendationRequest(_message.Message):
    __slots__ = ("product_id", "user_preferences")
    class UserPreferencesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    product_id: str
    user_preferences: _containers.ScalarMap[str, str]
    def __init__(self, product_id: _Optional[str] = ..., user_preferences: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Recommendation(_message.Message):
    __slots__ = ("product_id", "product_name", "relevance_score", "product_json")
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    RELEVANCE_SCORE_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_JSON_FIELD_NUMBER: _ClassVar[int]
    product_id: str
    product_name: str
    relevance_score: float
    product_json: str
    def __init__(self, product_id: _Optional[str] = ..., product_name: _Optional[str] = ..., relevance_score: _Optional[float] = ..., product_json: _Optional[str] = ...) -> None: ...

class RecommendationResponse(_message.Message):
    __slots__ = ("recommendations",)
    RECOMMENDATIONS_FIELD_NUMBER: _ClassVar[int]
    recommendations: _containers.RepeatedCompositeFieldContainer[Recommendation]
    def __init__(self, recommendations: _Optional[_Iterable[_Union[Recommendation, _Mapping]]] = ...) -> None: ...
