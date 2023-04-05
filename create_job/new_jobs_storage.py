class NewJobs:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._job_dict = {}
        return cls._instance

    @property
    def job_dict(self):
        return self._job_dict

    def clear_list(self):
        self._job_dict.clear()
