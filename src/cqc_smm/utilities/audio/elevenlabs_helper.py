import os

from elevenlabs import Voice, VoiceSettings, generate

voice_id = os.environ['ELEVENLABS_VOICE_ID']
api_key = os.environ['ELEVENLABS_API_KEY']


def get_text_to_speech(text: str):

    # TODO: Trucate the text to 2500 unless you are using api_key
    text = text[:2500]

    audio = generate(
        api_key=api_key, # Use when using paid API key
        text=text,
        voice=Voice(
            voice_id=voice_id,
            settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
        )
    )
    return audio
