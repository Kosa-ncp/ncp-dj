from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import requests
import os
import base64
import json
import time
from dotenv import load_dotenv

# .env 로드
load_dotenv()

app = Flask(__name__)
CORS(app)

# 환경 변수
HYPERCLOVA_API_KEY = os.getenv('HYPERCLOVA_API_KEY')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# ===== HyperClova API =====
class HyperClovaAPI:
    API_URL = "https://clovastudio.stream.ntruss.com/v1/chat-completions/HCX-003"

    def __init__(self, api_key):
        self.headers = {
            'Authorization': "Bearer " + api_key,
            'Content-Type': 'application/json'
        }

    def chat_completion(self, messages, max_tokens=100, temperature=0.3, retries=3, delay=2):
        payload = {
            'messages': messages,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': max_tokens,
            'temperature': temperature,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': True
        }
        for attempt in range(1, retries + 1):
          try:
              resp = requests.post(self.API_URL, headers=self.headers, json=payload, timeout=30)
              resp.raise_for_status()
              return resp.json()
          except Exception as e:
              print(f"[HyperClovaAPI] 시도 {attempt} 실패: {e}")
              if attempt < retries:
                  print(f"[HyperClovaAPI] {delay}초 후 재시도...")
                  time.sleep(delay)
              else:
                  print("[HyperClovaAPI] 모든 재시도 실패")
                  return None

hyperclova_api = HyperClovaAPI(HYPERCLOVA_API_KEY)

# ===== Spotify API =====
class SpotifyAPI:
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    SEARCH_URL = 'https://api.spotify.com/v1/search'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires = None

    def get_access_token(self):
        if self.access_token and self.token_expires and datetime.now() < self.token_expires:
            return self.access_token
        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {'Authorization': f'Basic {auth}'}
        data = {'grant_type': 'client_credentials'}
        try:
            resp = requests.post(self.TOKEN_URL, headers=headers, data=data, timeout=5)
            resp.raise_for_status()
            token_info = resp.json()
            self.access_token = token_info['access_token']
            self.token_expires = datetime.now() + timedelta(seconds=token_info['expires_in'] - 60)
            return self.access_token
        except Exception as e:
            print(f"[SpotifyAPI] 토큰 획득 실패: {e}")
            return None

    def search_track(self, query, limit=1):
        token = self.get_access_token()
        if not token:
            return None
        headers = {'Authorization': f'Bearer {token}'}
        params = {'q': query, 'type': 'track', 'limit': limit, 'market': 'KR'}
        try:
            resp = requests.get(self.SEARCH_URL, headers=headers, params=params, timeout=60)
            resp.raise_for_status()
            tracks = resp.json().get('tracks', {}).get('items', [])
            if tracks:
                track = tracks[0]
                return {
                    'spotify_url': track['external_urls']['spotify'],
                    'preview_url': track['preview_url'],
                    'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'duration_ms': track['duration_ms']
                }
        except Exception as e:
            print(f"[SpotifyAPI] 트랙 검색 실패: {e}")
        return None

spotify_api = SpotifyAPI(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

# ===== 감정 분석 =====
def analyze_emotion(text):
    messages = [
        {"role": "system", "content": """당신은 감정 분석 전문가입니다.
        사용자 텍스트를 분석해서 기쁨, 슬픔, 화남, 평온, 외로움, 설렘, 불안, 그리움 중 하나로 분류하고
        JSON 형식으로 반환하세요:
        {"emotion": "감정명", "intensity": 1-10, "keywords": ["키워드1", "키워드2"]}""" },
        {"role": "user", "content": text}
    ]
    result = hyperclova_api.chat_completion(messages, max_tokens=200)
    time.sleep(1)
    if result and 'result' in result and 'message' in result['result']:
        try:
            return json.loads(result['result']['message']['content'])
        except:
            pass
    return {"emotion": "평온", "intensity": 5, "keywords": []}

# ===== 음악 추천 =====
def recommend_music(emotion, intensity, keywords):
    prompt = f"""
    감정: {emotion}
    강도: {intensity}/10
    키워드: {', '.join(keywords)}
    위 감정에 맞는 한국 음악 5곡 추천 (JSON 형식):
    {{ "recommendations": [{{"title":"곡제목","artist":"아티스트명","genre":"장르","reason":"추천 이유"}}] }}
    """
    messages = [{"role": "system", "content": "당신은 음악 추천 전문가입니다."},
                {"role": "user", "content": prompt}]
    result = hyperclova_api.chat_completion(messages, max_tokens=800, temperature=0.7)
    if result and 'result' in result and 'message' in result['result']:
        try:
            return json.loads(result['result']['message']['content'])['recommendations']
        except:
            pass
    # 기본 추천곡
    return [
        {"title": "Spring Day", "artist": "BTS", "genre": "K-Pop", "reason": "감성적"},
        {"title": "Through the Night", "artist": "IU", "genre": "Ballad", "reason": "편안한 멜로디"}
    ]

# ===== Flask Routes =====
@app.route('/')
def home():
    return jsonify({"message": "MoodTunes API 서버 실행중", "version": "2.0.0", "ai_provider": "HyperClova X"})

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "spotify_enabled": bool(SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET)
    })

@app.route('/api/analyze-mood', methods=['POST'])
def analyze_mood():
    data = request.get_json()
    mood_text = data.get('mood', '').strip()
    if not mood_text:
        return jsonify({"error": "mood를 입력해주세요"}), 400

    emotion_data = analyze_emotion(mood_text)
    recommendations = recommend_music(emotion_data['emotion'], emotion_data['intensity'], emotion_data['keywords'])

    # Spotify 링크 추가
    for rec in recommendations:
        spotify_info = spotify_api.search_track(f"{rec['title']} {rec['artist']}")
        if spotify_info:
            rec.update(spotify_info)

    return jsonify({
        "success": True,
        "analysis": emotion_data,
        "recommendations": recommendations,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    print("[FEEDBACK]", data)
    return jsonify({"success": True, "message": "피드백 저장 완료"})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint를 찾을 수 없습니다"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "서버 내부 오류"}), 500

if __name__ == "__main__":
    print("🎵 MoodTunes Flask 서버 2.0 시작…")
    app.run(debug=True, host="0.0.0.0", port=5000)
