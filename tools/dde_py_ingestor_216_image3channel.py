def main():
    import os, sys, math, json, struct, logging, sqlite3, time
    import numpy as np
    import pandas as pd
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from collections import defaultdict
    from dateutil import parser as date_parser
    import faiss


    # ----------------- Logging Configuration -----------------
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        datefmt="%H:%M:%S")
    logger = logging.getLogger(__name__)

    # ----------------- libvips DLL Setup -----------------
    def get_dll_directory(default_path=None):
        if default_path and os.path.isdir(default_path):
            logger.debug("Using default DLL folder: %s", default_path)
            return default_path
        root = tk.Tk()
        root.withdraw()
        folder = filedialog.askdirectory(title="Select folder containing libvips DLLs")
        if not folder:
            messagebox.showerror("Error", "No folder selected for DLLs.")
            sys.exit(1)
        logger.debug("Selected DLL folder: %s", folder)
        root.destroy()
        return folder

    default_dll_folder = r"C:\libvips\bin"
    dll_folder = get_dll_directory(default_dll_folder)
    logger.debug("DLL folder contents: %s", os.listdir(dll_folder))
    try:
        os.add_dll_directory(dll_folder)
    except Exception as e:
        logger.exception("Error adding DLL directory:")
        sys.exit(1)
    os.environ["PATH"] = dll_folder + os.pathsep + os.environ.get("PATH", "")
    dll_candidate = os.path.join(dll_folder, "libvips-42.dll")
    if not os.path.exists(dll_candidate):
        dll_candidate = os.path.join(dll_folder, "vips-42.dll")
        if not os.path.exists(dll_candidate):
            sys.exit("Error: libvips DLL not found.")
    os.environ["VIPS_LIBRARY"] = dll_candidate
    try:
        import pyvips
        pyvips.cache_set_max(0)
        logger.debug("libvips version: %s", pyvips.version(0))
    except Exception as e:
        logger.exception("Error loading pyvips:")
        sys.exit("Error loading pyvips: " + str(e))

    # ----------------- Database Setup -----------------
    def init_text_mapping_db(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS text_mapping (
                col_name TEXT,
                text_value TEXT,
                code INTEGER,
                PRIMARY KEY (col_name, text_value)
            )
        """)
        conn.commit()
        return conn

    def init_metadata_table(conn):
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS image_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT,
                num_columns INTEGER,
                header_order TEXT,
                stats_json TEXT,
                column_types_json TEXT,
                reversal_data_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

    # ----------------- Reversible Encoding Functions -----------------
    def encode_numeric_cell(cell, col, stats):
        try:
            num = float(cell) if cell != "" else float('nan')
        except ValueError:
            return (0, 0, 0, 255)
        stat = stats.get(col, {})
        if stat.get("min_log") is not None and stat.get("max_log") is not None:
            num_for_log = num if num > 0 else 1e-9
            log_val = math.log(num_for_log)
            min_log, max_log = stat["min_log"], stat["max_log"]
            normalized = int(round((log_val - min_log) / (max_log - min_log) * (2**32 - 1))) if max_log != min_log else 0
        else:
            normalized = int.from_bytes(struct.pack("!f", num), byteorder="big")
        return ((normalized >> 24) & 0xFF, (normalized >> 16) & 0xFF, (normalized >> 8) & 0xFF, normalized & 0xFF)

    def encode_timestamp_cell(cell, col, stats):
        try:
            ts = date_parser.parse(cell).timestamp()
        except Exception:
            return (0, 0, 0, 255)
        stat = stats.get(col, {})
        if stat.get("min_log") is not None and stat.get("max_log") is not None:
            ts_for_log = ts if ts > 0 else 1e-9
            log_val = math.log(ts_for_log)
            min_log, max_log = stat["min_log"], stat["max_log"]
            normalized = int(round((log_val - min_log) / (max_log - min_log) * (2**32 - 1))) if max_log != min_log else 0
        else:
            normalized = int.from_bytes(struct.pack("!f", ts), byteorder="big")
        return ((normalized >> 24) & 0xFF, (normalized >> 16) & 0xFF, (normalized >> 8) & 0xFF, normalized & 0xFF)

    def get_or_create_code(conn, col, text_value):
        c = conn.cursor()
        c.execute("SELECT code FROM text_mapping WHERE col_name = ? AND text_value = ?", (col, text_value.strip()))
        row = c.fetchone()
        if row is not None:
            return row[0]
        c.execute("SELECT MAX(code) FROM text_mapping WHERE col_name = ?", (col,))
        row = c.fetchone()
        next_code = 0 if row[0] is None else int(row[0]) + 1
        c.execute("INSERT INTO text_mapping (col_name, text_value, code) VALUES (?, ?, ?)", (col, text_value.strip(), next_code))
        conn.commit()
        return next_code

    def encode_text_cell(cell, col, mapping_conn):
        code = get_or_create_code(mapping_conn, col, cell)
        return ((code >> 24) & 0xFF, (code >> 16) & 0xFF, (code >> 8) & 0xFF, code & 0xFF)

    # ----------------- Helper for Numpy Conversion -----------------
    def convert_np(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert_np(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_np(x) for x in obj]
        else:
            return obj

    # ----------------- Vectorized CSV Ingestion -----------------
    def ingest_csv_vectorized(file_path):
        try:
            df = pd.read_csv(file_path, engine='c', encoding='utf-8-sig')
        except Exception as e:
            logger.exception("Error reading file %s: %s", file_path, e)
            return None, None, None
        headers = df.columns.tolist()
        stats = {}
        column_types = {}
        for col in headers:
            try:
                series = pd.to_numeric(df[col], errors='coerce')
                if series.notna().sum() > 0:
                    stats[col] = {'min': series.min(), 'max': series.max()}
                    column_types[col] = "numeric"
                    continue
            except Exception:
                pass
            try:
                dt_series = pd.to_datetime(df[col], errors='coerce')
                if dt_series.notna().sum() > 0:
                    ts_series = dt_series.astype('int64') / 1e9
                    stats[col] = {'min': ts_series.min(), 'max': ts_series.max()}
                    column_types[col] = "timestamp"
                    continue
            except Exception:
                pass
            column_types[col] = "text"
            stats[col] = {'min': 0, 'max': 0}
        for col, s in stats.items():
            if s['min'] > 0:
                s['min_log'] = math.log(s['min'])
                s['max_log'] = math.log(s['max'])
            else:
                s['min_log'] = math.log(1e-9)
                s['max_log'] = math.log(max(s['max'], 1e-9))
        return headers, stats, df.values.tolist()

    # ----------------- Merging Ecosystems -----------------
    def merge_ecosystems(ecosystems):
        # Simple merge: assume same header order; concatenate rows and update stats.
        merged = {
            "file": ", ".join([eco["file"] for eco in ecosystems]),
            "headers": ecosystems[0]["headers"],
            "stats": ecosystems[0]["stats"],
            "column_types": ecosystems[0]["column_types"],
            "rows": []
        }
        for eco in ecosystems:
            merged["rows"].extend(eco["rows"])
            for col in merged["headers"]:
                try:
                    merged["stats"][col]["min"] = min(merged["stats"][col]["min"], eco["stats"][col]["min"])
                    merged["stats"][col]["max"] = max(merged["stats"][col]["max"], eco["stats"][col]["max"])
                except Exception:
                    pass
        return merged

    # ----------------- Square Image Generation -----------------
    def build_square_image(data_rows, dtype, bands, format_str):
        if not data_rows:
            return None
        arr = np.array(data_rows, dtype=dtype).reshape((-1, bands))
        total_pixels = arr.shape[0]
        new_width = int(math.ceil(math.sqrt(total_pixels)))
        new_height = int(math.ceil(total_pixels / new_width))
        padded = np.zeros((new_height * new_width, bands), dtype=dtype)
        padded[:total_pixels] = arr
        padded = padded.reshape((new_height, new_width, bands))
        return pyvips.Image.new_from_memory(padded.tobytes(), new_width, new_height, bands, format_str)

    # ----------------- Generate Channel Images -----------------
    def generate_channel_images(file_rows, headers, stats, column_types, output_folder, mapping_conn):
        numeric_rows = []
        timestamp_rows = []
        text_values = defaultdict(list)
        for row in file_rows:
            row_numeric = []
            row_timestamp = []
            for i, cell in enumerate(row):
                col = headers[i]
                typ = column_types.get(col, "text")
                if typ == "numeric":
                    try:
                        cell_val = cell.strip() if isinstance(cell, str) else cell
                        row_numeric.append(encode_numeric_cell(cell_val, col, stats))
                    except Exception as e:
                        logger.debug("Error encoding numeric cell (%s): %s", cell, e)
                        row_numeric.append((0, 0, 0, 255))
                elif typ == "timestamp":
                    try:
                        cell_val = cell.strip() if isinstance(cell, str) else str(cell)
                        row_timestamp.append(encode_timestamp_cell(cell_val, col, stats))
                    except Exception as e:
                        logger.debug("Error encoding timestamp cell (%s): %s", cell, e)
                        row_timestamp.append((0, 0, 0, 255))
                else:
                    try:
                        cell_val = cell.strip() if isinstance(cell, str) else str(cell)
                        text_values[col].append(cell_val)
                    except Exception as e:
                        logger.debug("Error processing text cell (%s): %s", cell, e)
                        text_values[col].append("")
            if row_numeric:
                numeric_rows.append(row_numeric)
            if row_timestamp:
                timestamp_rows.append(row_timestamp)
        numeric_img = build_square_image(numeric_rows, np.uint8, 4, "uchar")
        timestamp_img = build_square_image(timestamp_rows, np.uint8, 4, "uchar")
        all_text = []
        for col in headers:
            if column_types.get(col) == "text":
                all_text.extend(text_values[col])
        if all_text:
            unique_text = list(set(all_text))
            text_pixels = []
            for txt in unique_text:
                try:
                    text_pixels.append(encode_text_cell(txt, "text_lib", mapping_conn))
                except Exception as e:
                    logger.debug("Error encoding text cell (%s): %s", txt, e)
                    text_pixels.append((0, 0, 0, 255))
            def build_text_image(pixels, dtype, bands, format_str):
                total = len(pixels)
                side = int(math.ceil(math.sqrt(total)))
                padded = np.array(pixels, dtype=dtype)
                if padded.shape[0] < side*side:
                    pad_count = side*side - padded.shape[0]
                    padded = np.concatenate([padded, np.zeros((pad_count, bands), dtype=dtype)], axis=0)
                padded = padded.reshape((side, side, bands))
                return pyvips.Image.new_from_memory(padded.tobytes(), side, side, bands, format_str)
            text_img = build_text_image(text_pixels, np.uint8, 4, "uchar")
        else:
            text_img = None
        outputs = {}
        if numeric_img:
            num_path = os.path.join(output_folder, "numeric.png")
            numeric_img.write_to_file(num_path)
            outputs["numeric"] = num_path
        if timestamp_img:
            ts_path = os.path.join(output_folder, "timestamp.png")
            timestamp_img.write_to_file(ts_path)
            outputs["timestamp"] = ts_path
        if text_img:
            text_path = os.path.join(output_folder, "text_library.png")
            text_img.write_to_file(text_path)
            outputs["text"] = text_path
        return outputs

    # ----------------- FAISS Streaming -----------------
    global_faiss_index = None
    global_faiss_metadata_conn = None
    def init_faiss_stream(metadata_db_path, vector_dim):
        nonlocal global_faiss_index, global_faiss_metadata_conn
        global_faiss_index = faiss.IndexFlatL2(vector_dim)
        global_faiss_metadata_conn = sqlite3.connect(metadata_db_path)
        c = global_faiss_metadata_conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS faiss_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vector_index INTEGER,
                ecosystem TEXT,
                image_path TEXT,
                channel TEXT,
                rgba TEXT,
                positions TEXT
            )
        """)
        global_faiss_metadata_conn.commit()
        logger.debug("Initialized FAISS with dim %d", vector_dim)

    def stream_image_to_faiss(image_path, channel, ecosystem, target_width, target_height, target_cols):
        logger.debug(f"Streaming FAISS vectors for {image_path} (channel: {channel})")
        try:
            vimg = pyvips.Image.new_from_file(image_path, access="sequential")
        except Exception as e:
            logger.error(f"Error loading {image_path}: {e}")
            return
        scale = min(target_width / vimg.width, target_height / vimg.height, 1.0)
        if scale < 1.0:
            vimg = vimg.resize(scale)
        try:
            arr = np.ndarray(buffer=vimg.write_to_memory(), dtype=np.uint8,
                             shape=[vimg.height, vimg.width, vimg.bands])
        except Exception as e:
            logger.error(f"Error converting image to array: {e}")
            return
        h, w, _ = arr.shape
        sampled_indices = np.linspace(0, w - 1, num=target_cols, dtype=int) if w >= target_cols else np.concatenate([np.arange(w), np.full(target_cols - w, w - 1)])
        row_vectors = []
        positions = []
        for r in range(h):
            row = arr[r, :, :]
            sampled = row[sampled_indices, :]
            vector = sampled.flatten().astype(np.float32) / 255.0
            row_vectors.append(vector)
            positions.append({"row": r, "sampled": sampled_indices.tolist()})
        row_vectors = np.vstack(row_vectors)
        start_idx = global_faiss_index.ntotal
        global_faiss_index.add(row_vectors)
        c = global_faiss_metadata_conn.cursor()
        for i, pos in enumerate(positions):
            vector_id = start_idx + i
            c.execute("""
                INSERT INTO faiss_metadata (vector_index, ecosystem, image_path, channel, rgba, positions)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (vector_id, ecosystem, image_path, channel, json.dumps({"mean": float(np.mean(row_vectors[i]))}), json.dumps(pos)))
        global_faiss_metadata_conn.commit()
        logger.debug(f"Streamed {row_vectors.shape[0]} vectors from {image_path}")

    # ----------------- Main Execution -----------------
    root = tk.Tk()
    root.withdraw()
    db_file = filedialog.asksaveasfilename(title="Select/Name SQLite DB File", defaultextension=".db",
                                            filetypes=[("SQLite DB Files", "*.db"), ("All Files", "*.*")])
    if not db_file:
        sys.exit("No DB file selected.")
    mapping_conn = init_text_mapping_db(db_file)
    init_metadata_table(mapping_conn)
    folder = filedialog.askdirectory(title="Select Folder Containing CSV/TXT Files")
    if not folder:
        sys.exit("No folder selected.")
    csv_files = [os.path.join(folder, f) for f in os.listdir(folder)
                 if f.lower().endswith((".csv", ".txt"))]
    if not csv_files:
        sys.exit("No CSV/TXT files found.")
    out_folder = filedialog.askdirectory(title="Select Output Folder for Final Images")
    if not out_folder:
        sys.exit("No output folder selected.")
    ecosystems = []
    for fp in csv_files:
        logger.debug("Ingesting file: %s", fp)
        headers, stats, rows = ingest_csv_vectorized(fp)
        if headers is None:
            logger.warning("Skipping file due to ingestion error: %s", fp)
            continue
        eco = {
            "file": os.path.basename(fp),
            "headers": headers,
            "stats": stats,
            "column_types": {},
            "rows": rows
        }
        for col in headers:
            eco["column_types"][col] = "numeric" if stats[col]['min'] != 0 or stats[col]['max'] != 0 else "text"
        ecosystems.append(eco)
    if ecosystems:
        merged_ecosystem = merge_ecosystems(ecosystems)
    else:
        sys.exit("No valid ecosystems ingested.")
    outputs = generate_channel_images(merged_ecosystem["rows"], merged_ecosystem["headers"],
                                        merged_ecosystem["stats"], merged_ecosystem["column_types"],
                                        out_folder, mapping_conn)
    logger.debug("Generated channel images: %s", outputs)
    reversal_data = {
        "header_order": merged_ecosystem["headers"],
        "stats": convert_np(merged_ecosystem["stats"]),
        "column_types": merged_ecosystem["column_types"]
    }
    c = mapping_conn.cursor()
    c.execute("INSERT INTO image_metadata (file_name, num_columns, header_order, stats_json, column_types_json, reversal_data_json) VALUES (?, ?, ?, ?, ?, ?)",
              (merged_ecosystem["file"],
               len(merged_ecosystem["headers"]),
               json.dumps(merged_ecosystem["headers"]),
               json.dumps(convert_np(merged_ecosystem["stats"])),
               json.dumps(merged_ecosystem["column_types"]),
               json.dumps(reversal_data)))
    mapping_conn.commit()
    logger.debug("Recorded reversal metadata in DB.")
    faiss_db = filedialog.asksaveasfilename(title="Select/Name FAISS Metadata DB File", defaultextension=".db",
                                            filetypes=[("SQLite DB Files", "*.db"), ("All Files", "*.*")])
    if not faiss_db:
        sys.exit("No FAISS DB file selected.")
    faiss_target_cols = 64
    init_faiss_stream(faiss_db, faiss_target_cols * 4)
    for ch, path in outputs.items():
        if not path: continue
        stream_image_to_faiss(path, ch, "merged", target_width=1920, target_height=1080, target_cols=faiss_target_cols)
    faiss_index_path = filedialog.asksaveasfilename(title="Save FAISS Index As", defaultextension=".faiss",
                                                    filetypes=[("FAISS Files", "*.faiss"), ("All Files", "*.*")])
    if faiss_index_path:
        faiss.write_index(global_faiss_index, faiss_index_path)
        logger.debug("Saved FAISS index to %s", faiss_index_path)
    global_faiss_metadata_conn.close()
    mapping_conn.close()
    root.destroy()

if __name__ == "__main__":
    import logging, time
    start = time.time()
    main()
    logging.getLogger(__name__).info("Processing completed in %.2f seconds.", time.time()-start)
