from app.services.google_auth import get_calendar_service
from datetime import datetime, timedelta

def create_appointment_event(summary, description, start_time_str, duration_minutes=60, attendee_email=None):
    """Googleカレンダーに予定を登録する"""
    try:
        service = get_calendar_service()

        # 'YYYY-MM-DDTHH:MM' 形式を想定
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        end_time = start_time + timedelta(minutes=duration_minutes)

        event = {
          'summary': summary,
          'description': description,
          'start': {
            'dateTime': start_time.isoformat() + ':00+09:00', # 日本時間を想定
            'timeZone': 'Asia/Tokyo',
          },
          'end': {
            'dateTime': end_time.isoformat() + ':00+09:00',
            'timeZone': 'Asia/Tokyo',
          },
        }

        if attendee_email:
            event['attendees'] = [{'email': attendee_email}]

        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return event_result.get('id')
    except Exception as e:
        print(f"カレンダー登録エラー: {e}")
        raise e
