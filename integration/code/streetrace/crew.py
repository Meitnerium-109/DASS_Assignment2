class CrewMember:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.role = None  # Expected: 'driver', 'mechanic'
        self.is_assigned = False

class CrewManagementModule:
    """Manages crew members and their roles."""
    def __init__(self, registration_module):
        self.registration = registration_module
        self.members = {}

    def register_crew_member(self, user_id, name, member_id):
        if member_id in self.members:
            raise ValueError("Crew member ID already exists.")
        if user_id not in self.registration.users:
            raise ValueError("User not found: You must be a registered user to hire crew.")
        
        member = CrewMember(name, member_id)
        self.members[member_id] = member
        self.registration.users[user_id].crew.append(member)
        return member

    def assign_role(self, member_id, role):
        if member_id not in self.members:
            raise ValueError("Crew member not found.")
        valid_roles = ["driver", "mechanic", "spotter"]
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of {valid_roles}")
        
        member = self.members[member_id]
        member.role = role
        member.is_assigned = True
        return member
