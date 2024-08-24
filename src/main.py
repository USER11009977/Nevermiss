import re

def parse_osu_file(osu_file_path):
    notes = []
    with open(osu_file_path, 'r') as file:
        lines = file.readlines()
    
    hit_objects_section = False
    for line in lines:
        line = line.strip()
        if line.startswith('[HitObjects]'):
            hit_objects_section = True
            continue
        if hit_objects_section:
            if not line:
                break
            # osu! hit object format: x,y,time,type,0,0:0:0:0:
            parts = line.split(',')
            x = int(parts[0])
            y = int(parts[1])
            time = int(parts[2])
            note_type = int(parts[3])
            
            # Convert osu! coordinates to Roblox lane positions
            # osu! x in range [0, 512], convert to Roblox lane (1-4)
            position = int(x // 128) + 1
            note_type_str = "hold" if note_type & 2 else "normal"
            
            notes.append({
                'time': time / 1000.0,  # Convert milliseconds to seconds
                'position': position,
                'type': note_type_str,
                'duration': 0.5 if note_type & 2 else 0  # Example duration
            })
    
    return notes

def generate_roblox_chart(notes, output_file_path):
    with open(output_file_path, 'w') as file:
        file.write("local Chart = {}\n\n")
        file.write("Chart.Notes = {\n")
        for note in notes:
            file.write(f"    {{time = {note['time']}, position = {note['position']}, type = '{note['type']}', duration = {note['duration']}}},\n")
        file.write("}\n\n")
        file.write("return Chart")

if __name__ == "__main__":
    osu_file_path = 'chart.osu'
    output_file_path = 'chart.lua'
    notes = parse_osu_file(osu_file_path)
    generate_roblox_chart(notes, output_file_path)
    print(f"Converted osu! chart to Roblox format: {output_file_path}")
