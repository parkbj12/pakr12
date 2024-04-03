#실습문제 3번
import openai


API_KEY = "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"
client = openai.OpenAI(api_key = API_KEY)

audio_file = open("output.mp3", "rb")

transcript = client.audio.transcriptions.create(model = "whisper-1", file = audio_file)

print(transcript.text)