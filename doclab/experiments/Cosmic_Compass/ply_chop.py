import os

# --- CONFIGURATION ---
file_path = "pirouette_deep_field.ply"
# The error index from CloudCompare (Vertex number)
bad_vertex_index = 13905528 
# ---------------------

def repair_ply():
    print(f"Analyzing {file_path}...")
    
    # Create a name for the fixed file
    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    new_path = os.path.join(dir_name, "FIXED_" + base_name)
    
    header_lines = []
    header_ended = False
    vertex_count = 0
    current_vertex_index = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as infile, \
             open(new_path, 'w', encoding='utf-8') as outfile:
            
            # PHASE 1: PROCESS HEADER AND WRITE IT LATER
            for line in infile:
                if not header_ended:
                    if "element vertex" in line:
                        # We will replace this line later with the new count
                        header_lines.append("ELEMENT_VERTEX_PLACEHOLDER\n")
                    elif "end_header" in line:
                        header_lines.append(line)
                        header_ended = True
                        print("Header found. Streaming data...")
                        
                        # Write the header now, but with the TRUNCATED count
                        # We set the count to the index where it crashed, 
                        # effectively deleting the rest of the file.
                        for h_line in header_lines:
                            if h_line == "ELEMENT_VERTEX_PLACEHOLDER\n":
                                outfile.write(f"element vertex {bad_vertex_index - 1}\n")
                            else:
                                outfile.write(h_line)
                    else:
                        header_lines.append(line)
                    continue
                
                # PHASE 2: STREAM BODY DATA
                # We are now in the data body.
                # Stop writing EXACTLY before the bad line.
                if current_vertex_index < (bad_vertex_index - 1):
                    outfile.write(line)
                    current_vertex_index += 1
                    
                    if current_vertex_index % 1000000 == 0:
                        print(f"Processed {current_vertex_index} vertices...")
                
                elif current_vertex_index == (bad_vertex_index - 1):
                    # We reached the bad line. Let's look at it!
                    print("\n--- CRASH REPORT ---")
                    print(f"Stopped at vertex {current_vertex_index + 1}.")
                    print(f"The Next Line (The Culprit) looks like this:")
                    print(f"'{line.strip()}'")
                    print("--------------------")
                    print("Truncating file here to save valid data.")
                    break

        print(f"\nSUCCESS! Saved cleaned file to: {new_path}")
        print("You can now import this FIXED file into Blender or CloudCompare.")

    except Exception as e:
        print(f"Script Error: {e}")

repair_ply()