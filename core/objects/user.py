import core.functions.registry as registry

class Group():
    def __init__(self, name, group_description, last_write, user_count,
        members):
        self.name = name
        self.group_description = group_description
        self.last_write = last_write
        self.user_count = user_count
        self.members = members


class User():
    def __init__(self, username, sid, user_folder, account_type, rid,
        account_created_date, last_login_date, password_reset_date,
        password_fail_date, account_flags, failed_login_count, login_count,
        lm_hash, nt_hash):
        self.username = username
        self.sid = sid
        self.user_folder = user_folder
        self.account_type = account_type
        self.rid = rid
        self.account_created_date = account_created_date
        self.last_login_date = last_login_date
        self.password_reset_date = password_reset_date
        self.password_fail_date = password_fail_date
        self.account_flags = account_flags
        self.failed_login_count = failed_login_count
        self.login_count = login_count
        self.lm_hash = lm_hash
        self.nt_hash = nt_hash


def get_sid_and_folder_from_username(config, username):
    try:
        for key in (k for k in registry.find_key_start_with(
            config.software_hive,
            "Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
            if "ProfileImagePath" in k['Name']):
            if key['Value'].split("\\")[-1] == username:
                sid = str(key['Name'].split("\\")[4])
                user_folder = str(key['Value'])
                return [sid, user_folder]
        return ['Unknown', 'Unknown']
    except:
        return ['Unknown', 'Unknown']


def get_groups_list(config):
    groups_list = []
    sam_info = registry.samparse(config.sam_hive)
    for group in sam_info['groups']:
        bgroup = group
        if type(group) is not str:
            group = group.decode("utf-8")
        name = ''.join(group[::2])
        group_description = sam_info['groups'][bgroup]['Group Description']
        if type(group_description) is not str:
            group_description = group_description.decode("utf-8")
        group_description  = ''.join(group_description[::2])
        last_write = sam_info['groups'][bgroup]['Last Write']
        user_count = sam_info['groups'][bgroup]['User Count']
        members = []
        for member in sam_info['groups'][bgroup]['Members'].split("\n"):
            if member:
                members.append([registry.sid_to_username(member, config.folder),
                    member])
        groups_list.append(Group(name, group_description, last_write,
            user_count, members))
    return groups_list        


def get_users_list(config):
    users_list = []
    sam_info = registry.samparse(config.sam_hive)
    for user in sam_info['users']:
        username = user
        [sid, user_folder] = get_sid_and_folder_from_username(config,
            username)
        account_type = sam_info['users'][user]['Account Type']
        rid = sam_info['users'][user]['RID']
        account_created_date = sam_info['users'][user]['Account Created Date']
        last_login_date = sam_info['users'][user]['Last Login Date']
        password_reset_date = sam_info['users'][user]['Password Reset Date']
        password_fail_date = sam_info['users'][user]['Password Fail Date']
        account_flags = sam_info['users'][user]['Account Flags']
        failed_login_count = sam_info['users'][user]['Failed Login Count']
        login_count = sam_info['users'][user]['Login Count']
        lm_hash = ''.join('{:02x}'.format(ord(c)) for c in sam_info['users']
            [user]['LM Password Hash'])
        nt_hash = ''.join('{:02x}'.format(ord(c)) for c in sam_info['users']
            [user]['NT Password Hash'])
        users_list.append(User(username, sid, user_folder, account_type, rid,
            account_created_date, last_login_date, password_reset_date,
            password_fail_date, account_flags, failed_login_count, login_count,
            lm_hash, nt_hash))
    return users_list

