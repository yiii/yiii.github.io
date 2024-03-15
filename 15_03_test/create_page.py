import os
import re

# Define the directory
directory = 'data'


mapping = {
    'audio_2024-03-12_20-39-38_Nd_1.mp3': 'A-1',
    'audio_2024-03-12_20-39-47_Nd_2.mp3': 'A-2',
    'Nadya.mp3': 'A-3',
    'audio_2024-03-12_20-41-42_Ns_1.mp3': 'B-1',
    'audio_2024-03-12_20-41-46_Ns_2.mp3': 'B-2',
    'NastyaBarat.mp3': 'B-3',
    'audio_2024-03-13_13-39-00_Rm_1.mp3': 'C-1',
    'audio_2024-03-13_13-39-03_Rm_2.mp3': 'C-2',
    'audio_2024-03-12_20-43-40_Ls_1_.mp3': 'D-1',
    'audio_2024-03-12_20-44-14_Ls_2_.mp3': 'D-2',
    'Anna1.mp3': 'E-1',
    'Anna2.mp3': 'E-2',
    'NinaVasilevna1.mp3': 'F-1',
    'NinaVasilevna2.mp3': 'F-2',
}


# Initialize the HTML
html = '''
<html>
<body>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Speaker Ref</th>
                <th>Generated</th>
                <th>FX</th>
            </tr>
        </thead>
        <tbody>
'''
all= os.listdir(directory)
# Extract the leading number from the directory name
def extract_leading_number(dir_name):
    match = re.match(r'(\d+)_', dir_name)
    return int(match.group(1)) if match else 0

# Sort the directories numerically
all = sorted(all, key=extract_leading_number)
print(all)
# Iterate over each subdirectory in the directory
for subdir in all:
    subdir_path = os.path.join(directory, subdir)

    # Skip if not a directory
    if not os.path.isdir(subdir_path):
        continue

    # List all files in the subdirectory
    files = os.listdir(subdir_path)

    # Sort the files
    files.sort()

    # Iterate over the files

    # Extract the speaker reference
    speaker_ref = next((f for f in files if  not('batch' in f)), '')
    print(speaker_ref)
    if not(speaker_ref):
        print(f"Skipping {file} as it does not contain a speaker reference.")
        continue
    # Find the corresponding _D_ and _W_ files
    d_file = next((f for f in files if '_D_' in f), '')
    w_file = next((f for f in files if  '_W_' in f), '')

    # Add a row to the HTML with media players
    html += f'''
        <tr>
            <td>{mapping.get(speaker_ref, speaker_ref)}</td>
            <td>
                {f'<audio controls><source src="{os.path.join(subdir_path, speaker_ref)}" type="audio/mpeg"></audio>' if d_file else ''}
            </td>
            <td>
                {f'<audio controls><source src="{os.path.join(subdir_path, d_file)}" type="audio/mpeg"></audio>' if d_file else ''}
            </td>
            <td>
                {f'<audio controls><source src="{os.path.join(subdir_path, w_file)}" type="audio/mpeg"></audio>' if w_file else ''}
            </td>
        </tr>
    '''

# Close the HTML
html += '''
        </tbody>
    </table>
</body>
</html>
'''

# Output HTML to a file
output_file = 'index.html'
#delete the file if it already exists
if os.path.exists(output_file):
    os.remove(output_file)
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(html)

print(f"HTML page generated successfully and saved to {output_file}.")