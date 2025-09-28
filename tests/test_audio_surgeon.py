# /tests/test_audio_surgeon.py

import unittest
import os
import sys
import shutil
import pandas as pd
from pydub import AudioSegment

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.audio_surgeon_agent import splice_audio

class TestAudioSurgeon(unittest.TestCase):
    def setUp(self):
        self.test_dir = "temp_test_dir_for_surgeon"
        self.meow_dir = os.path.join(self.test_dir, "meow_library", "processed")
        os.makedirs(self.meow_dir, exist_ok=True)

        self.db_path = os.path.join(self.meow_dir, "meow_database.csv")
        meow_paths = [
            os.path.join("processed", "meow_short.wav"),
            os.path.join("processed", "meow_long.wav")
        ]
        meow_data = {'path': meow_paths, 'duration': [0.5, 1.5], 'pitch': [300, 200]}
        pd.DataFrame(meow_data).to_csv(self.db_path, index=False)

        AudioSegment.silent(duration=500).export(os.path.join(self.meow_dir, "meow_short.wav"), format="wav")
        AudioSegment.silent(duration=1500).export(os.path.join(self.meow_dir, "meow_long.wav"), format="wav")

        self.source_audio_path = os.path.join(self.test_dir, "source.wav")
        AudioSegment.silent(duration=10000).export(self.source_audio_path, format="wav")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_splicing_and_file_creation(self):
        print("\n--- Running Test Case: Audio Splicing and File Creation ---")
        
        censor_times = [
            {'start_time': 1.0, 'end_time': 1.4},
            {'start_time': 5.0, 'end_time': 6.6}
        ]
        
        # *** FIX APPLIED HERE ***
        # By changing the current working directory, we ensure the output file
        # is created inside our temporary folder, making cleanup easy.
        original_cwd = os.getcwd()
        try:
            os.chdir(self.test_dir)
            # Use relative paths from within the temp directory
            source_path_relative = os.path.basename(self.source_audio_path)
            db_path_relative = os.path.join("meow_library", "processed", "meow_database.csv")

            output_path = splice_audio(source_path_relative, censor_times, db_path_relative)
            
            print(f"Source Audio: {source_path_relative}")
            print(f"Censor Times: {censor_times}")
            print(f"Agent Output Path: {output_path}")

            self.assertTrue(os.path.exists(output_path), "The censored audio file was not created.")

            source_duration = len(AudioSegment.from_file(source_path_relative))
            output_duration = len(AudioSegment.from_file(output_path))
            self.assertAlmostEqual(source_duration, output_duration, delta=50,
                                   msg=f"Output audio duration is significantly different from source. Source: {source_duration}, Output: {output_duration}")
        finally:
            # Always change back to the original directory
            os.chdir(original_cwd)
            
        print("--- Test Case: Passed ---")

if __name__ == '__main__':
    unittest.main()