from datetime import datetime


# This function is used to write common utility codes that can be reused else where in the project
class Utilities:
    def change_time_format_from_timestamp(X):
        dt = datetime.fromisoformat(str(X))
        dt_st = dt.timestamp()
        return datetime.fromtimestamp(dt_st)