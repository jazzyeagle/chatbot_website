# result.py:  Holds the Result class definition, which is used by data.py & views to convey information
#             back and forth.

from enum import Enum


class ResultFlag(Enum):
    Ok    = 1
    Error = 2


class Result:
    # resultType is of type ResultFlag
    # resultValue is either the successfully computed value OR the error message
    def __init__(self, resultType, resultValue):
        self.resultType  = resultType
        if resultType == ResultFlag.Ok:
            self.value       = resultValue
        else:
            self.errors.append(resultValue)


    def isOk(self):
        if self.resultType == ResultFlag.Ok:
            return True
        return False

    def hasErrors(self):
        if self.resultType == ResultFlag.Error:
            return True
        return False

    def get(self):
        if self.resultType == ResultFlag.Ok:
            return self.value
        return None

    def set(self, new_value):
        self.value = new_value

    def getErrors(self):
        if self.resultType == ResultFlag.Error:
            return self.errors
        return None
