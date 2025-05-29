import edge_tts
import io


class TextToSpeech:
    """Convert text to speech using Azure's Text-to-Speech API."""

    def __init__(self, voice: str = "en-US-GuyNeural"):
        self.voice = voice

    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech.

        Args:
            text (str): The text to convert to speech.

        Returns:
            bytes: The audio data as bytes.
        """
        communicate = edge_tts.Communicate(text, self.voice)

        buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buffer.write(chunk["data"])

        return buffer.getvalue()


if __name__ == "__main__":
    import asyncio
    import os

    async def main():
        os.makedirs("tmp", exist_ok=True)

        tts = TextToSpeech()
        audio = await tts.text_to_speech("Hello.")
        with open("tmp/output.mp3", "wb+") as f:
            f.write(audio)

    asyncio.run(main())
