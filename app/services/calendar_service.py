from app.services.google_auth import get_calendar_service
from datetime import datetime, timedelta
import uuid

def create_appointment_event(summary, description, start_time_str, duration_minutes=60, attendee_email=None, generate_meet_url=True):
    """Googleカレンダーに予定を登録し、オプションでGoogle MeetのURLを生成する"""
    try:
        service = get_calendar_service()

        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        end_time = start_time + timedelta(minutes=duration_minutes)

        start_iso = start_time.strftime('%Y-%m-%dT%H:%M:%S') + '+09:00'
        end_iso = end_time.strftime('%Y-%m-%dT%H:%M:%S') + '+09:00'

        event = {
          'summary': summary,
          'description': description,
          'start': {
            'dateTime': start_iso,
            'timeZone': 'Asia/Tokyo',
          },
          'end': {
            'dateTime': end_iso,
            'timeZone': 'Asia/Tokyo',
          },
        }

        if attendee_email:
            event['attendees'] = [{'email': attendee_email}]

        if generate_meet_url:
            event['conferenceData'] = {
                'createRequest': {
                    'requestId': str(uuid.uuid4()),
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            }

        try:
            event_result = service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1 if generate_meet_url else 0
            ).execute()
        except Exception as api_err:
            # 無料のGmailアカウント等でMeetの自動生成が許可されていない場合のエラーハンドリング
            if generate_meet_url and '400' in str(api_err) and 'badRequest' in str(api_err):
                print(f"Meetの自動生成に失敗しました。通常の予定として登録を試みます。エラー詳細: {api_err}")
                # Meet自動生成部分を外して再試行
                event.pop('conferenceData', None)
                event_result = service.events().insert(
                    calendarId='primary',
                    body=event,
                    conferenceDataVersion=0
                ).execute()
                # MeetURLは発行できなかったことを呼び出し元に伝えるために特殊な文字列等を返すこともできるが、
                # 今回は単純に None にしてエラーを出さない運用にする
                return event_result.get('id'), None
            else:
                raise api_err

        event_id = event_result.get('id')
        meet_url = None

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
