"""
A short script that takes a .wav file and converts it to text
"""

from transformers import pipeline

def main():
    asr = pipeline(
            task="automatic-speech-recognition",
            model= "facebook/wav2vec2-base-960h",
            tokenizer= "facebook/wav2vec2-base-960h",
            )

    text = asr("test.wav")["text"]
    print(text)

if __name__ == "__main__":
    main()

