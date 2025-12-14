#Represents an IT support ticket

def __init__(self, ticket_id: int, priority, description, status , assigned_to, created_at, resolution_time_hours: int):
    self.ticket_id = ticket_id
    self.priority = priority
    self.description = description
    self.status = status
    self.assigned_to = assigned_to
    self.created_at = created_at
    self.resolution_time_hours = resolution_time_hours

    def assign_to(self, staff: str) -> None:
        """Assign the ticket to a staff member."""
        self.__assigned_to = staff

    def close_ticket(self) -> None:
        """Mark the ticket as closed."""
        self.status = "Closed"

    def get_status(self):
        return self.__status

    def __str__(self) -> str:
        return (
            f"Ticket {self.ticket_id}: {self.description} "
            f"[{self.priority}] – {self.status} "
            f"(assigned to: {self.assigned_to}, created at: {self.created_at}, "
            f"resolution time: {self.resolution_time_hours}h)"
            )