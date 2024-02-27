

import os
import re

# Constants for the base data directory and the phrases file
BASE_DATA_DIR = 'data/'
PHRASES_FILE = 'data/all_text_v3.txt'


# Read phrases from file
def read_phrases(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

# Extract index from filename
def extract_index(filename):
    match = re.search(r'section_(\d+)_output_reference.mp3', filename)
    return int(match.group(1)) if match else None

# Map audio files to their corresponding phrases
def map_audio_files(base_path):
    audio_map = {}
    for root, dirs, files in os.walk(base_path):
        speaker = os.path.basename(root)
        for file in files:
            if file.endswith('.mp3'):
                index = extract_index(file)
                if index is not None:
                    if index not in audio_map:
                        audio_map[index] = {}
                    audio_map[index][speaker] = os.path.join(root, file)
    return audio_map

# Generate HTML
def generate_html(phrases, audio_map):
    speakers = set(speaker for files in audio_map.values() for speaker in files)
    
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Files Showcase</title>
    <style>
        td { max-width: 50vw; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        audio { width: 100%; } /* Adjust if necessary */
    </style>
</head>
<body>
    <h1>Fine tunned model demo (16 epoch, 3 batch size, 9 grad) generation demo</h1>
    <section id="Demo">
        <table border="1">
            <thead>
                <tr>
                    <th>Index</th>
                    <th>Phrase</th>
    '''
    
    for speaker in sorted(speakers):
        html += f'<th>{speaker}</th>'
    
    html += '''
                </tr>
            </thead>
            <tbody>
    '''
    
    for i, phrase in enumerate(phrases):
        html += f'<tr><td>{i}</td><td>{phrase}</td>'
        for speaker in sorted(speakers):
            audio_file = audio_map.get(i, {}).get(speaker, "")
            if audio_file:
                audio_path = audio_file.replace('\\', '/')  # Ensure path is in HTML format
                html += f'<td><audio controls src="{audio_path}"></audio></td>'
            else:
                html += '<td></td>'
        html += '</tr>'
    
    html += '''
            </tbody>
        </table>
    </section>
</body>
</html>
    '''
    return html

phrases = read_phrases(PHRASES_FILE)
audio_map = map_audio_files(BASE_DATA_DIR)
html_code = generate_html(phrases, audio_map)

# Output HTML to a file
output_file = 'index.html'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(html_code)

print(f"HTML page generated successfully and saved to {output_file}.")

