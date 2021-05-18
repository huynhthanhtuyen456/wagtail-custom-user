

class BaseConstantClass(object):
    @classmethod
    def get_all_members_as_dict(cls):
        members = {attr: getattr(cls, attr) for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")}
        return members


class UserRole(BaseConstantClass):
    EMPLOYER = 'employer'
    TALENT = 'talent'


class FilterType(BaseConstantClass):
    ALL = 'all'
    CATEGORY = 'category'
    SAVED = 'saved'
    REHIRE = 'rehire'
    LOCATION = 'location'
    EXPERIENCE = 'experience'
    RATING = 'rating'


class RatingOrder(BaseConstantClass):
    RATING_HIGH_TO_LOW = 'high_to_low'
    RATING_LOW_TO_HIGH = 'low_to_high'


class SortedCreate(BaseConstantClass):
    NEWEST = 'newest'
    OLDEST = 'oldest'


class SubjectJob(BaseConstantClass):
    JOB_REJECT = 'Job Rejected'
    JOB_APPROVAL = 'Job Approval'


class TemplateMailJob(BaseConstantClass):
    JOB_TEMPLATE_REJECT = 'approval_job/reject_job.html'
    JOB_TEMPLATE_APPROVAL = 'approval_job/approval_job.html'
