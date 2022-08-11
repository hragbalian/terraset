
class TerrasetException(Exception):
    pass


class SupersetProfileIssue(TerrasetException):
    def __init__(
            self,
            profile_info,
            message='Could not find Superset profile {profile_info}'):
        self.message = message.format(profile_info=profile_info)
        super().__init__(self.message)


class TerrasetProfileNotFoundInPath(TerrasetException):
    def __init__(
            self,
            message='Could not find Terraset profile in specified path'):
        self.message = message
        super().__init__(self.message)


class FoundExistingCharts(TerrasetException):
    def __init__(
            self,
            count,
            message='Found {count} charts stored in your local directory. To overwrite, set overwrite to True'):
        self.message = message.format(count=count)
        super().__init__(self.message)


class FoundExistingDashboards(TerrasetException):
    def __init__(
            self,
            count,
            message='Found {count} dashboards stored in your local directory. To overwrite, set overwrite to True'):
        self.message = message.format(count=count)
        super().__init__(self.message)
