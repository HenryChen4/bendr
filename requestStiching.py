import os
import requests
from pydub import AudioSegment
import io

YOUR_XI_API_KEY = "d488cd4c207fbc7e59aab06edc4c4d77"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel
PARAGRAPHS = [
    "The advent of technology has transformed countless sectors, with education "
    "standing out as one of the most significantly impacted fields.",
    "In recent years, educational technology, or EdTech, has revolutionized the way "
    "teachers deliver instruction and students absorb information.",
    "From interactive whiteboards to individual tablets loaded with educational software, "
    "technology has opened up new avenues for learning that were previously unimaginable.",
    "One of the primary benefits of technology in education is the accessibility it provides.",
]
segments = []

for i, paragraph in enumerate(PARAGRAPHS):
    is_last_paragraph = i == len(PARAGRAPHS) - 1
    is_first_paragraph = i == 0
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream",
        json={
            "text": paragraph,
            "model_id": "eleven_multilingual_v2",
            "previous_text": None if is_first_paragraph else " ".join(PARAGRAPHS[:i]),
            "next_text": None if is_last_paragraph else " ".join(PARAGRAPHS[i + 1:])
        },
        headers={"xi-api-key": YOUR_XI_API_KEY},
    )

    if response.status_code != 200:
        print(f"Error encountered, status: {response.status_code}, "
               f"content: {response.text}")
        quit()

    print(f"Successfully converted paragraph {i + 1}/{len(PARAGRAPHS)}")
    segments.append(AudioSegment.from_mp3(io.BytesIO(response.content)))

segment = segments[0]
for new_segment in segments[1:]:
    segment = segment + new_segment

audio_out_path = os.path.join(os.getcwd(), "with_text_conditioning.wav")
segment.export(audio_out_path, format="wav")
print(f"Success! Wrote audio to {audio_out_path}")

