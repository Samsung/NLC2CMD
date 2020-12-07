import json
import re
import tqdm


def _repl(m):
    text = m.group()
    text = re.sub('[^0-9A-Z]', '', text)
    text = f"_{text}"
    return text


def _build_patterns():
    pattern = re.compile(r"\[\-\[.+?\]\-\]")
    indexed_pattern = re.compile(r"\[\-\[\d\=.*?\]\-\]")
    numbered_pattern = re.compile(r"\[\-\[\$\d\]\-\]")
    return indexed_pattern, numbered_pattern, pattern


def _convert_cmd(y, numbered_name, numbered_pattern, pattern):
    y_text = y['y_text']
    # Find number patterns
    # ex> [-[$1]-]
    for name in re.findall(numbered_pattern, y_text):
        for num in ['1', '2', '3']:
            if num in name:
                y_text = y_text.replace(name, numbered_name[num])

    y_text = re.sub(pattern, _repl, y_text)
    return y_text


def _convert_nl(x, indexed_pattern, pattern, numbered_name):
    x_text = x['x_text']
    # Find patterns with numbers in front
    # ex> [-[1=FILENAME]-]
    for name in re.findall(indexed_pattern, x_text):
        for num in ['1', '2', '3']:
            if num in name:
                numbered_name[num] = name

    x_text = re.sub(pattern, _repl, x_text)
    return x_text


def _make_pair_dataset(cmds, invocations):
    new_data = []
    for cmd in cmds:
        for invocation in invocations:
            new_data += [{"invocation": invocation, "cmd": cmd}]
    return new_data


def convert(ainix_data):
    indexed_pattern, numbered_pattern, pattern = _build_patterns()
    new_data = []
    for idx in tqdm.tqdm(ainix_data):
        datum = ainix_data[idx]
        numbered_name = {}
        invocations = []
        for x in datum['x']:
            if x['x_weight'] < 0.5:
                continue
            invocations.append(_convert_nl(x, indexed_pattern, pattern, numbered_name))

        cmds = []
        for y in datum['y']:
            if y['y_preference'] < 0.5:
                continue
            cmds.append(_convert_cmd(y, numbered_name, numbered_pattern, pattern))
        new_data += _make_pair_dataset(cmds, invocations)

    final = {}
    for idx, datum in enumerate(new_data):
        final[str(idx+1)] = datum

    return final


def main():
    with open('data/ainix-kernal-dataset-archie.json', 'r') as f:
        ainix_data = json.load(f)

    final = convert(ainix_data)

    with open('data/ainix_data.json', 'w') as f:
        json.dump(final, f)


if __name__ == '__main__':
    main()
