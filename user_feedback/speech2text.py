"""
A short script that takes a .wav file and converts it to text
"""

from argparse import ArgumentParser
from transformers import pipeline

def main():
    parser = ArgumentParser(description="Process the provided audio file to text")
    parser.add_argument("--input", type=str, help="The input file to process")

    asr = pipeline(
            task="automatic-speech-recognition",
            model= "facebook/wav2vec2-base-960h",
            tokenizer= "facebook/wav2vec2-base-960h",
            )
    args = parser.parse_args()
    text = asr(args.input)["text"]
    print(text)

if __name__ == "__main__":
    main()

