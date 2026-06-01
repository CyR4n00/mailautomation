from app.services.google_auth import get_calendar_service
from datetime import datetime, timedelta
import uuid

def create_appointment_event(summary, description, start_time_str, duration_minutes=60, attendee_email=None, generate_meet_url=True):
    """Googleカレンダーに予定を登録し、オプションでGoogle MeetのURLを生成する"""
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

        # Google MeetのURLを発行する場合の設定
        if generate_meet_url:
            event['conferenceData'] = {
                'createRequest': {
                    'requestId': str(uuid.uuid4()), # 一意のIDが必要
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            }

        # conferenceDataVersion=1 を指定しないとMeetのURLは生成されない
        event_result = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1 if generate_meet_url else 0
        ).execute()

        event_id = event_result.get('id')
        meet_url = None

        # 生成されたMeetのURLを取得する
        if generate_meet_url and 'conferenceData' in event_result:
            entry_points = event_result['conferenceData'].get('entryPoints', [])
            for point in entry_points:
                if point.get('entryPointType') == 'video':
                    meet_url = point.get('uri')
                    break

        return event_id, meet_url
    except Exception as e:
        print(f"カレンダー登録エラー: {e}")
        raise e
