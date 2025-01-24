"""
NotificationHandler.py handles desktop notifications for the chat application.

The NotificationHandler class provides methods to display desktop notifications for 
new messages, private messages, and unread message counts using the plyer library
for cross-platform notification support.

@author Osagie Owie
@email owieo204@potsdam.edu
"""

from plyer import notification

class NotificationHandler:
    """
    Initialize notification handler and set default state
    
    @param self NotificationHandler instance
    """
    def __init__(self):
        self.notification_enabled = True

    """
    notify Display a notification with given title and message
    
    @param self NotificationHandler instance
    @param title String notification title
    @param message String notification message
    """
    def notify(self, title, message):
        if not self.notification_enabled:
            return

        # Attempt to show notification    
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="ChitChat",
                timeout=5
            )
        except Exception:
            pass # Ignore notification errors

    """
    toggle_notifications Enable/disable notifications
    
    @param self NotificationHandler instance
    @return Boolean new notification state
    """
    def toggle_notifications(self):
        self.notification_enabled = not self.notification_enabled
        return self.notification_enabled

    """
    notify_new_message Show notification for new chat message
    
    @param self NotificationHandler instance
    @param sender String username of message sender
    @param message String message content
    """
    def notify_new_message(self, sender, message):
        self.notify("New Message", f"From {sender}: {message[:50]}")

    """
    notify_private_message Show notification for private message
    
    @param self NotificationHandler instance  
    @param sender String username of message sender
    @param message String message content
    """
    def notify_private_message(self, sender, message):
        self.notify("Private Message", f"From {sender}: {message[:50]}")

    """
    notify_unread_messages Show notification for unread message count
    
    @param self NotificationHandler instance
    @param count Integer number of unread messages
    """
    def notify_unread_messages(self, count):
        self.notify("Unread Messages", f"You have {count} unread message(s)")