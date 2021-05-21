from peewee import DoesNotExist

from bot.db.models import UserModel, Interest, Subject

from typing import Optional

# TODO
'''
    def email_validation(self, email: str):
    pass
'''


def add_new_user(t_id, t_username, name, email, department, degree_level):
    UserModel.create(
        t_id=t_id,
        t_username=t_username,
        name=name,
        email=email,
        department=department,
        degree_level=degree_level,
    )


def is_user_exist(t_id) -> bool:
    try:
        UserModel.get(t_id=t_id)
    except DoesNotExist:
        return False

    return True


def get_user(t_id: int) -> Optional[UserModel]:

    return UserModel.get_or_none(t_id=t_id)


def assign_interest(user: UserModel, subject_name: str):
    subject = Subject.get_or_none(name=subject_name)

    user_interests = get_all_interests_for_user(user.t_id)

    if subject_name not in user_interests.keys():
        Interest.create(user=user.id, subject=subject)


def remove_interest(user: UserModel, subject_name: str):
    """
        Removes interest for user. If subject with given name wasn't found DoesNotExist exception is being thrown.
    """
    subject = Subject.get_or_none(name=subject_name)
    if subject is not None:
        interest = Interest.get_or_none(user=user, subject=subject)

        if interest is not None:
            Interest.delete_by_id(interest.id)
        else:
            raise DoesNotExist("User {} doesn't have given interest \"{}\".".format(user.t_username, subject.name))
    else:
        raise DoesNotExist("Subject \"{}\" doesn't exist.".format(subject_name))


def get_all_interests_for_user(user_id: int) -> dict:
    """
        Returns a dict of pairs {subject_name, science_name (linked to the subject)}.
    """
    predicate = (UserModel.t_id == user_id)
    query_interests = ((Interest
                        .select(Interest, UserModel, Subject)
                        .join(UserModel, on=(Interest.user == UserModel.id))
                        .switch(Interest)
                        .join(Subject, on=(Interest.subject == Subject.id))
                        .where(predicate)
                        ))
    subjects = {}
    for record in query_interests:
        subjects[record.subject.name] = record.subject.science.name

    return subjects


def alter_user_info(user: UserModel, name: str = None, email: str = None,
                    department: str = None, degree_level: str = None):
    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    if department is not None:
        user.department = department
    if degree_level is not None:
        user.degree_level = degree_level

    user.save()
