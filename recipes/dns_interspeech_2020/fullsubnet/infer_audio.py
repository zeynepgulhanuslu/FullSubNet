import argparse
import os
from pathlib import Path

import librosa.util
import soundfile as sf
import toml
import torchaudio

from recipes.dns_interspeech_2020.inferencer import Inferencer

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Inference")
    parser.add_argument(
        "-C", "--config", type=str, required=True, help="Config file."
    )
    parser.add_argument(
        "-M",
        "--model_checkpoint_path",
        type=str,
        required=True,
        help="The path of the model's checkpoint.",
    )
    parser.add_argument(
        "-I",
        "--input",
        type=str,
        required=True,
        help="Input audio file or a directory that contains audio files.",
    )
    parser.add_argument(
        "-O",
        "--output_dir",
        type=str,
        required=True,
        help="The path for saving enhanced speeches.",
    )

    args = parser.parse_args()
    config_path = Path(args.config).expanduser().absolute()
    checkpoint_path = args.model_checkpoint_path
    input_audio = args.input
    output_dir = args.output_dir

    configuration = toml.load(config_path.as_posix())

    inferencer = Inferencer(configuration, checkpoint_path, None)
    print(inferencer.config)
    if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    if os.path.isfile(input_audio):
        waveform, sample_rate = torchaudio.load(input_audio)
        print("inference start")
        enhanced = inferencer.full_band_crm_mask(waveform)
        print('enhanced type:', type(enhanced))
        name = os.path.basename(input_audio)

        sf.write(os.path.join(output_dir, name), enhanced, samplerate=16000)
    else:
        noisy_files = librosa.util.find_files(input_audio, ext='wav')
        for noisy_p in noisy_files:
            waveform, sample_rate = torchaudio.load(noisy_p)
            enhanced = inferencer.full_band_crm_mask(waveform)
            name = os.path.basename(noisy_p)
            sf.write(os.path.join(output_dir, name), enhanced, samplerate=16000)
