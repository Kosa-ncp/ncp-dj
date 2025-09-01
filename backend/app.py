from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import requests
import base64
import json
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # React 앱과의 통신을 위해 CORS 활성화

# 환경 변수 설정
openai.api_key = os.getenv('OPENAI_API_KEY')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

class SpotifyAPI:
    def __init__(self):
        self.access_token = None
        self.token_expires = None

    def get_access_token(self):
        """Spotify Access Token 획득"""
        if self.access_token and self.token_expires and datetime.now() < self.token_expires:
            return self.access_token

        auth_url = 'https://accounts.spotify.com/api/token'
        auth_header = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()

        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {'grant_type': 'client_credentials'}

        response = requests.post(auth_url, headers=headers, data=data)

        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.token_expires = datetime.now() + timedelta(seconds=token_data['expires_in'] - 60)
            return self.access_token

        return None

    def search_track(self, query, limit=1):
        """Spotify에서 트랙 검색"""
        token = self.get_access_token()
        if not token:
            return None

        search_url = 'https://api.spotify.com/v1/search'
        headers = {'Authorization': f'Bearer {token}'}
        params = {
            'q': query,
            'type': 'track',
            'limit': limit,
            'market': 'KR'
        }

        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if data['tracks']['items']:
                track = data['tracks']['items'][0]
                return {
                    'spotify_url': track['external_urls']['spotify'],
                    'preview_url': track['preview_url'],
                    'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'duration_ms': track['duration_ms']
                }

        return None

spotify_api = SpotifyAPI()

def analyze_emotion_with_openai(mood_text):
    """OpenAI를 사용하여 감정 분석"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """당신은 감정 분석 전문가입니다.
                    사용자의 텍스트를 분석해서 다음 중 하나의 감정으로 분류해주세요:
                    - 기쁨 (joy)
                    - 슬픔 (sadness)
                    - 화남 (anger)
                    - 평온 (calm)
                    - 외로움 (loneliness)
                    - 설렘 (excitement)
                    - 불안 (anxiety)
                    - 그리움 (nostalgia)

                    응답은 반드시 JSON 형식으로 해주세요:
                    {"emotion": "감정명", "intensity": 1-10, "keywords": ["키워드1", "키워드2"]}
                    """
                },
                {
                    "role": "user",
                    "content": mood_text
                }
            ],
            max_tokens=200,
            temperature=0.3
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        print(f"감정 분석 오류: {e}")
        return {"emotion": "평온", "intensity": 5, "keywords": []}

def get_music_recommendations(emotion, intensity, keywords):
    """감정에 기반한 음악 추천"""
    try:
        prompt = f"""
        감정: {emotion}
        강도: {intensity}/10
        키워드: {', '.join(keywords)}

        위 감정에 맞는 한국 음악 5곡을 추천해주세요.
        K-Pop, 인디, 발라드, R&B 등 다양한 장르를 포함해주세요.

        응답 형식 (JSON):
        {{
            "recommendations": [
                {{
                    "title": "곡제목",
                    "artist": "아티스트명",
                    "genre": "장르",
                    "reason": "추천 이유"
                }}
            ]
        }}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 음악 추천 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )

        result = json.loads(response.choices[0].message.content)
        return result['recommendations']

    except Exception as e:
        print(f"음악 추천 오류: {e}")
        # 기본 추천곡 반환
        return [
            {"title": "Spring Day", "artist": "BTS", "genre": "K-Pop", "reason": "감성적이고 위로가 되는 곡"},
            {"title": "Through the Night", "artist": "IU", "genre": "Ballad", "reason": "따뜻하고 편안한 멜로디"},
            {"title": "Palette", "artist": "IU ft. G-Dragon", "genre": "R&B", "reason": "세련되고 감성적인 분위기"},
        ]

@app.route('/')
def home():
    """API 상태 확인"""
    return jsonify({
        "message": "MoodTunes API 서버가 실행중입니다!",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze-mood [POST]",
            "health": "/api/health [GET]"
        }
    })

@app.route('/api/health')
def health_check():
    """서버 상태 확인"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/analyze-mood', methods=['POST'])
def analyze_mood():
    """감정 분석 및 음악 추천 메인 엔드포인트"""
    try:
        # 요청 데이터 검증
        data = request.get_json()
        if not data or 'mood' not in data:
            return jsonify({"error": "기분/상황을 입력해주세요"}), 400

        mood_text = data['mood'].strip()
        if not mood_text:
            return jsonify({"error": "기분/상황을 입력해주세요"}), 400

        # 1단계: 감정 분석
        print(f"감정 분석 시작: {mood_text}")
        emotion_result = analyze_emotion_with_openai(mood_text)

        # 2단계: 음악 추천
        print(f"음악 추천 시작: {emotion_result}")
        recommendations = get_music_recommendations(
            emotion_result['emotion'],
            emotion_result['intensity'],
            emotion_result['keywords']
        )

        # 3단계: Spotify 링크 추가 (선택사항)
        enhanced_recommendations = []
        for song in recommendations:
            song_data = song.copy()

            # Spotify에서 실제 곡 검색
            search_query = f"{song['title']} {song['artist']}"
            spotify_info = spotify_api.search_track(search_query)

            if spotify_info:
                song_data.update(spotify_info)

            enhanced_recommendations.append(song_data)

        # 응답 데이터 구성
        response_data = {
            "success": True,
            "analysis": {
                "original_text": mood_text,
                "detected_emotion": emotion_result['emotion'],
                "intensity": emotion_result['intensity'],
                "keywords": emotion_result['keywords']
            },
            "recommendations": enhanced_recommendations,
            "timestamp": datetime.now().isoformat()
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"서버 오류: {e}")
        return jsonify({
            "success": False,
            "error": "서버에서 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        }), 500

@app.route('/api/feedback', methods=['POST'])
def feedback():
    """사용자 피드백 수집"""
    try:
        data = request.get_json()
        feedback_type = data.get('type')  # 'like' 또는 'dislike'
        song_info = data.get('song_info')
        emotion = data.get('emotion')

        # 피드백 데이터 로깅/저장 (실제로는 DB에 저장)
        print(f"피드백 수집: {feedback_type} - {song_info} - {emotion}")

        return jsonify({
            "success": True,
            "message": "피드백이 성공적으로 저장되었습니다."
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": "피드백 저장에 실패했습니다."
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "요청한 엔드포인트를 찾을 수 없습니다."}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "내부 서버 오류가 발생했습니다."}), 500

if __name__ == '__main__':
    # 환경 변수 확인
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY 환경 변수가 설정되지 않았습니다!")

    if not os.getenv('SPOTIFY_CLIENT_ID') or not os.getenv('SPOTIFY_CLIENT_SECRET'):
        print("⚠️  Spotify API 키가 설정되지 않았습니다. Spotify 기능은 비활성화됩니다.")

    print("🎵 MoodTunes Flask 서버 시작…")
    app.run(debug=True, host='0.0.0.0', port=5000)