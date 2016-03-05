import core.objects.user as u

class UsersHandler():
    def __init__(self, session):
        self.session = session

    def display_users(self, arg):
        """\tDisplay the users informations."""
        output = "\n"
        users = u.get_users_list(self.session.configuration)
        for user in users:
            output += "Username:\t\t" + user.username + "\n"
            output += "SID:\t\t\t" + user.sid + "\n"
            output += "User folder:\t\t" + user.user_folder + "\n"
            output += "Account type:\t\t" + user.account_type + "\n"
            output += "User RID:\t\t" + user.rid + "\n"
            output += "Account creation date:\t" + user.account_created_date + "\n"
            output += "Last login date:\t" + user.last_login_date + "\n"
            output += "Password reset date:\t" + user.password_reset_date + "\n"
            output += "Password fail date:\t" + user.password_fail_date + "\n"
            output += "Account flags:\t\t" + user.account_flags + "\n"
            output += "Failed login count:\t" + str(user.failed_login_count) + "\n"
            output += "Login count:\t\t" + str(user.login_count) + "\n"
            output += "LM hash:\t\t" + user.lm_hash + "\n"
            output += "NT hash:\t\t" + user.nt_hash + "\n"
            output += "---------------------------------\n\n"
        return output
 
    def display_groups(self, arg):
        """\tDisplay the groups informations."""
        output = "\n"
        groups = u.get_groups_list(self.session.configuration)
        for group in groups:
            output += "Name:\t" + group.name + "\n"
            output += "Description:\t" + group.group_description + "\n"
            output += "Last write:\t" + '%s/%s/%s' % (group.last_write.month, group.last_write.day, group.last_write.year) + "\n"
            output += "Users number:\t" + str(group.user_count) + "\n"
            output += "Members:\n"
            for member in group.members:
                output += "\tUsername:\t" + member[0] + "\n"
                output += "\tSID:\t\t" + member[1] + "\n\n"
            output = output[:-1]
            if not group.members:
                output += "\tNone\n"
            output += "---------------------------------\n\n"
        return output
