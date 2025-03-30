# from typing import List, Dict
#
#
# class Error:
#     code: int
#     title: str
#     message: str
#
#     def __init__(self, code: bool, title: str, message: str):
#         self.code = code
#         self.title = title
#         self.message = message
#
#     def to_dict(self) -> Dict:
#         return {
#             "code": self.code,
#             "title": self.title,
#             "message": self.message
#         }
#
#
# class Response:
#     success: bool
#     payload: Dict
#     error: List[Error]
#
#     def __init__(self, success: bool, payload: Dict, error: List[Error]) -> None:
#         self.success = success
#         self.payload = payload
#         self.error = error
#
#     def to_dict(self) -> Dict:
#         errors: List[Dict] = []
#         for error in self.error:
#             errors.append(error.to_dict())
#
#         return {
#             "success": self.success,
#             "payload": self.payload,
#             "error": errors
#         }
