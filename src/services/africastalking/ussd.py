"""USSD service for Africastalking."""


# session_manager.py
class SessionManager:
    """Session Manager."""

    def __init__(self) -> None:
        """Initialize."""
        self.sessions = {}

    def start_session(self, session_id: str):
        self.sessions[session_id] = {"step": "main_menu"}

    def get_session(self, session_id: str):
        return self.sessions.get(session_id, None)

    def update_session(self, session_id: str, data: dict):
        if session_id in self.sessions:
            self.sessions[session_id].update(data)

    def end_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]


class USSDMenu:
    """USSD Menu manager."""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    def handle_request(
        self,
        *,
        session_id: str,
        user_input: str,
        phone_number: str,
    ):
        session = self.session_manager.get_session(session_id)

        # Start a new session if it doesn't exist
        if not session:
            self.session_manager.start_session(session_id)
            session = self.session_manager.get_session(session_id)
            return self.main_menu(session_id)

        step = session["step"]

        # Flow handling based on step
        if step == "main_menu":
            return self.main_menu(session_id)

        if step == "main_menu_response":
            return self.main_menu_response(session_id, user_input)

        if step == "payment_menu":
            return self.payment_menu(session_id, user_input, phone_number)

        self.session_manager.end_session(session_id)
        return "END Session expired. Please try again."

    # ---------- Menu Handlers ----------
    def main_menu(self, session_id):
        response = "CON Welcome to InFlow360 Invoice Service\n"
        response += "1. Check outstanding payments\n"
        response += "2. Make Payment\n"
        response += "3. Exit"
        self.session_manager.update_session(session_id, {"step": "main_menu_response"})
        return response

    def main_menu_response(self, session_id: str, user_input: str):
        if user_input == "1":
            outstanding = 150  # Example: fetch from DB
            self.session_manager.update_session(
                session_id,
                {"step": "payment_menu", "outstanding": outstanding},
            )
            return f"CON Outstanding payment: ${outstanding}\n1. Pay now\n2. Back"

        if user_input == "2":
            self.session_manager.update_session(session_id, {"step": "payment_menu"})
            return "CON Make Payment\n1. Pay now\n2. Back"

        if user_input == "3":
            self.session_manager.end_session(session_id)
            return "END Thank you for using our service"

        return "CON Invalid option\n1. Check payments\n2. Exit"

    def payment_menu(self, session_id: str, user_input: str, phone_number: str):
        session = self.session_manager.get_session(session_id)
        amount = session.get("outstanding", 0)

        if user_input == "1":
            # Initialize payment here
            self.session_manager.end_session(session_id)
            # Initialize payment request.
            return f"END Payment of ${amount} initialized. You'll receive confirmation shortly."

        if user_input == "2":
            return self.main_menu(session_id)

        return "CON Invalid option\n1. Pay now\n2. Back"


ussd_menu = USSDMenu(SessionManager())
