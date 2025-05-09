def remove_duplicate_fasta_entries(content):
    entries = content.strip().split(">")
    seen = set()
    unique_entries = []
    removed_count = 0

    for entry in entries:
        if not entry.strip():
            continue
        header, *sequence = entry.splitlines()
        header = header.strip()
        sequence = "\n".join(line.strip() for line in sequence)
        if header not in seen:
            seen.add(header)
            unique_entries.append(f">{header}\n{sequence}")
        else:
            removed_count += 1

    return "\n".join(unique_entries), removed_count